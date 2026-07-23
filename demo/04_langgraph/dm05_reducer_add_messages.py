"""
Reducer: add_messages：为消息列表量身定制的 Reducer

理解了 Reducer，add_messages 就不神秘了——它就是 LangChain 为「消息列表」专门写的一个 Reducer，比 operator.add 更聪明.

它在「追加」的基础上，还额外处理了几件消息场景特有的事：

- 如果新消息带有和旧消息相同的 id，会做更新而不是重复追加（这在流式输出等场景很有用）。
- 自动把字符串、字典等格式包装成标准的消息对象；

所以在 EduAgent 里，凡是 State 里的对话消息字段，统一写成 Annotated[list[BaseMessage], add_messages]。这一行就让「多轮对话历史自动累积」这件事变得理所当然。

Author: danke
Date: 2026/7/22 18:15
"""
import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END, add_messages


class ChatS(TypedDict):
    # 关键：用 operator.add 作为合并规则 → 列表会「拼接」而不是「覆盖」
    messages: Annotated[list, add_messages]

def add_one(state: ChatS) -> dict:
    return {"messages": ["新消息"]}

builder = StateGraph(ChatS)
builder.add_node("n", add_one)
builder.add_edge(START, "n")
builder.add_edge("n", END)
graph = builder.compile()

# 这次历史保住了，新消息被追加到末尾。秘密就在 Annotated[list, operator.add]：它告诉 LangGraph「这个字段的合并方式是『旧值 + 新值』」。
print(graph.invoke({"messages": ["历史1", "历史2"]}))
