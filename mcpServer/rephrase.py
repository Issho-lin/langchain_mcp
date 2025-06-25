'''
Author: linqibin
Date: 2025-05-28 09:10:57
LastEditors: linqibin
LastEditTime: 2025-06-23 17:41:32
Description: 

Copyright (c) 2025 by 智慧空间研究院/金地空间科技, All Rights Reserved. 
'''
from fastmcp import FastMCP
from openai import OpenAI
import os

mcp = FastMCP('润色用户的问题')

client = OpenAI(api_key=os.environ.get('api_key'), base_url=os.environ.get('base_url'))
messages = [{"role": "system", "content": "给定以下对话和一个后续问题，请将后续问题重述为一个独立的问题。如果问题有歧义，请再次向用户提问确认。请注意，重述的问题应该包含足够的信息，使得没有看过对话历史的人也能理解。"}]


@mcp.tool()
def rephrase_prompt(prompt: str) -> str:
    """
    润色用户的问题
    :param prompt: 要润色的问题
    :return: 润色的结果
    """
    messages.append({"role": "user", "content": f"将这个问题重述为一个独立的问题：{prompt}，保持原有的意思。"})

    response = client.chat.completions.create(
        model=os.environ.get('model'),
        messages=messages,
        temperature=0.2,
        stream=False
    )
    result = response.choices[0].message.content
    messages.append({"role": "assistant", "content": result})
    return result

if __name__ == "__main__":
    mcp.run()