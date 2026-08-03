"""
Markdown 加载：TextLoader
Markdown 不需要复杂的解析——本质上它是纯文本文件。用 TextLoader 读取整个文件内容，后续再交给 5.3 的 MarkdownHeaderTextSplitter 按标题切分。

Author: danke
Date: 2026/7/31 10:53
"""
from langchain_community.document_loaders import TextLoader

loader = TextLoader("../../商家智能配置助手.md", encoding="utf-8")
docs = loader.load()           # 返回 list[Document]，整个文件 = 一个 Document

print(docs[0].page_content[:200])   # 文件内容前 200 字符
print(docs[0].metadata)             # {'source': 'course.md'}