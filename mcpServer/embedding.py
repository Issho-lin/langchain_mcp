'''
Author: linqibin
Date: 2025-05-28 17:52:49
LastEditors: linqibin
LastEditTime: 2025-06-24 09:47:32
Description: 

Copyright (c) 2025 by 智慧空间研究院/金地空间科技, All Rights Reserved. 
'''
from fastmcp import FastMCP
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableSequence, RunnablePassthrough, RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from .utils.history import JSONChatHistory

import os

mcp = FastMCP('查询知识库')

llm = ChatOpenAI(
    model=os.environ.get('model'),
    base_url=os.environ.get('base_url'),
    api_key=os.environ.get('api_key'),
    temperature=0.2
)

def build_vector_db():
    """构建向量数据库"""
    embeddings = OpenAIEmbeddings(
        model=os.environ.get('embedding_model') or "text-embedding-v1",
        base_url=os.environ.get('base_url') or 'https://dashscope.aliyuncs.com/compatible-mode/v1',
        api_key=os.environ.get('api_key') or 'sk-b72b74abd3f541a08b68dc756de84958',
        chunk_size=1000,
    )
    loader = TextLoader('./document/sport.md')
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20
    )
    split_docs = splitter.split_documents(docs)
    vector_db = FAISS.from_documents(split_docs, embeddings)
    vector_db.save_local('./db/sport_db')

@mcp.tool()
def query_knowledge_base(question: str):
    """查询知识库"""
    embeddings = OpenAIEmbeddings(
        model=os.environ.get('embedding_model'),
        base_url=os.environ.get('base_url'),
        api_key=os.environ.get('api_key'),
        chunk_size=1000,
    )
    vector_db = FAISS.load_local('./db/vector_db', embeddings)
    retriever = vector_db.as_retriever(2)
    convert_docs_to_string = lambda docs: ''.join([doc.page_content for doc in docs]).join('\n')
    retriever__input = lambda input: input['question']
    context_retriever_chain = RunnableSequence([
        retriever__input,
        retriever,
        convert_docs_to_string
    ])
    SYSTEM_TEMPLATE = """
    你是一个熟知内部知识库的机器人，你在回答时会引用知识库，并擅长通过自己的总结归纳，组织语言给出答案。
    并且回答时仅根据知识库，尽可能回答用户问题，如果知识库中没有相关内容，你可以从历史记录中找答案，如果历史记录也没有相关内容，你可以回答“原文中没有相关内容”，不要回答知识库以外的内容。
    以下是原文中跟用户回答相关的内容：
    {context}
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_TEMPLATE),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}")
    ])
    llm = ChatOpenAI(
        model=os.environ.get('model'),
        base_url=os.environ.get('base_url'),
        api_key=os.environ.get('api_key'),
    )
    chain = RunnableSequence([
        RunnablePassthrough.assign(
            context=context_retriever_chain
        ),
        prompt,
        llm,
        StrOutputParser()
    ])
    get_session_history = lambda session_id: h
    chain_with_history = RunnableWithMessageHistory(
       get_session_history=get_session_history
    )
    return chain_with_history

llm = ChatOpenAI()


build_vector_db()
# if __name__ == "__main__":
#     build_vector_db()
#     mcp.run()