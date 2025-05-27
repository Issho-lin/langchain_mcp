'''
Author: linqibin
Date: 2025-05-26 17:03:36
LastEditors: linqibin
LastEditTime: 2025-05-26 17:34:27
Description: 

Copyright (c) 2025 by 智慧空间研究院/金地空间科技, All Rights Reserved. 
'''
import asyncio
from  fastmcp import Client

client = Client("weather.py")

async def call_tool(location: str):
    async with client:
        result = await client.call_tool("get_weather", { "location": location })
        print(result[0].text)

asyncio.run(call_tool('北京'))