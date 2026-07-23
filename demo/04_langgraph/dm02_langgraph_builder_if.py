"""
传统构造着模式, 构建LangGraph图
条件边：分类后，根据 route_by_category 的返回值选择目标节点
  .add_conditional_edges

Author: danke
Date: 2026/7/22 17:14
"""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class HelperState(TypedDict):
    question: str  # 用户的问题（输入）
    category: str  # 分类结果：concept / code / chat（中间结果）
    answer: str  # 最终回应（输出）

def answer_concept_node(state: HelperState) -> dict:
    return {"answer": f"【概念解答】关于「{state['question']}」，它的核心思想是……"}


def answer_code_node(state: HelperState) -> dict:
    return {"answer": f"【代码助手】针对「{state['question']}」，我们一步步排查……"}


def answer_chat_node(state: HelperState) -> dict:
    return {"answer": "【闲聊】哈哈，没问题，我们继续聊～"}


def route_by_category(state: HelperState) -> str:
   """路由函数：返回一个字符串路标，决定下一步去哪个节点"""
   q = state["question"]
   if "代码" in q or "报错" in q or "bug" in q:
       category = "code"
   elif "什么是" in q or "概念" in q or "原理" in q:
       category = "concept"
   else:
       category = "chat"
   return category


graph = (StateGraph(HelperState)  # ① 用 State 类型创建图构建器
          # 注册节点（名字, 函数）
         .add_node("answer_concept", answer_concept_node)
         .add_node("answer_code", answer_code_node)
         .add_node("answer_chat", answer_chat_node)
          # 设置边:
          #          ┌──► concept ──┐
          #   START ─┼──► code ─────┼──► END
          #          └──► chat ─────┘
          #                 （由 route_by_category 决定走哪条）
         # .add_edge(START, "classify")  # ③ 连边：START 是入口
          # 条件边：分类后，根据 route_by_category 的返回值选择目标节点
         .add_conditional_edges(source=START,  # 从哪个节点出发
                                path=route_by_category,  # 路由函数
                                path_map={                      # 路标 → 目标节点 的映射, 如果名字一样, 可以自动映射, 不需要path_map
                                    "concept": "answer_concept",
                                    "code": "answer_code",
                                    "chat": "answer_chat"
                                })  # 分类后去回应
         .add_edge("answer_concept", END)  # 回应后结束（END 是出口）
         .add_edge("answer_code", END)  # 回应后结束（END 是出口）
         .add_edge("answer_chat", END)  # 回应后结束（END 是出口）
          # 编译成可执行的图
         .compile())

graph.get_graph().draw_mermaid_png(output_file_path="graph.png")  # 保存为图片

# 试三种不同的问题，观察走了不同分支
for q in ["什么是装饰器", "这段代码报错怎么办", "今天天气不错"]:
    result = graph.invoke({"question": q, "category": "", "answer": ""})
    print(f"问题：{q}\n  → 分类：{result['category']}　回应：{result['answer']}\n")
