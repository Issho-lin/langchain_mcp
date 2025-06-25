from fastmcp import FastMCP
from utils.knowledge import search_knowledge
import os

mcp = FastMCP('查询山海行旅园区内部知识库')

@mcp.tool()
def get_sports(question: str) -> str:
    """
    查询园区内的运动项目
    :param question: 运动相关的问题
    :return: 查询结果
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(current_dir, 'db', 'sport_db')
    return search_knowledge(directory=directory, question=question)

@mcp.tool()
def get_amusement(question: str) -> str:
    """
    查询园区内的娱乐项目
    :param question: 娱乐项目相关的问题
    :return: 查询结果
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(current_dir, 'db', 'amusement_db')
    return search_knowledge(directory=directory, question=question)

@mcp.tool()
def get_biology(question: str) -> str:
    """
    查询园区内的动植物相关信息
    :param question: 动植物科普相关的问题
    :return: 查询结果
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(current_dir, 'db', 'biology_db')
    return search_knowledge(directory=directory, question=question)

if __name__ == "__main__":
    mcp.run()
    # get_sports(question="我想了解一下山海行旅园区的运动项目")