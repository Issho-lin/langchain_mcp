from fastmcp import FastMCP
from openai import OpenAI
import os

mcp = FastMCP('润色用户的问题')

client = OpenAI(api_key=os.environ.get('api_key'), base_url=os.environ.get('base_url'))
messages = [{"role": "system", "content": "给定以下对话和一个后续问题，请将后续问题重述为一个独立的问题。请注意，重述的问题应该包含足够的信息，使得没有看过对话历史的人也能理解。"}]


@mcp.tool()
def rephrase_prompt(prompt: str) -> str:
    """
    润色用户的问题
    :param prompt: 要润色的问题
    :return: 润色的结果
    """
    messages.append({"role": "user", "content": f"将这个问题重述为一个独立的问题：{prompt}"})

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