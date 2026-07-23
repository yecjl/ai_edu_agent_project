"""
组合复杂结构：嵌套模型与列表
真实业务的数据往往是「模型套模型」。比如一份完整简历，里面有**多条**教育经历、**多条**项目经历。Pydantic 支持把一个模型作为另一个模型的字段类型，用 list[子模型] 表示「一个列表，里面每一项都是这种子模型」：


Author: danke
Date: 2026/7/22 15:17
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
        {"school": "清华大学", "major": "计算机"},
        {"school": "北京大学", "major": "软件工程"},
    ],
)
# 也可以用子模型对象
resume = Resume(
    name="小明",
    education=[
        EducationItem(school="清华大学", major="计算机"),
        EducationItem(school="北京大学", major="软件工程"),
    ],
)

print(resume.name)                    # 小明
print(resume.education[0].school)     # 清华大学  ← 注意：已经是 EducationItem 对象了
print(type(resume.education[0]))      # <class '__main__.EducationItem'>
