"""
传统构造着模式, 构建LangGraph图
「Agent = 图」的心智模型：State、Node、Edge、Checkpointer
没有分支

Author: danke
Date: 2026/7/22 17:14
"""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# 第一步：定义 State
class HelperState(TypedDict):
    question: str      # 用户的问题（输入）
    category: str      # 分类结果：concept / code / chat（中间结果）
    answer:   str      # 最终回应（输出）

# 第二步：写节点
def classify_node(state: HelperState) -> dict:
    """分类节点：根据关键词判断问题类型"""
    q = state["question"]
    if "代码" in q or "报错" in q or "bug" in q:
        category = "code"
    elif "什么是" in q or "概念" in q or "原理" in q:
        category = "concept"
    else:
        category = "chat"
    return {"category": category}          # 只返回要更新的字段

def answer_concept_node(state: HelperState) -> dict:
    return {"answer": f"【概念解答】关于「{state['question']}」，它的核心思想是……"}

def answer_code_node(state: HelperState) -> dict:
    return {"answer": f"【代码助手】针对「{state['question']}」，我们一步步排查……"}

def answer_chat_node(state: HelperState) -> dict:
    return {"answer": "【闲聊】哈哈，没问题，我们继续聊～"}

# 第三步：搭图、编译、运行
# 执行直线, 没有分支
# START ──► classify ──► answer ──► END

# builder = StateGraph(HelperState)          # ① 用 State 类型创建图构建器
#
# builder.add_node("classify", classify_node)        # ② 注册节点（名字, 函数）
# builder.add_node("answer", answer_concept_node)
#
# builder.add_edge(START, "classify")        # ③ 连边：START 是入口
# builder.add_edge("classify", "answer")     #    分类后去回应
# builder.add_edge("answer", END)            #    回应后结束（END 是出口）
#
# graph = builder.compile()                  # ④ 编译成可执行的图


graph = (StateGraph(HelperState)                      # ① 用 State 类型创建图构建器
           .add_node("classify", classify_node)       # ② 注册节点（名字, 函数）
           .add_node("answer", answer_concept_node)
           .add_edge(START, "classify")               # ③ 连边：START 是入口
           .add_edge("classify", "answer")            #    分类后去回应
           .add_edge("answer", END)                   #    回应后结束（END 是出口）
           .compile())                                # ④ 编译成可执行的图

# ⑤ 运行：传入初始 State，拿回最终 State
result = graph.invoke({"question": "什么是装饰器", "category": "", "answer": ""})
print(result)
