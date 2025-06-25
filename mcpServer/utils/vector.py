'''
Author: linqibin
Date: 2025-06-24 16:45:57
LastEditors: linqibin
LastEditTime: 2025-06-25 09:44:03
Description: 

Copyright (c) 2025 by 智慧空间研究院/金地空间科技, All Rights Reserved. 
'''

# from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import os

file_name = 'sport'

def build_vector_db():
    """构建向量数据库"""
    loader = TextLoader(f'../documents/{file_name}.md')
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    split_docs = text_splitter.split_documents(docs)
    # print("Type of split_docs:", type(split_docs))
    # print(split_docs)
    # texts = [f"{d.page_content}\n" for d in split_docs]
    # metadatas = [d.metadata for d in split_docs]
    # print(texts)
    # print(metadatas)
    for d in split_docs:
        print(f"{d.page_content}\n")
        print('=================================')

    embeddings = DashScopeEmbeddings(
        model=os.environ.get('embedding_model') or"text-embedding-v1",
        dashscope_api_key=os.environ.get('api_key') or 'sk-b72b74abd3f541a08b68dc756de84958'
    )

    # print(embeddings)
    # embeddings = embedding.embed_documents(texts)
    # print("Embeddings created.")

    # text = "This is a test query."
    # query_result = embedding.embed_query(text)

    # embeddings = embedding.embed_documents(texts)
    vector_db = FAISS.from_documents(documents=split_docs, embedding=embeddings)
    print("向量数据库创建成功，正在保存...")
    vector_db.save_local(folder_path=f'../db/{file_name}_db')
    print(f"保存成功！保存路径为：../db/{file_name}_db")

# if __name__ == "__main__":
#     # 启用tracemalloc以获取对象分配跟踪（可选）
#     import tracemalloc
#     tracemalloc.start()
    
build_vector_db()