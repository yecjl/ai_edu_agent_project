"""
description 为什么是「大模型结构化输出」的关键?

它直接关系到后面好几个 Agent 的实现原理。
我们后面会用到 LangChain 的一个能力：让大模型不要返回一段自由文本，而是严格按照一个 Pydantic 模型的结构来填空（对应代码 llm.with_structured_output(你的模型)）。
那么大模型怎么知道每个字段该填什么？答案就是：它会读取你这个 Pydantic 模型的「字段名 + 类型 + description」，把它们当成填空指令。 换句话说：
你给字段写的 description，就是你对大模型下达的精确指令。 description 写得越清楚，大模型填得越准。

当我们把一份简历文本和这个模型一起交给大模型时，大模型读到：

school（字符串，「学校名称」）→ 它就去简历里找学校名填进来；
degree（字符串，「学历：本科/专科/硕士等」）→ description 里给的例子帮它规范了输出格式；
duration（「在校时间，如 2020.09 - 2024.06」）→ 连日期格式都被这句话约束住了。
所以写 Pydantic 模型 = 设计大模型的输出格式 = 写提示词的一部分。这就是为什么本项目里几乎每个字段都认真写了 description。
（简历 Agent）和（问答 Agent）就会反复用到这个套路。

Author: danke
Date: 2026/7/22 15:10
"""
from pydantic import BaseModel, Field

class EducationItem(BaseModel):
    """单条教育经历"""
    school:   str = Field(description="学校名称")
    major:    str = Field(description="专业名称")
    degree:   str = Field(description="学历：本科/专科/硕士等")
    duration: str = Field(description="在校时间，如 2020.09 - 2024.06")
    gpa:      str = Field(default="", description="GPA 或成绩（可选）")
