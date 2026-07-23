"""
生成器与 yield —— 一个能「暂停」的函数
普通函数一旦 return 就彻底结束了。但有一种特殊函数，用 yield 代替 return，它能执行到一半「暂停」，把值交出去，之后还能从暂停的地方「继续」往下跑。这种函数叫生成器。

Author: danke
Date: 2026/7/22 12:13
"""
def my_gen():
    print("A：第一段")
    yield                # 执行到这里「暂停」，把控制权交出去
    print("B：第二段")    # 等被要求「继续」时，才会执行这里

g = my_gen()             # 注意：此时函数体一行都还没执行！只是创建了生成器
print("=== 第一次 next ===")
next(g)                  # 让它跑到第一个 yield 处暂停 → 打印 A
print("=== 第二次 next ===")
next(g)                  # 让它从 yield 之后「继续」 → 打印 B
