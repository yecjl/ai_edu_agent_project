"""
FastAPI 是什么、在项目里干什么
回顾第一章的架构图：API 层是整个系统的「大门」。前端发来的每一个请求（登录、提问、上传简历……）都先经过这道门。FastAPI 就是用来建这道门的 Web 框架，它负责：

接收并校验请求——把前端发来的 JSON、文件、URL 参数解析成 Python 对象，并自动校验格式；
调用业务逻辑——比如调用某个 Agent；
返回结果——普通 JSON，或者「一个字一个字往外吐」的流式响应。
FastAPI 的两大招牌优势，正好契合本项目：

基于类型注解自动校验：你用 Pydantic 写清楚「请求该长什么样」，校验它全包了（这就是 2.2 学的东西派上用场的地方）。
全异步：天然支持 async def 接口，和我们 2.1 学的异步、以及大模型调用无缝配合。

访问 http://localhost:8000/health，会看到 {"status":"ok"}；
访问 http://localhost:8000/docs，会看到自动生成的交互式文档。

Author: danke
Date: 2026/7/23 10:14
"""
import asyncio
import json

from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from sse_starlette import EventSourceResponse

app = FastAPI(title="EduAgent Demo")

# 请求体模型：前端要发来的数据长这样
class LoginRequest(BaseModel):
    username: str = Field(..., description="用户名或邮箱") #  ... 表示「必填」
    password: str = Field(..., description="密码")

# 响应模型：我们会返回的数据长这样
class TokenResponse(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    role:         str

"""
---------- 1. get: 无参数请求 ----------
"""
@app.get("/health")
async def health_check():
    return {"status": "ok"}

"""
---------- 2. get: 路径参数 ----------
路径参数——把参数嵌在 URL 路径里，用 {} 占位，函数里同名参数自动接收
"""
@app.get("/reviews/{review_id}")
async def get_review(review_id: str):
    return {"review_id": review_id, "status": "completed"}
# 访问 GET /reviews/abc-123 → review_id 自动等于 "abc-123"

"""
---------- 3. get: 查询参数 ----------
查询参数——URL 问号后面的 ?key=value，在函数里写成「带默认值的普通参数」
"""
@app.get("/reviews")
async def list_reviews(page: int = 1, size: int = 10):
    return {"page": page, "size": size}
# 访问 GET /reviews?page=2&size=20 → page=2, size=20
# 不传则用默认值 page=1, size=10

"""
---------- 4. post: 用 Pydantic 接收请求体 ----------
当前端要「提交数据」（比如登录时提交用户名密码），我们用一个 Pydantic 模型作为接口函数的参数。FastAPI 会自动把请求体里的 JSON 解析成这个模型，并完成校验
"""
# response_model: LoginRequest：把 Pydantic 模型写成参数类型，FastAPI 就知道「请求体应该是这个结构」，并自动解析 + 校验。
# 如果前端少传了 password，FastAPI 会自动返回一个清晰的 422 错误，你一行校验代码都不用写。
@app.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest):           # 参数类型是 Pydantic 模型
    # req 已经是解析并校验好的对象，直接用 req.username / req.password
    if req.username == "student01" and req.password == "Student@123456":
        # response_model=TokenResponse：声明这个接口返回的数据结构。它会让自动文档更准确，也会过滤掉不该返回的多余字段。
        # 比如 TokenResponse 中没有的 role 字段，FastAPI 会自动过滤掉。
        return TokenResponse(access_token="fake-token-abc", role="student")
    return {"access_token": "", "token_type": "bearer", "role": "guest"}

"""
---------- 5. Depends: 依赖注入（模拟数据库 + 模拟鉴权） ----------
为了让你在 Postman 里能直接测通，这里不强制要求传 Token，而是直接返回模拟用户。
但为了演示真实鉴权流程，我加一个可选的 Bearer Token 校验（非必须，以便测试）。
这里我们使用文档中的 get_current_user 模拟版本。
"""
async def get_db():
    return {"db": "fake_session"}

# 模拟的当前用户（不校验 Token，直接返回）
async def get_current_user():
    return {"user_id": "test_user", "role": "student"}

@app.get("/my-reviews")
async def my_reviews(
    db:dict = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # await get_db() 和内部调用也是一样的
    return {"db": db["db"], "user": current_user["user_id"], "data": "这是受保护的数据"}

"""
---------- 6. UploadFile: 文件上传 ----------
status_code=202: 设置成功码为202 
"""
@app.post("/upload", status_code=202)
async def upload(file: UploadFile = File(...)):
    content = await file.read()                  # 异步读取文件内容（bytes）
    return {"filename": file.filename, "size": len(content)}

"""
---------- 7. SSE 流式响应（重点） ----------
普通接口是「算完一次性返回」。但智能问答、模拟面试希望答案**像打字机一样逐字蹦出来**，这就要用 SSE（Server-Sent Events，服务器推送事件）：服务器和浏览器保持连接，持续不断地往外推送一小段一小段内容。
1. chat_stream(): 调用 event_generator() → 得到一个 AsyncGenerator 对象（惰性，未执行）
2. chat_stream(): 将该对象传给 EventSourceResponse() → 立即返回 HTTP 200 响应头
3. sse-starlette 框架: 在后台通过 async for item in generator: 逐次拉取数据
4. 每次拉取时: 生成器才真正执行到下一个 yield，产出一个 token
5. 框架: 将 yield 出的数据写入 HTTP 响应流，flush 给客户端
6. 循环结束: 生成器耗尽，连接关闭
"""
@app.post("/chat/stream")
async def chat_stream():
    async def event_generator():
        answer = "装饰器是一种包装函数的语法。"
        for char in answer:                       # 模拟逐字生成
            await asyncio.sleep(0.1)
            # 每个事件是一个字典，data 里放 JSON 字符串
            yield {"data": json.dumps({"type": "token", "content": char}, ensure_ascii=False)}
        yield {"data": json.dumps({"type": "done"})}   # 结束标志

    # event_generator() 调用后返回的是一个 AsyncGenerator 对象, 用 EventSourceResponse 包装成 SSE 响应
    return EventSourceResponse(event_generator())


"""
---------- 8. 错误处理 ----------
需要返回错误时，抛出 HTTPException 即可，FastAPI 会把它转成对应的 HTTP 错误响应
status_code 是 HTTP 状态码（404 = 找不到，401 = 未授权，400 = 请求有误……），detail 是给前端看的错误说明。
"""
def find_review(review_id):
    print(review_id)


@app.get("/reviews_error/{review_id}")
async def get_review_error(review_id: str):
    review = find_review(review_id)     # 伪代码
    if review is None:
        raise HTTPException(status_code=404, detail="审查记录不存在")
    return review


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
    # Terminal: uvicorn dm:app --reload   # dm是python文件名, app是FastAPI对象