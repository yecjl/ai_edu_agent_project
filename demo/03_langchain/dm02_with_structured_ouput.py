"""


Author: danke
Date: 2026/7/22 16:42
"""
import asyncio

from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field

from config import settings

# model_provider="openai" + base_url=...：这两个配合使用，意思是「用 OpenAI 的协议格式，但把请求发到 DeepSeek 的地址」。
# 这里有个**必须避开的坑**：千万**不要**把模型名写成 "deepseek/deepseek-chat" 这种带前缀的形式，那会触发框架去找另一个专用的 langchain-deepseek 包，导致出错。
# 正确做法就是上面这样：model="deepseek-chat" + model_provider="openai" + base_url。
llm = init_chat_model(
    model=settings.llm_model_chat,  # 模型名称
    model_provider="openai",  # 走 OpenAI 兼容协议（关键）
    api_key=settings.llm_api_key,  # DeepSeek 的 API Key
    base_url=settings.llm_base_url,  # DeepSeek 接口地址（关键）
    temperature=0,  # 输出的随机性，0 = 最稳定
)

# ① 定义期望的输出结构（回顾 2.2：description 就是给大模型的填空指令）
class PersonInfo(BaseModel):
    name: str = Field(description="姓名")
    age:  int = Field(description="年龄（整数）")
    city: str = Field(description="所在城市")

# ② 把模型绑定上去，得到一个「结构化输出版」的 llm
structured_llm = llm.with_structured_output(PersonInfo, method='function_calling')

async def main():
    messages = [
        SystemMessage(content="你是一位专业的 Python 讲师，用一句话回答。"),
        HumanMessage(content="什么是装饰器？"),
    ]
    # ③ 调用后直接返回 PersonInfo 对象，不是文本！
    result:PersonInfo = await structured_llm.ainvoke(messages)     # 异步调用，返回一个 AIMessage
    print(type(result))  # <class '__main__.PersonInfo'>
    print(result.name)  # 小明
    print(result.age)  # 25
    print(result.city)  # 上海

asyncio.run(main())
