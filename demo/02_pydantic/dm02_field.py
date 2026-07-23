"""
Field：给字段加「说明书」
必填 vs 可选：Field 里没写 default 的字段就是必填（创建实例时必须提供，否则报错）；写了 default 的就是可选的。
description：对字段含义的文字说明。请记住这个参数——下一节你会看到它有多重要。

一个常见坑：列表 / 字典的默认值要用 default_factory
如果一个字段的默认值是「空列表」或「空字典」这类可变对象，不要写 default=[]，而要写 default_factory=list：

Author: danke
Date: 2026/7/22 15:01
"""
from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    name: str = Field(description="用户姓名")  # 必填：没有默认值
    phone: str = Field(default="", description="手机号")  # 可选：有默认值 ""
    age: int = Field(default=18, description="年龄")  # 可选：默认 18
    # 为什么不能用 default=[]？ 因为如果所有实例共享同一个列表默认值，往一个实例里加元素会「污染」到其他实例。
    # default_factory=list 的意思是「每次创建实例时，都新建一个空列表」，从而避免这个隐患。
    # 当 Python 加载这个类定义时，[] 只被创建一次。之后所有未传 tags 参数的实例，其 tags 字段都指向内存中同一个列表对象
    # 可变对象都要用default_factory
    # tags:  list[str] = Field(defaul=[], description="标签列表")  # ❌写法
    # tags:  list[str] = Field(default_factory=list, description="标签列表")  # 正确写法
    hobbies:  dict[str, str] = Field(default_factory=dict, description="爱好")  # 正确写法
