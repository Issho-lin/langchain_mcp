"""
Author: linqibin
Date: 2025-06-24 16:45:57
LastEditors: linqibin
LastEditTime: 2025-06-24 17:00:33
Description: 

Copyright (c) 2025 by 智慧空间研究院/金地空间科技, All Rights Reserved. 
"""

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.retrievers.document_compressors.chain_extract import LLMChainExtractor
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import (
    RunnableSequence,
    RunnableLambda,
    RunnablePassthrough,
)
from langchain_core.output_parsers import StrOutputParser
import os

TEMPLATE = """
你是一个熟知内部知识库的机器人，你在回答时会引用知识库，并擅长通过自己的总结归纳，组织语言给出答案。
并且回答时仅根据知识库，尽可能回答用户问题，如果知识库中没有相关内容，你可以回答“原文中没有相关内容”，不要回答知识库以外的内容。
以下是知识库中跟用户回答相关的内容：
{context}
现在，你需要基于知识库，回答以下问题：
{question}
"""


def search_knowledge(directory: str, question: str):
    """
    搜索知识库
    :param directory: 知识库名称
    :param question: 问题
    :return: 搜索的结果
    """
    api_key = os.environ.get("api_key") or "sk-b72b74abd3f541a08b68dc756de84958"
    embeddings = DashScopeEmbeddings(
        model=os.environ.get("embedding_model") or "text-embedding-v1",
        dashscope_api_key=api_key,
    )
    vector_db = FAISS.load_local(
        folder_path=directory,
        embeddings=embeddings,
        allow_dangerous_deserialization=True,
    )

    llm = ChatOpenAI(
        model=os.environ.get("model") or "qwen-turbo-1101",
        base_url=os.environ.get("base_url")
        or "https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key=api_key,
    )

    # 创建一个从 Document 中提取核心内容的 compressor
    compressor = LLMChainExtractor.from_llm(llm)

    # 创建一个会自动对上下文进行压缩的 Retriever
    retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=vector_db.as_retriever(search_kwargs={"k": 3}),
    )
    # retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    convert_docs_to_string = lambda docs: "".join(
        [f"{doc.page_content}\n" for doc in docs]
    )

    prompt = ChatPromptTemplate.from_template(template=TEMPLATE)

    retriever_chain = retriever | RunnableLambda(convert_docs_to_string)

    def input_to_context(input):
        return {"question": input, "context": retriever_chain.invoke(input=input)}

    rag_chain = RunnableSequence(
        first=RunnableLambda(input_to_context),
        middle=[
            RunnablePassthrough(func=lambda x: print(f"{x['context']}\n")),
            prompt,
            llm,
        ],
        last=StrOutputParser(),
    )

    res = rag_chain.invoke(input=question)

    print(res)

    # res = retriever.invoke(input=question)

    # print(res)

    return res


# search_knowledge(directory="../db/sport_db", question="全息战术跑怎么走")
