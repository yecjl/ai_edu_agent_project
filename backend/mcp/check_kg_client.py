import asyncio, sys
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv(".env.local")

from backend.mcp.client import call_mcp_tool, list_mcp_tools

async def main():
    # base = "http://localhost:8001"          # 独立模式：直接指向端口，无路径前缀
    base = "http://localhost:8000/mcp/kb"     # main.py 有路径前缀

    tools = await list_mcp_tools(base)
    print(f"已注册工具：{[t['name'] for t in tools]}\n")

    results = await call_mcp_tool(
        server_url=base,
        tool_name="search_knowledge_base",
        arguments={"query": "介绍一下菜单工程", "tenant_id": "tenant_default"},
    )
    print(f"命中 {len(results)} 条")
    print(results)
    print(type(results))

asyncio.run(main())