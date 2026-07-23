"""
协程、async / await 与 asyncio.run
异步编程的三个最基础概念：

协程函数：用 async def 定义的函数。调用它不会立刻执行，而是返回一个「协程对象」（可以理解为「一个待办任务」）。
await：用来「等待一个协程跑完并拿到它的结果」。只能写在 async def 函数内部。
asyncio.run(...)：异步世界的「总开关 / 入口」，负责启动事件循环并运行最外层的协程。

Author: danke
Date: 2026/7/22 10:53
"""
import asyncio

async def say_hello():
    print("Hello")
    await asyncio.sleep(1)        # 异步地等 1 秒（不阻塞事件循环）
    print("Async")
    return "完成"

async def main():
    result = await say_hello()    # 用 await 等它跑完并拿到返回值
    print("拿到结果：", result)

asyncio.run(main())               # 从同步世界进入异步世界的唯一入口
