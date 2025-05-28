'''
Author: linqibin
Date: 2025-05-26 17:55:17
LastEditors: linqibin
LastEditTime: 2025-05-28 09:45:00
Description: 

Copyright (c) 2025 by 智慧空间研究院/金地空间科技, All Rights Reserved. 
'''
from fastmcp import FastMCP
import requests
import os

mcp = FastMCP('查询当天的新闻')

@mcp.tool()
def get_news(query: str) -> str:
    """
    利用百度api查询当天的新闻
    :param query: 要查询的关键词
    :return: 查询的结果
    """
    # api_key = "185032b32dc536d633129d221f7f7be48629f0e4569138241d817449166e21ca"
    api_key = os.environ.get('api_key')
    url = f"https://serpapi.com/search?engine=baidu&q={query}&api_key={api_key}"
    response = requests.get(url)
    results = response.json()
    return results

if __name__ == "__main__":
    mcp.run()