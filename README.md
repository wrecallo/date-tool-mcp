# date-tool-mcp

一个获取今天日期的 MCP（Model Context Protocol）服务。提供 `get_today` 工具，返回北京时间（`Asia/Shanghai`，UTC+8）的日期，格式为 `YYYY-MM-DD`。服务默认使用 **stdio** 传输，可用于魔搭 MCP 广场的“从 GitHub 仓库快速创建”和托管部署。

服务不需要 API Key、环境变量、本地文件或数据库。日期按北京时间计算，不受托管机器系统时区影响。

## MCP 服务配置（Server config）

**发布前提：维护者需要先将本项目发布到 PyPI，包名为 `date-tool-mcp`。** 仅将代码推送到 GitHub 不能完成魔搭托管部署；下列配置在 PyPI 包发布成功后可用。

```json
{
  "mcpServers": {
    "date-tool-mcp": {
      "command": "uvx",
      "args": ["date-tool-mcp@latest"]
    }
  }
}
```

此配置通过 `uvx` 从 PyPI 安装并启动 stdio 服务。环境变量配置留空即可；`DASHSCOPE_API_KEY` 仅用于仓库内的可选大模型客户端示例，与 MCP 服务本身无关。

## 工具

| 工具名称 | 输入参数 | 返回值 |
| --- | --- | --- |
| `get_today` | 无，调用参数为 `{}` | 北京时间的今天日期，例如 `2026-11-26` |

适用场景：让 AI 助手回答“今天几号”、获取生成文档时使用的当前日期。

## 发布到 PyPI

需要 Python 3.10+ 和 [uv](https://docs.astral.sh/uv/getting-started/installation/)。在项目根目录执行：

```bash
uv build
uvx twine check dist/*
uv publish dist/*
```

`uv publish` 会要求进行 PyPI 身份验证，使用你自己的 PyPI API Token。不要把 Token 写入代码或提交到 GitHub。更新已发布版本时，先增加 `pyproject.toml` 中的 `version`，再构建并上传对应新版本的产物；PyPI 不允许覆盖已有版本。

首次发布前，请确认你能在 PyPI 使用 `date-tool-mcp` 包名。如果该名称已被他人占用，需要同时调整 `pyproject.toml` 的项目名、命令入口名，以及上方服务配置的包名。

发布完成后验证：

```bash
uvx date-tool-mcp@latest
```

命令启动后等待 MCP 客户端通过 stdin/stdout 通信属于正常现象，不会显示网页；可按 Ctrl+C 退出。下方的协议测试会实际执行初始化、工具发现和工具调用。

## 在魔搭从 GitHub 仓库快速创建

根据[魔搭官方创建指南](https://www.modelscope.cn/docs/mcp/create)，快速创建会从 GitHub 仓库根目录的 README 正文提取服务介绍及 stdio 配置；托管部署通过 `uvx` / `npx` 从 PyPI / NPM 安装包，当前不支持直接从 GitHub 拉源码部署。

1. 完成上面的 PyPI 发布，并将 `README.md`、`pyproject.toml` 和 `src/` 等项目文件提交、推送到公开的 GitHub 仓库。
2. 打开[魔搭 MCP 创建页面](https://modelscope.cn/mcp/servers/create)，选择“从 GitHub 仓库快速创建”。
3. 按下表填写信息并创建，等待 README 自动解析。
4. 在服务设置中确认提取出的配置与本文“Server config”一致，环境变量无需填写。
5. 等待自动部署检测通过。在工具测试页调用 `get_today`，参数为 `{}`。通过后可获取魔搭提供的远程连接配置。

| 表单字段 | 填写内容 |
| --- | --- |
| GitHub 地址 | `https://github.com/wrecallo/date-tool-mcp` |
| 英文名称 | `date-tool-mcp` |
| 展示名称 | 今日日期工具 |
| 所有者 | 你的魔搭账号或组织 |
| 是否公开 | 公开 |
| 托管类型 | **可托管部署** |

魔搭部署检测会检查服务配置、安装 PyPI 包、连接 MCP 服务并调用 `list_tools`。若失败，先检查包是否已发布、包名是否一致、`command` 是否为 `uvx`，以及 JSON 中是否混入注释。本仓库的 `127.0.0.1` 地址仅用于本地示例，不能填写为魔搭的公网服务地址。

## 本地开发与验证

仅安装 MCP 服务依赖（不需要大模型 API Key）：

```bash
uv sync
uv run python -m unittest discover -s tests -v
uv run date-tool-mcp
```

也可以使用 pip：

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m date_tool_mcp
```

包同时提供 `date-tool-mcp` 命令与 `python -m date_tool_mcp` 入口，两者均使用 stdio。测试会从项目外的临时目录启动已安装的两个入口，验证初始化、工具发现及日期返回值。

### 可选：本地 HTTP 传输示例

安装项目后，还可以运行以下示例；它们复用同一个工具实现：

| 传输方式 | 启动命令 | 本地客户端连接方式 |
| --- | --- | --- |
| stdio | `python mcp_server_stdio.py` | 客户端以子进程启动 |
| SSE | `python mcp_server_sse.py` | `http://127.0.0.1:8000/sse` |
| Streamable HTTP | `python mcp_server_streamable.py` | `http://127.0.0.1:8000/mcp` |

SSE 与 Streamable HTTP 均监听本机 8000 端口，请分别启动。

### 可选：LangChain 大模型客户端

```bash
python -m pip install -r requirements.txt
```

在 PowerShell 中配置模型 API Key 并运行：

```powershell
$env:DASHSCOPE_API_KEY="你的 DashScope API Key"
python mcp_client.py
```

客户端默认以 stdio 启动已安装的 `date_tool_mcp`，无需修改本地绝对路径。若使用 SSE 或 Streamable HTTP，请切换文件中的连接配置，并先启动对应服务。 `.env.example` 仅提供变量示例，代码不会自动加载 `.env`。

## 项目结构

```text
.
├── pyproject.toml             # PyPI 打包、服务依赖与命令入口
├── src/date_tool_mcp/
│   ├── __init__.py            # stdio 启动入口
│   ├── __main__.py            # python -m date_tool_mcp
│   └── server.py              # get_today 工具
├── tests/test_mcp.py          # 时区边界与 MCP 协议测试
├── mcp_server_stdio.py        # 本地 stdio 示例
├── mcp_server_sse.py          # 本地 SSE 示例
├── mcp_server_streamable.py   # 本地 Streamable HTTP 示例
├── mcp_client.py              # 可选 LangChain 客户端
├── requirements.txt          # 本地完整示例依赖
├── .env.example
└── LICENSE
```

## License

[MIT](LICENSE)
