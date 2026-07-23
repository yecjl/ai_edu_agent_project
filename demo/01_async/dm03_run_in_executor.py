"""
loop.run_in_executor: 运行耗时的同步函数

异步的世界有一条铁律：绝对不能在协程里直接调用「会长时间阻塞」的同步函数。一旦这么做，整个事件循环会被卡死，所有并发任务全部停摆。

可现实是，我们经常不得不调用一些只有同步版本的重活，比如：

本地模型（BGE-M3 / BGE-Reranker / MiniLM）的推理是同步的、还挺吃 CPU；
解析 PDF、解析 Word 文档是同步的；
校验密码（bcrypt）是同步的、且故意设计得很慢。
解决办法是 loop.run_in_executor：把这个同步函数丢进一个线程池里执行，主事件循环在它跑的时候继续处理别的任务，等它跑完再用 await 取回结果。

Author: danke
Date: 2026/7/22 11:11
"""
import asyncio
import time

def heavy_sync_work(n):              # 一个阻塞的同步函数（模拟本地模型推理）
    print("同步重活开始……")
    time.sleep(2)                    # 故意阻塞 2 秒
    print("同步重活结束")
    return n * n

# 绝对不能在协程里直接调用「会长时间阻塞」的同步函数。
# 可以在协程里执行同步函数
def light_work():
    print("同步轻松活")

async def main():
    light_work()
    loop = asyncio.get_running_loop()        # 拿到当前事件循环
    # 第一个参数 None 表示用默认线程池；后面依次是「要执行的函数」和「它的参数」
    result = await loop.run_in_executor(None, heavy_sync_work, 10)
    print("结果：", result)

asyncio.run(main())