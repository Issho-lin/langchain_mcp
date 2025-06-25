'''
Author: linqibin
Date: 2025-05-26 17:03:36
LastEditors: linqibin
LastEditTime: 2025-05-28 11:37:03
Description: 

Copyright (c) 2025 by 智慧空间研究院/金地空间科技, All Rights Reserved. 
'''
import asyncio
from  fastmcp import Client

client = Client("sports.py")

async def call_tool(sport: str):
    async with client:
        result = await client.call_tool("get_sports", { "sport": sport })
        print(result[0].text)

asyncio.run(call_tool('减肥'))