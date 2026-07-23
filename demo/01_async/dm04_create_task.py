"""
asyncio.create_task 将一个协程对象包装成一个任务（Task），并立即将其注册到当前正在运行的事件循环中，让它开始调度执行

有些活儿很慢，但用户不需要傻等结果。比如试卷批改：接口可以先告诉用户「已收到，正在后台批改」，立刻返回，批改任务在后台慢慢跑。这就要用到 asyncio.create_task——它把一个协程「扔到后台去跑」，不阻塞当前流程。

但这里有一个非常隐蔽、新手必踩的坑：

asyncio.create_task 返回一个 Task 对象。如果你没有用变量持有它的强引用，Python 的垃圾回收器可能在任务还没跑完时就把它回收掉，导致后台任务无声无息地消失。

正确的做法是：用一个模块级的 set 持有所有后台任务的引用，并在任务完成时把它从 set 里移除（避免内存泄漏）：

Author: danke
Date: 2026/7/22 11:23
"""
import asyncio

# 模块级集合：持有所有后台任务的强引用，防止被 GC 提前回收
_background_tasks: set[asyncio.Task] = set()

async def grade_exam(exam_id):
    print(f"开始批改试卷 {exam_id}……")
    await asyncio.sleep(2)               # 模拟耗时的批改过程
    print(f"试卷 {exam_id} 批改完成")

async def submit():
    task = asyncio.create_task(grade_exam("EX-001"))  # 丢到后台
    _background_tasks.add(task)                         # 关键①：强引用，防 GC
    task.add_done_callback(_background_tasks.discard)   # 关键②：跑完自动移除
    print("接口立即返回：已收到，正在后台批改")

async def main():
    await submit()
    await asyncio.sleep(3)    # 模拟服务持续运行，给后台任务跑完的时间
    print("当前后台任务数：", len(_background_tasks))

asyncio.run(main())


async def download_picture(session, url):
    print(f'开始下载: {url}')

    # 发送网络请求，获取这张图片，请求发出去后，要等待服务器把数据返回，等的这段时间就是IO等待
    async with session.get(url) as response:
        # 等待数据（图片数据可能分多次传输，需要等待数据全部读完，等的这段时间也是IO等待）
        content = await response.read()
        # 保存图片到本地
        with open(f'./data/{url[-10:]}', 'wb') as f:
            f.write(content)
    print(f'下载和保存完毕')

if __name__ == '__main__':
    asyncio.run(main())