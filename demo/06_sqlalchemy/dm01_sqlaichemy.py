"""
用 SQLAlchemy 异步连接数据库

我们不直接跟数据库对话，而是通过 SQLAlchemy 这个工具库。因为整个项目是异步的（回顾 2.1，数据库查询是典型的 I/O 等待），我们用它的**异步**版本。

连接分三步：建引擎 → 建会话工厂 → 用会话：

- 引擎（engine）：管理「连接池」——一组可复用的数据库连接，避免每次都重新建立连接。
- 会话（session）：你和数据库的一次「对话」。每次要执行 SQL，就从 AsyncSessionLocal() 拿一个会话来用。
- 连接地址的唯一区别：项目用 postgresql+asyncpg://...，本 demo 用 sqlite+aiosqlite:///demo.db。换地址即可，下面的代码完全通用。

Author: danke
Date: 2026/7/23 17:14
"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# ① 创建异步引擎（管理数据库连接池）
#    项目里是 PostgreSQL： "postgresql+asyncpg://用户:密码@主机:端口/库名"
#    本 demo 用 SQLite 零配置演示；换成 PostgreSQL 只改这一行（2.6 你已连过真实 PG）：
engine = create_async_engine("sqlite+aiosqlite:///demo.db")

# ② 创建「会话工厂」，之后每次操作数据库都从它产出一个会话
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
