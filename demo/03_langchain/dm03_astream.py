"""
流式输出：astream（了解即可）

Author: danke
Date: 2026/7/22 16:51
"""
import asyncio

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

from backend.config import get_settings

settings = get_settings()

llm = init_chat_model(
    model=settings.llm_model_chat,  # 模型名称
    model_provider="openai",  # 走 OpenAI 兼容协议（关键）
    api_key=settings.llm_api_key,  # DeepSeek 的 API Key
    base_url=settings.llm_base_url,  # DeepSeek 接口地址（关键）
    temperature=0,  # 输出的随机性，0 = 最稳定
)

async def main():
    messages = [HumanMessage(content="用三句话介绍一下 Python。")]
    async for chunk in llm.astream(messages):   # 逐块接收
        print(chunk.text, end="", flush=True)    # 拼接打印，形成打字机效果

asyncio.run(main())