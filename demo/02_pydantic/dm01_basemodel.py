"""
BaseModel 与自动校验

Author: danke
Date: 2026/7/22 14:46
"""
from pydantic import BaseModel, ValidationError


class Student(BaseModel):
    name: str          # 字符串
    age: int           # 整数

# 用关键字参数创建实例
s = Student(name="小明", age=18)
print(s.name)          # 小明
print(s.age)           # 18
print(s)               # name='小明' age=18

try:
    # Pydantic 会在创建实例时自动校验类型。它还会做合理的自动转换
    Student(name="小刚", age="18")   # "十八" 无法转成整数
    # 但如果数据没法合理转换，Pydantic 会立刻抛出 ValidationError，并告诉你错在哪：
    Student(name="小刚", age="十八")   # "十八" 无法转成整数
except ValidationError as e:
    print(e)