/*
 * @Author: linqibin
 * @Date: 2025-05-27 17:05:12
 * @LastEditors: linqibin
 * @LastEditTime: 2025-05-27 18:26:30
 * @Description:
 *
 * Copyright (c) 2025 by 智慧空间研究院/金地空间科技, All Rights Reserved.
 */
import express from "express";
import { chat } from "../index";

const app = express();

app.use(express.json());

app.get("/chat", async (req, res) => {
  let question = req.query.question as string;
  // 再次解码，防止客户端未正确编码
  try {
    question = decodeURIComponent(question);
  } catch (e) {}

  // 设置响应头，指定UTF-8编码
  res.setHeader("Content-Type", "text/event-stream; charset=utf-8");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");

  await chat(question, (content) => {
    // 对内容进行UTF-8编码
    const encodedContent = Buffer.from(content).toString('utf-8');
    res.write(`data: ${encodedContent}\n\n`);
  });
  res.end();
});

app.post("/chat", async (req, res) => {
  let question = req.body.question;
  // 兼容处理：如果检测到乱码，尝试转码
  if (typeof question === "string" && /[\u00C0-\u017F]/.test(question)) {
    try {
      question = Buffer.from(question, "latin1").toString("utf8");
    } catch (e) {}
  }
  console.log(question);
  res.setHeader("Content-Type", "application/octet-stream; charset=utf-8");
  await chat(question, (content) => {
    res.write(content);
  });
  res.end();
});

app.listen(3000, () => {
  console.log("Example app listening on port 3000!");
});
