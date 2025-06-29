'''
Author: linqibin
Date: 2025-05-26 17:55:17
LastEditors: linqibin
LastEditTime: 2025-06-23 16:12:24
Description: 

Copyright (c) 2025 by 智慧空间研究院/金地空间科技, All Rights Reserved. 
'''
from fastmcp import Context, FastMCP
import requests
import os

mcp = FastMCP('查询当天的新闻')

@mcp.prompt()
def generate_query(query: str) -> str:
    """
    优化用户输入的查询关键词
    """
    return f'{query} 在24小时之内的新闻'


@mcp.tool()
def get_news(query: str, context: Context) -> str:
    """
    利用百度api查询当天的新闻
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
    # mcp.run(transport="sse", port=3001)