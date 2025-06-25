'''
Author: linqibin
Date: 2025-06-12 15:18:59
LastEditors: linqibin
LastEditTime: 2025-06-23 17:59:13
Description: 

Copyright (c) 2025 by 智慧空间研究院/金地空间科技, All Rights Reserved. 
'''

from fastmcp import Context, FastMCP
import requests
import os

mcp = FastMCP('百度搜索引擎')

@mcp.tool()
def deep_search(query: str, context: Context) -> str:
    """
    利用百度搜索引擎搜索任何与园区内部无关且LLM无法回答的问题
    """
    api_key = os.environ.get('api_key') # 从环境变量中获取api_key
    if not api_key:
        api_key = context.get_http_request().query_params.get('api_key')
    url = f"https://serpapi.com/search?engine=baidu&q={query}&api_key={api_key}"
    response = requests.get(url)
    results = response.json()
    return results

if __name__ == "__main__":
    mcp.run()
    # mcp.run(transport="sse", port=9081)