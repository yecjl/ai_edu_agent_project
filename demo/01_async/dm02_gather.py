"""
用 asyncio.gather 实现并发
asyncio.gather 能把多个协程同时启动、一起等待，这是异步最常用、最能体现价值的能力。

Author: danke
Date: 2026/7/22 11:01
"""
import asyncio
import time

async def fetch(name, seconds):
    print(f"开始 {name}")
    await asyncio.sleep(seconds)     # 注意：换成异步 sleep
    print(f"完成 {name}")
    return f"{name} 的结果"

async def main():
    start = time.time()
    results = await asyncio.gather(   # 三个任务同时开始，一起等
        fetch("请求A", 2),
        fetch("请求B", 2),
        fetch("请求C", 2),
    )
    print("所有结果：", results) # 返回一个列表, 包含所有协程返回的结果
    print(f"总耗时：{time.time() - start:.1f} 秒")

asyncio.run(main())
