"""
PDF 加载：PyPDFLoader
PyPDFLoader 是 langchain-community 自带的 PDF 加载器，底层依赖 pypdf，无需额外配置。

pip install pypdf
pip install langchain-community

Author: danke
Date: 2026/7/31 10:46
"""
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("../../陈佳露的简历(20260729).pdf")
pages = loader.load()          # 返回 list[Document]，一页 = 一个 Document

print(f"共 {len(pages)} 页")
print(pages[0].page_content)   # 第一页的文字内容
print(pages[0].metadata)       # {'source': 'course.pdf', 'page': 0}