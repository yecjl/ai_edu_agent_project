"""
环境配置

Author: danke
Date: 2026/7/22 16:42
"""
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# .env.local 在项目根目录（config.py 在 backend/ 下）
# ENV_FILE = Path(__file__).parents[0] / ".env.local"
# .env.local 与 config.py 同级
ENV_FILE = Path(__file__).parent / ".env.local"

# 方式一: 如果直接加载, 不用BaseSettings, 可以这样写:
# load_dotenv(ENV_FILE, encoding="utf-8")
# api_key = os.getenv("llm_api_key")

# 方式二: 继承 BaseSettings
class Settings(BaseSettings):
    #  env_file = ".env.local"          # 从这个文件读取配置
    #  env_file_encoding = "utf-8"      # 文件编码
    #  case_sensitive = False           # 大小写不敏感：环境变量 DB_HOST 能对应字段 db_host
    #  extra = "ignore"                 # .env.local 里多出来的、模型没定义的字段一律忽略（不报错
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore", case_sensitive=False)


    # ── 数据库（PostgreSQL）──
    db_host: str = "localhost"  # 主机；写了默认值 = 可选项
    db_port: int = 5433  # 端口；本机 5432 已占用，隔离到 5433
    db_name: str = "eduagent"  # 库名
    db_user: str = ... # 用户名；没有默认值 = 必填，.env.local 缺了会启动报错
    db_password: str = ...  # 密码；同样必填

    @property
    def database_url(self) -> str:
        """把上面几个散件拼成 SQLAlchemy 需要的连接串。
        用 @property 装饰后，可像访问属性一样 settings.database_url 取值，不用加括号调用。"""
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    # ── Milvus 向量库 ──
    milvus_host: str = "localhost"
    milvus_port: int = 19531  # 本机 19530 已占用，隔离到 19531

    # ── 大模型（DeepSeek）──
    llm_api_key: str = 'sk-ws-H.EDHMLRP.W73Z.MEYCIQCNoU5gyuNu2mZjHXjoBz8dyiHV7fNTo48uxalzuIpSdQIhAMEAkI5VKhTx029pS0GEZIUlAxs1q74OoLqO-CME2Nxt'
    llm_base_url: str = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
    llm_model_chat: str = 'qwen-plus'
    # deepseek_api_key: str  # 必填：DeepSeek 的 API Key
    # deepseek_base_url: str = "https://api.deepseek.com/v1"  # DeepSeek 接口地址
    # deepseek_model_chat: str = "deepseek-chat"  # 对话模型名
    # deepseek_model_coder: str = "deepseek-coder"  # 代码模型名

    # ── 本地模型权重路径 ──
    # reranker_model_path: str = "./models/reranker/bge-reranker-large"  # 精排模型
    reranker_model_path: str = "/Users/yezhimeier/Study/Heima/bigdata/code/models/reranker/bge-reranker-large"  # 精排模型
    classifier_model_path: str = "/Users/yezhimeier/Study/Heima/bigdata/code/models/classifier/all-MiniLM-L6-v2"  # 意图分类模型
    bge_m3_model_path: str = "/Users/yezhimeier/Study/Heima/bigdata/code/models/embedding/bge-m3"  # 嵌入模型
    finetuned_classifier_path: str = "models/classifier/query-classifier-finetuned"

    # ── JWT 认证 ──
    jwt_secret_key: str = "f8Kz9Xp2Lm7Qw4Rv1Nt6Ys8Bc3Dg0Eh5AjWkUoIxPqZyMnSrGvTbF"  # 必填：签发登录令牌用的密钥
    jwt_algorithm: str = "HS256"  # 签名算法
    jwt_access_token_expire_minutes: int = 10080  # 令牌有效期（分钟）

    # ── MCP Server 地址（第五章用）──
    kb_mcp_server_url: str = "http://localhost:8000/mcp/kb"
    web_search_mcp_url: str = "http://localhost:8000/mcp/web-search"

    # ── Web 搜索（Tavily 可选；留空则自动用免费的 DuckDuckGo）──
    tavily_api_key: str = ""

    # ── 应用基础配置 ──
    app_env: str = "local"  # 运行环境标识
    app_debug: bool = False  # 是否调试模式
    app_host: str = "0.0.0.0"  # 监听地址
    app_port: int = 8000  # 监听端口
    log_level: str = "INFO"  # 日志级别
    default_tenant_id: str = "tenant_default"  # 多租户默认值

# 单例: 饿汉式
# settings = Settings()

# 单例: 懒汉式
@lru_cache()                             # 缓存：保证 get_settings() 只创建一次 Settings、只读一次文件
def get_settings() -> Settings:
    """获取全局唯一的配置对象。任何模块要用配置，都调用这个函数。"""
    return Settings()

if __name__ == '__main__':
    print(get_settings().llm_model_chat)