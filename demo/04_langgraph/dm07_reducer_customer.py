"""
自定义计数 Reducer

最后用一个例子巩固——我们做一个「每经过一个节点就把计数加 1」的累加器，自己写一个 Reducer

Author: danke
Date: 2026/7/23 10:41
"""
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END

def add(old: int, new: int) -> int:     # 自定义 Reducer：把新旧值相加
    return old + new

class CounterState(TypedDict):
    count: Annotated[int, add]           # count 字段的合并方式 = 相加

def step(state: CounterState) -> dict:
    return {"count": 1}                  # 每个节点只「贡献」+1

builder = StateGraph(CounterState)
builder.add_node("a", step)
builder.add_node("b", step)
builder.add_node("c", step)
builder.add_edge(START, "a")
builder.add_edge("a", "b")
builder.add_edge("b", "c")
builder.add_edge("c", END)
graph = builder.compile()

print(graph.invoke({"count": 0})) # {'count': 3}

