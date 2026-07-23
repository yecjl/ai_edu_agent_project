"""
环境配置

Author: danke
Date: 2026/7/22 16:42
"""
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).parents[0] / ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore")
    llm_model: str = ...
    llm_api_key: str = ...
    llm_base_url: str = ...


settings = Settings()


if __name__ == '__main__':
    print(settings.llm_model)