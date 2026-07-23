"""
BaseSettings：从环境变量 / .env 文件读配置

Pydantic 还有一个专门用来「读配置」的基类 BaseSettings（来自 pydantic-settings 包）。它能自动从环境变量或 .env 文件里把配置项读出来，并同样做类型校验。


Author: danke
Date: 2026/7/22 15:52
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 5433              # 会自动把环境变量里的字符串转成 int

settings = Settings()
print(settings.db_host, settings.db_port)
