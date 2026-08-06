"""


Author: danke
Date: 2026/8/3 21:25
"""
import os
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from openllmetry import init_auto_instrumentation  # 关键：自动注入 LLM/LangGraph 追踪

# ===================== 1. 初始化 OpenTelemetry =====================
def setup_otel():
    """配置 OTel Provider 并启用 LangGraph/LLM 自动埋点"""
    exporter = OTLPSpanExporter(endpoint="http://localhost:4317")  # 替换为你的 Collector 地址
    provider = TracerProvider()
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    # 自动为 LangChain / LangGraph / OpenAI 等注入追踪
    init_auto_instrumentation()

setup_otel()

# ===================== 2. 定义 Graph State & Nodes =====================
class AgentState(TypedDict):
    messages: Annotated[list, lambda x, y: x + y]
    next_step: str

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def researcher(state: AgentState):
    """研究节点：会被自动追踪为一个 Span"""
    response = llm.invoke("总结最新的 RAG 优化技术")
    return {"messages": [response], "next_step": "writer"}

def writer(state: AgentState):
    """写作节点：同样被自动追踪"""
    context = state["messages"][-1].content
    response = llm.invoke(f"基于以下内容撰写一段技术博客摘要：{context}")
    return {"messages": [response], "next_step": END}

# ===================== 3. 构建并运行 Graph =====================
graph = StateGraph(AgentState)
graph.add_node("researcher", researcher)
graph.add_node("writer", writer)
graph.set_entry_point("researcher")
graph.add_conditional_edges(
    "researcher",
    lambda s: s["next_step"],
    {"writer": "writer", END: END}
)
app = graph.compile()

# 运行时会自动生成完整 Trace，无需手动创建 Span
result = app.invoke({"messages": [], "next_step": ""})
print(result["messages"][-1].content)