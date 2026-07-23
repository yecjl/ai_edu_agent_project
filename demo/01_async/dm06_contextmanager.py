"""
同步版：@contextmanager（把生成器变成上下文管理器)
Python 提供了一个装饰器 @contextmanager，能把「一个带 yield 的生成器」直接变成「一个能用于 with 的上下文管理器」。它的约定是：

yield 之前的代码 = 进入 with 时执行（准备）；
yield 之后的代码 = 离开 with 时执行（收尾）。

Author: danke
Date: 2026/7/22 12:08
"""
from contextlib import contextmanager

@contextmanager
def managed_resource():
    print("【准备】打开资源")     # 进入 with 时执行
    yield "资源对象"              # 把 yield 的值交给 as 后面的变量
    print("【收尾】关闭资源")     # 离开 with 时执行

with managed_resource() as res:
    print(f"正在使用：{res}")
