"""
用装饰器模式（Functional API）重写后，你会发现代码变得非常像普通的 Python 函数，完全不需要显式地画“节点”和“边”了

Author: danke
Date: 2026/7/22 17:14
"""
from typing import TypedDict

from langgraph.func import task, entrypoint
from langgraph.graph import StateGraph, START, END

# 1. 定义状态类
class HelperState(TypedDict):
    question: str  # 用户的问题（输入）
    category: str  # 分类结果：concept / code / chat（中间结果）
    answer: str  # 最终回应（输出）

# 2. 使用 @task 装饰器标记子任务（相当于之前的节点）
@task
def classify_node(state: HelperState) -> dict:
    """分类节点：根据关键词判断问题类型"""
    q = state["question"]
    if "代码" in q or "报错" in q or "bug" in q:
        category = "code"
    elif "什么是" in q or "概念" in q or "原理" in q:
        category = "concept"
    else:
        category = "chat"
    return {"category": category}  # 只返回要更新的字段


@task
def answer_concept_node(state: HelperState) -> dict:
    return {"answer": f"【概念解答】关于「{state['question']}」，它的核心思想是……"}


@task
def answer_code_node(state: HelperState) -> dict:
    return {"answer": f"【代码助手】针对「{state['question']}」，我们一步步排查……"}


@task
def answer_chat_node(state: HelperState) -> dict:
    return {"answer": "【闲聊】哈哈，没问题，我们继续聊～"}

# 3. 使用 @entrypoint 装饰器定义主工作流入口
@entrypoint()
def workflow(input_data: dict) -> dict:
    """主工作流：像普通 Python 代码一样编排逻辑"""
    question = input_data['question']
    # 调用分类任务，注意：被 @task 装饰的函数调用后，需要加 .result() 获取结果
    category = classify_node(question)
    # 使用标准的 Python if/else 进行路由分发（替代了之前的条件边）
    if category == "concept":
        answer = answer_concept_node(question).result()
    elif category == "code":
        answer = answer_code_node(question).result()
    else:
        answer = answer_chat_node(question).result()

    # 返回最终状态
    return {
        "question": question,
        "category": category,
        "answer": answer
    }

# 4. 运行工作流
for q in ["什么是装饰器", "这段代码报错怎么办", "今天天气不错"]:
    result = workflow.invoke({"question": q, "category": "", "answer": ""})
    print(f"问题：{q}\n  → 分类：{result['category']}　回应：{result['answer']}\n")