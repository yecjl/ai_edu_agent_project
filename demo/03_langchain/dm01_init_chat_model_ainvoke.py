"""
# LangChain
市面上的大模型有很多（DeepSeek、通义千问、OpenAI……），每家的 SDK 调用方式都不一样。LangChain 的核心价值，
就是给各种大模型提供一套「统一接口」：你用同一套代码就能调用不同的模型，将来换模型时业务代码几乎不用改。


# 1.用 init_chat_model 创建模型（1.x 新写法）
在 LangChain 1.x 里，创建一个大模型实例的标准方式是 init_chat_model（注意：不是 旧版的 ChatOpenAI(...)）。
DeepSeek 提供的是「OpenAI 兼容接口」，所以我们通过指定 model_provider="openai" + DeepSeek 的 base_url 来接入它：


# 2.消息体系：System / Human / AI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
- SystemMessage（系统消息）：给大模型设定身份和规则，比如「你是一位严谨的简历评审专家」。它影响大模型整体的行为风格。
- HumanMessage（用户消息）：用户实际说的话 / 提出的问题。
- AIMessage（AI 消息）：大模型的回复。我们调用模型后，拿到的就是一个 AIMessage；在多轮对话里，也用它来表示「AI 之前说过的话」。

# 3.调用模型：ainvoke 与 .text

Author: danke
Date: 2026/7/22 16:11
"""
import asyncio

from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

from config import settings

# model_provider="openai" + base_url=...：这两个配合使用，意思是「用 OpenAI 的协议格式，但把请求发到 DeepSeek 的地址」。
# 这里有个**必须避开的坑**：千万**不要**把模型名写成 "deepseek/deepseek-chat" 这种带前缀的形式，那会触发框架去找另一个专用的 langchain-deepseek 包，导致出错。
# 正确做法就是上面这样：model="deepseek-chat" + model_provider="openai" + base_url。
llm = init_chat_model(
    model=settings.llm_model,  # 模型名称
    model_provider="openai",  # 走 OpenAI 兼容协议（关键）
    api_key=settings.llm_api_key,  # DeepSeek 的 API Key
    base_url=settings.llm_base_url,  # DeepSeek 接口地址（关键）
    temperature=0,  # 输出的随机性，0 = 最稳定
)

async def main():
    messages = [
        SystemMessage(content="你是一位专业的 Python 讲师，用一句话回答。"),
        HumanMessage(content="什么是装饰器？"),
    ]
    response = await llm.ainvoke(messages)     # 异步调用，返回一个 AIMessage
    # （补充：AIMessage 还有一个 .content 字段是更底层的原始内容，它有时是字符串、有时是结构化的内容块；日常取纯文本时，用 .text 最省心。）
    print(response.text)                       # 用 .text 取出文本（属性，不加括号！）
    print(response.content)                    # 用 .content 取出文本（属性，不加括号！）同上

asyncio.run(main())
