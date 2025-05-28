/*
 * @Author: linqibin
 * @Date: 2025-05-27 09:17:09
 * @LastEditors: linqibin
 * @LastEditTime: 2025-05-28 11:56:25
 * @Description:
 *
 * Copyright (c) 2025 by 智慧空间研究院/金地空间科技, All Rights Reserved.
 */
import { MultiServerMCPClient } from "@langchain/mcp-adapters";
import { ChatOpenAI } from "@langchain/openai";
import { createReactAgent } from "@langchain/langgraph/prebuilt";
import mcpConfig from "./mcpConfig.json";
import fs from "fs";
import path from "path";
// import tools from "./tools";
import "dotenv/config";
// import { ChatPromptTemplate } from "@langchain/core/prompts";

// 读取prompt.txt文件内容
const promptPath = path.join(__dirname, "prompt.txt");
const prompt = fs.readFileSync(promptPath, "utf-8");

console.log(prompt);

// 在配置中使用读取的提示词
const model = new ChatOpenAI({
  model: process.env.MODEL_NAME,
  configuration: {
    baseURL: process.env.BASE_URL,
    apiKey: process.env.OPENAI_API_KEY,
  },
});

export async function chat(
  input: string,
  onSuccess: (content: string) => void
) {
  const client = new MultiServerMCPClient(mcpConfig);
  const tools = await client.getTools();
  //   console.log(tools);

  const agent = createReactAgent({
    llm: model,
    tools,
    prompt,
  });
  const stream = await agent.stream(
    {
      messages: [{ role: "user", content: input }],
    },
    { streamMode: "messages" }
  );
  for await (const [token] of stream) {
    console.log(token);
    if (token.content && token.response_metadata?.usage) {
    //   console.log(token.content);
      onSuccess(token.content);
    }
  }
  await client.close();
}

chat("北京天气", () => {});
