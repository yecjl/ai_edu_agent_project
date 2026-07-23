"""
Reducer: 自定义「合并规则」

1. 默认规则：节点返回的字典「覆盖式」合并进 State
默认规则非常简单：你返回哪个字段，就用新值覆盖 State 里那个字段；没返回的字段保持不变。 看个例子：

2. 问题来了：列表字段用「覆盖」会丢数据
设想一个聊天场景：State 里有一个 messages 列表。第一轮加进去一条消息，第二轮我们又想加一条。如果用默认的覆盖规则,

3. 解决方案：Reducer —— 自定义「合并规则」

LangGraph 允许你给某个字段指定一个自定义的合并规则，这个规则就叫 Reducer。写法是用 Annotated 把「字段类型」和「合并函数」绑在一起：
Annotated[字段类型, 合并函数]

合并函数接收两个参数：(旧值, 新值)，返回「合并后的值」。比如，对列表我们想要的是「拼接」，那合并函数就是「旧列表 + 新列表」。
Python 标准库的 operator.add 正好能做列表拼接

Author: danke
Date: 2026/7/22 18:15
"""
import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END

class ChatS(TypedDict):
    # 关键：用 operator.add 作为合并规则 → 列表会「拼接」而不是「覆盖」
    messages: Annotated[list, operator.add]

def add_one(state: ChatS) -> dict:
    return {"messages": ["新消息"]}

builder = StateGraph(ChatS)
builder.add_node("n", add_one)
builder.add_edge(START, "n")
builder.add_edge("n", END)
graph = builder.compile()

# 这次历史保住了，新消息被追加到末尾。秘密就在 Annotated[list, operator.add]：它告诉 LangGraph「这个字段的合并方式是『旧值 + 新值』」。
print(graph.invoke({"messages": ["历史1", "历史2"]}))
