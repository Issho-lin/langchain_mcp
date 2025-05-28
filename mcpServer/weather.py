'''
Author: linqibin
Date: 2025-05-26 16:39:26
LastEditors: linqibin
LastEditTime: 2025-05-27 16:43:33
Description: 

Copyright (c) 2025 by 智慧空间研究院/金地空间科技, All Rights Reserved. 
'''
from fastmcp import FastMCP
import requests
import os

mcp = FastMCP('查询某个地区的天气预报')

@mcp.tool()
def get_weather(location: str) -> str:
    """
    利用高德api查询近4天的天气预报
    :param location: 要查询的地区
    :return: 查询的结果
    """
    # api_key = '9ffeb028648b13888b743927a941ed15'

    api_key = os.environ.get('api_key')

    city_response = requests.get(f"https://restapi.amap.com/v3/geocode/geo?address={location}&key={api_key}")
    city_result = city_response.json()
    adcode = city_result['geocodes'][0]['adcode']
    weather_info = requests.get(f"https://restapi.amap.com/v3/weather/weatherInfo?city={adcode}&key={api_key}&extensions=all")
    result = weather_info.json()
    return result


if __name__ == "__main__":
    mcp.run()
    # mcp.run(transport="sse", port=3001)
