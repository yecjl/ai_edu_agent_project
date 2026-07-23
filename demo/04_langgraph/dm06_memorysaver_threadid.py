"""


Author: danke
Date: 2026/7/23 09:56
"""
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage

class ChatState(TypedDict):
    # Annotated[..., add_messages]：告诉 LangGraph 这个列表字段「追加」而非「覆盖」
    messages: Annotated[list, add_messages]

def reply_node(state: ChatState) -> dict:
    last_user_msg = state["messages"][-1].content        # 取最后一条用户消息
    history_count = len(state["messages"])               # 看看记住了几条
    reply = f"我收到了「{last_user_msg}」（当前历史共 {history_count} 条消息）"
    return {"messages": [AIMessage(content=reply)]}      # 返回的新消息会被「追加」

builder = StateGraph(ChatState)
builder.add_node("reply", reply_node)
builder.add_edge(START, "reply")
builder.add_edge("reply", END)

graph = builder.compile(checkpointer=MemorySaver())      # 绑定记忆

config = {"configurable": {"thread_id": "user-1"}}        # 同一对话的标识

graph.invoke({"messages": [HumanMessage(content="你好")]}, config)
result = graph.invoke({"messages": [HumanMessage(content="还记得我刚说了啥吗")]}, config)

# result["messages"] 总共4条消息
for m in result["messages"]:
    print(f"{type(m).__name__}: {m.content}")
