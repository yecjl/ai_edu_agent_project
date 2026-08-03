"""
LangChain Document 是什么
在 LangChain 体系里，所有文档内容都用一个统一的数据结构表示 Document

Author: danke
Date: 2026/7/31 10:40
"""
from langchain_core.documents import Document

doc = Document(
    page_content="这是文档的文本内容",   # 主体文字，后续会被切分、嵌入
    metadata={                           # 附加信息，检索时随内容一起返回
        "source": "Java讲义第3章.pdf",
        "page":   2,
    }
)
print(doc)
