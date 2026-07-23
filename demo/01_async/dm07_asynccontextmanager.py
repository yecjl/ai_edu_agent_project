"""
异步版：@asynccontextmanager
当「准备」和「收尾」里包含异步操作（比如异步连接数据库、异步预热模型）时，我们就需要异步版本：

装饰器换成 @asynccontextmanager；
函数前面加 async；
使用时从 with 换成 async with。
其余的「yield 上面是准备、下面是收尾」规则一模一样。

Author: danke
Date: 2026/7/22 12:10
"""
import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan():
    print("【启动】异步加载模型 / 连接数据库")    # yield 之前 = 启动
    await asyncio.sleep(0.5)                 # 这里可以写异步操作
    yield
    print("【关闭】异步释放资源")               # yield 之后 = 关闭

async def main():
    async with lifespan():
        print("应用运行中……")

asyncio.run(main())
