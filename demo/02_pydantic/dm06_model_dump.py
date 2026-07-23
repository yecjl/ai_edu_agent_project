"""
model_dump()：在「模型」和「字典」之间转换

Author: danke
Date: 2026/7/22 15:37
"""
from pydantic import BaseModel, Field

class EducationItem(BaseModel):
    school: str = Field(description="学校名称")
    major:  str = Field(description="专业名称")

class Resume(BaseModel):
    name:      str                = Field(description="姓名")
    education: list[EducationItem] = Field(default_factory=list)  # 教育经历列表

# 创建时，嵌套部分可以直接用字典，Pydantic 会自动转成对应的子模型
resume = Resume(
    name="小明",
    education=[
        EducationItem(school="清华大学", major="计算机"),
        EducationItem(school="北京大学", major="软件工程"),
    ],
)
resume_dict = resume.model_dump()
print(resume_dict)
resume_model = Resume.model_validate(resume_dict)
print(resume_model)
resume_model = Resume(**resume_dict)
print(resume_model)


