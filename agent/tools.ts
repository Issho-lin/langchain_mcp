import {
  DynamicStructuredTool,
} from "@langchain/core/tools";
import { z } from "zod";

const get_weather = new DynamicStructuredTool({
  name: "mcp__weather__get_weather",
  description: "利用高德api查询近4天的天气预报",
  schema: z.object({
    location: z.string().describe("要查询的地区"),
  }),
  func: async ({ location }: { location: string }) => {
    const api_key = "9ffeb028648b13888b743927a941ed15";
    const city_response = await fetch(
      `https://restapi.amap.com/v3/geocode/geo?address=${location}&key=${api_key}`
    );
    const city_info = await city_response.json();
    const adcode = city_info.geocodes[0].adcode;
    const weather_response = await fetch(
      `https://restapi.amap.com/v3/weather/weatherInfo?city=${adcode}&key=${api_key}&extensions=all`
    );
    const weather_info = await weather_response.json();
    return JSON.stringify(weather_info)
  },
});

const get_news = new DynamicStructuredTool({
  name: "mcp__news__get_news",
  description: "利用百度api查询当天的新闻",
  schema: z.object({
    query: z.string().describe("要查询的关键词"),
  }),
  func: async ({ query }: { query: string }) => {
    const api_key = "185032b32dc536d633129d221f7f7be48629f0e4569138241d817449166e21ca"
    const response = await fetch(`https://serpapi.com/search?engine=baidu&q=${query}&api_key=${api_key}`)
    const info = await response.json()
    return JSON.stringify(info)
  },
});

export default [get_weather, get_news];
