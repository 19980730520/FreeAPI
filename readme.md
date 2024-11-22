## 本项目收集了一些可以白嫖的图像识别大模型api

| 提供平台 | 模型名            | 类型   | 调用方法           |
| ---------- | -------------------- | -------- | ---------------------- |
| cloudflare | llama-3.2-11b-vision | 图文->文 | llama_3_2_11b_vision() |
| val.twon   | chatgpt-4o-mini      | 图文->文 | chatgpt_4o_mini()      |

## 1. 配置环境
```
python3 -m venv venv
source venv/bin/activate
pip install requests numpy
```

## 2. 配置config.json

将 [config.json.template](config.json.template) 复制为 config.json，并修改里面的参数。

- CF_ACCOUNT_ID: cloudflare account id，cloudflare 官网控制台获取
- CF_AUTH_TOKEN: cloufdflare auth token，cloudflare 官网控制台获取
- ValTown_Url: val.twon创建一个api代理服务的访问链接（例：`https://xxxxxx.web.val.run/api/ai-proxy`）

### 2.1 ValTown_Url

打开 [https://val.town/](https://val.town/) 

Create new HTTP

将[valtown_proxy.ts](valtown_proxy.ts)中的代码填入

val.town 提供的访问链接即为 ValTown_Url

### 2.2 Umi-OCR

Umi-OCR 是一个免费的OCR程序，运行在 Windows 平台，同时能够提供 api 接口。

[github.com/hiroi-sora/Umi-OCR](https://github.com/hiroi-sora/Umi-OCR)

## 3. 使用

参考 main.py 的代码



