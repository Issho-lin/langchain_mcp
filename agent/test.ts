/*
 * @Author: linqibin
 * @Date: 2025-05-27 09:17:09
 * @LastEditors: linqibin
 * @LastEditTime: 2025-05-27 14:52:56
 * @Description:
 *
 * Copyright (c) 2025 by 智慧空间研究院/金地空间科技, All Rights Reserved.
 */
import { ChatOpenAI } from "@langchain/openai";
import {
  AgentExecutor,
  createToolCallingAgent,
} from "langchain/agents";
import "dotenv/config";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import tools from "./tools";

async function run() {
  //   const client = new MultiServerMCPClient(mcpConfig);
  //   const tools = (await client.getTools()) as any;
  //   console.log(tools.map((tool: any) => tool));
  //   // Create an OpenAI model
  const model = new ChatOpenAI({
    model: process.env.MODEL_NAME,
    configuration: {
      baseURL: process.env.BASE_URL,
      apiKey: process.env.OPENAI_API_KEY,
    },
  });

  //   const prompt = ChatPromptTemplate.fromTemplate(`Answer the following questions as best you can. You have access to the following tools:

  // {tools}

  // Use the following format:

  // Question: the input question you must answer
  // Thought: you should always think about what to do
  // Action: the action to take, should be one of [{tool_names}]
  // Action Input: the input should be a simple string or number without quotes
  // Observation: the result of the action
  // ... (this Thought/Action/Action Input/Observation can repeat N times)
  // Thought: I now know the final answer
  // Final Answer: the final answer to the original input question

  // Begin!

  // Question: {input}
  // {agent_scratchpad}`);

  // Create the React agent
  //   const agent = await createReactAgent({
  //     llm: model,
  //     prompt,
  //     tools
  //   });

  const prompt = ChatPromptTemplate.fromMessages([
    ["system", "You are a helpful assistant"],
    ["placeholder", "{chat_history}"],
    ["human", "{input}"],
    ["placeholder", "{agent_scratchpad}"],
  ]);

  const agent = createToolCallingAgent({
    llm: model,
    tools,
    prompt,
  });

  const agentExecutor = new AgentExecutor({
    agent,
    tools,
  });

  const response = await agentExecutor.invoke({
    input: "小米汽车最新新闻？",
  });

  console.log(response);

  //   // Run the agent
  //   const response = await agent.invoke({
  //     messages: [{ role: "user", content: "小米汽车怎么样？" }],
  //   });
  //   console.log(response.messages);

  //   await client.close();
}

run();
