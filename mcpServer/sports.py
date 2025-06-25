'''
Author: linqibin
Date: 2025-06-24 08:59:22
LastEditors: linqibin
LastEditTime: 2025-06-24 09:36:41
Description: 

Copyright (c) 2025 by 智慧空间研究院/金地空间科技, All Rights Reserved. 
'''
from fastmcp import FastMCP
import os

mcp = FastMCP('查询园区内的运动项目')

@mcp.tool()
def get_sports(sport: str) -> str:
    """
    查询内部知识库中关于园区运动项目的信息
    :param sport: 运动项目关键词
    :return: 运动项目的信息
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'documents', 'sport.md')

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # 查找指定运动项目的信息
    sport = sport.strip().lower()
    sections = [section.strip().lower() for section in content.split('###')]
    results = []
    
    for section in sections:
        if not section:
            continue
            
        # # 提取运动项目名称
        # section_title = section.split('\n')[0].strip()
        # 检查运动项目名称是否包含查询的关键词
        if sport in section:
            results.append(section)

    if results:
        # 提取运动项目的详细信息
        sport_info = '\n'.join(results)
        return sport_info
    
    return f"未找到关于{sport}的运动项目信息。请前往客服服务中心寻求人工咨询。"

if __name__ == "__main__":
    mcp.run()