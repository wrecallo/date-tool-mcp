---
license: MIT
tasks:
  - any
language:
  - zh
  - en
tags:
  - mcp
  - model-context-protocol
  - langchain
  - agent
  - tool-calling
domain:
  - nlp
---

# date-tool-mcp

一个基于 [MCP (Model Context Protocol)](https://modelcontextprotocol.io) 与 [LangChain](https://python.langchain.com) 的最小示例：用 MCP Server 暴露一个「获取今天日期」的工具，再让大模型通过自然语言调用它。

项目同时演示 MCP 的三种传输方式：

| 传输方式 | Server | 客户端连接地址 |
| --- | --- | --- |
| stdio | `mcp_server_stdio.py` | 由客户端以子进程方式启动 |
| SSE | `mcp_server_sse.py` | `http://127.0.0.1:8000/sse` |
| Streamable HTTP | `mcp_server_streamable.py` | `http://127.0.0.1:8000/mcp` |

## 项目结构

```
.
├── mcp_client.py              # LangChain Agent 客户端（含三种传输的配置示例）
├── mcp_demo.py                # 使用官方 mcp-server-time 的示例（依赖 uv / uvx）
├── mcp_server_stdio.py        # stdio 传输的 MCP Server
├── mcp_server_sse.py          # SSE 传输的 MCP Server
├── mcp_server_streamable.py   # Streamable HTTP 传输的 MCP Server
├── requirements.txt
├── .env.example
└── LICENSE
```

## 环境要求

- Python 3.10+（实测 3.12）
- 可选：`uv`（仅 `mcp_demo.py` 需要，用于 `uvx` 启动官方 time server）

## 安装

```bash
pip install -r requirements.txt
```

## 配置

客户端通过环境变量读取 API Key：

```powershell
$env:DASHSCOPE_API_KEY="你的 DashScope API Key"
```

也可以复制 `.env.example` 为 `.env` 后填写。注意当前代码是直接用 `os.getenv` 读取环境变量；若想让 `.env` 自动生效，请自行安装 `python-dotenv` 并在入口处调用 `load_dotenv()`。

## 使用

`mcp_client.py` 中的三种连接配置默认以注释形式给出，**按需取消注释其中一种**即可。

### 1) stdio

客户端会自动以子进程方式启动 `mcp_server_stdio.py`，直接运行：

```bash
python mcp_client.py
```

> 请把配置里 `"args"` 的路径改成你本机 `mcp_server_stdio.py` 的绝对路径。

### 2) SSE

先启动 Server：

```bash
python mcp_server_sse.py
```

再在客户端启用 `date-tool-sse` 配置并运行：

```bash
python mcp_client.py
```

### 3) Streamable HTTP

先启动 Server：

```bash
python mcp_server_streamable.py
```

再在客户端启用 `date-tool-streamable` 配置并运行：

```bash
python mcp_client.py
```

> SSE 与 Streamable HTTP 默认都监听 `127.0.0.1:8000`，请勿同时启动。

### 附加示例：官方 time server

```bash
python mcp_demo.py
```

需要已安装 `uv`。

## 自定义

`get_today` 工具定义在各 `mcp_server_*.py` 中，使用 `@mcp.tool()` 装饰普通函数即可新增工具：

```python
@mcp.tool()
def get_today() -> str:
    """返回当前的年月日，格式 YYYY-MM-DD。"""
    return datetime.now().strftime("%Y-%m-%d")
```

## License

[MIT](LICENSE)
