"""
用 SQLAlchemy 异步操作数据库
1. 为了零配置仍用 SQLite（pip install sqlalchemy aiosqlite）。
这里 SQLite 只是为了演示 SQLAlchemy 的用法本身——SQLAlchemy 的 API 和连接 PostgreSQL 完全一样，
区别只在连接地址那一行（你在 2.6 已经连过真实 PG 了，把地址换成 postgresql+asyncpg://... 即可）。

2.通过 SQLAlchemy 这个工具库。因为整个项目是异步的（回顾 2.1，数据库查询是典型的 I/O 等待），我们用它的异步版本。

3.执行 SQL：text() + 参数化查询（项目核心写法）
在 SQLAlchemy 里执行原生 SQL，要把 SQL 字符串用 text() 包起来，再交给会话的 execute 方法。

4.:名字 占位
而当 SQL 里需要嵌入变量时（比如「查用户名等于某个值的用户」），绝对不要用 f-string 直接拼接，
而要用参数化查询：在 SQL 里用 :名字 占位，再用一个字典把值传进去。

5.commit()（提交事务）
关于 commit()（提交事务）：INSERT / UPDATE / DELETE 这类改动，执行后必须 await session.commit() 才会真正写入数据库；
如果中途出错，可以 await session.rollback() 撤销。
在 EduAgent 里，你几乎不用手动写 commit——回顾 2.5.5 的 get_db 依赖，它已经在 yield 之后帮你自动 commit、出错自动 rollback 了。


Author: danke
Date: 2026/7/23 17:12
"""
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine("sqlite+aiosqlite:///demo.db")
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def main():
    async with AsyncSessionLocal() as session:
        # 建表（项目里由 init_db.sql 完成，这里为了演示临时建一张）
        await session.execute(text("DROP TABLE IF EXISTS users"))
        await session.execute(text("""
            CREATE TABLE users (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                username  TEXT,
                role      TEXT,
                is_active BOOLEAN
            )
        """))

        # 增（INSERT）：参数化
        await session.execute(
            text("INSERT INTO users (username, role, is_active) VALUES (:u, :r, :a)"),
            [{"u": "student01", "r": "student", "a": True},{"u": "student02", "r": "student02", "a": True}]
        )
        await session.execute(
            text("INSERT INTO users (username, role, is_active) VALUES (:u, :r, :a)"),
            {"u": "teacher01", "r": "teacher", "a": True},
        )

        # 查（SELECT）
        result = await session.execute(
            text("SELECT id, username, role FROM users WHERE role = :r"),
            {"r": "student"},
        )
        row = result.fetchone()
        print("查到学生：", row.id, row.username, row.role)

        # 改（UPDATE）
        await session.execute(
            text("UPDATE users SET is_active = :a WHERE username = :u"),
            {"a": False, "u": "student01"},
        )

        # 删（DELETE）
        await session.execute(
            text("DELETE FROM users WHERE username = :u"),
            {"u": "teacher01"},
        )

        # 提交事务：让上面所有改动真正生效
        await session.commit()

        # 验证：看看现在表里剩什么
        all_rows = (await session.execute(text("SELECT username, is_active FROM users")))
        print(f'all_rows={type(all_rows)}')
        all_rows = (await session.execute(text("SELECT username, is_active FROM users"))).mappings().all()
        print(f'all_rows={type(all_rows)}')
        print("最终数据：", [dict(r) for r in all_rows])

asyncio.run(main())
