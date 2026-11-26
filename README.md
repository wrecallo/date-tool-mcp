# date-tool-mcp

一个获取今天日期的 MCP（Model Context Protocol）服务。提供 `get_today` 工具，返回北京时间（`Asia/Shanghai`，UTC+8）的日期，格式为 `YYYY-MM-DD`。服务默认使用 **stdio** 传输，可直接用于魔搭 MCP 广场的「从 GitHub 仓库快速创建」与托管部署。

服务不需要 API Key、环境变量、本地文件或数据库。日期按北京时间计算，不受托管机器系统时区影响。

## 工具

| 工具名称 | 输入参数 | 返回值 |
| --- | --- | --- |
| `get_today` | 无，调用参数为 `{}` | 北京时间的今天日期，例如 `2026-11-26` |

适用场景：让 AI 助手回答「今天几号」、为生成的文档补上当前日期。

## MCP 服务配置（Server config）

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

配置通过 `uvx` 从 PyPI 安装并启动 stdio 服务，**无需填写任何环境变量**。`DASHSCOPE_API_KEY` 仅用于仓库内可选的 LangChain 客户端示例，与 MCP 服务本身无关。

> 魔搭托管部署依赖这个配置：平台会用 `uvx` 拉取 PyPI 包并以 stdio 方式连接。**因此必须先完成下面的 PyPI 发布**，仅把代码推到 GitHub 不足以部署成功。

## 上传到 GitHub

仓库需为**公开**仓库（魔搭快速创建会读取它）。项目文件已经就绪，推送到 `main` 即可：

```bash
git add -A
git commit -m "chore: 补齐发布与魔搭部署所需文件"
git push origin main
```

推送后确认仓库根目录能直接看到 `README.md`、`pyproject.toml` 和 `src/date_tool_mcp/`。`.gitignore` 已排除 `.env`、虚拟环境和 `dist/`，不要把 PyPI Token 或 API Key 提交进仓库。

## 发布到 PyPI

魔搭托管部署只认 PyPI 包，所以先发布。项目采用 [hatchling](https://github.com/pypa/hatch) 打包，`python -m date_tool_mcp` 与 `date-tool-mcp` 命令都是 stdio 入口。

### 方式一：GitHub Actions 自动发布（推荐）

仓库内置 `.github/workflows/publish.yml`，打 `v*` 标签即自动构建、校验并发布到 PyPI，使用 PyPI Trusted Publishing（OIDC），不需要把 Token 存进仓库。

首次使用前，在 [PyPI](https://pypi.org/manage/account/publishing/) 添加一个 Trusted Publisher：

| 字段 | 值 |
| --- | --- |
| PyPI Project Name | `date-tool-mcp` |
| Owner | `wrecallo` |
| Repository name | `date-tool-mcp` |
| Workflow name | `publish.yml` |
| Environment name | `pypi` |

然后在 GitHub 仓库的 Environments 里新建名为 `pypi` 的环境（无需密钥），最后打标签发布：

```bash
git tag v0.1.0
git push origin v0.1.0
```

### 方式二：本地手动发布

需要 Python 3.10+ 和 [uv](https://docs.astral.sh/uv/getting-started/installation/)：

```bash
uv build
uvx twine check dist/*
uv publish          # 输入 PyPI API Token，不要把它写进任何文件
```

PyPI 不允许覆盖同一版本，更新时先改 `pyproject.toml` 里的 `version`，再构建上传。

发布后验证：

```bash
uvx date-tool-mcp@latest
```

命令启动后等待 MCP 客户端通过 stdin/stdout 通信属于正常现象，不会显示网页，按 Ctrl+C 退出即可。`tests/test_mcp.py` 会实际执行初始化、`list_tools` 和工具调用，可用于确认包本身可用。

## 在魔搭从 GitHub 仓库快速创建

参考[魔搭 MCP 创建文档](https://www.modelscope.cn/docs/mcp/create)。快速创建会从 GitHub 仓库根目录的 `README.md` 提取服务介绍与 stdio 配置；托管部署通过 `uvx` / `npx` 从 PyPI / NPM 安装，**不支持直接从仓库拉源码部署**。

1. 完成上面的 PyPI 发布（否则部署检测会在安装阶段失败）。
2. 确认 GitHub 仓库为公开状态，且包含 `README.md`、`pyproject.toml`、`src/`。
3. 打开[魔搭 MCP 创建页面](https://modelscope.cn/mcp/servers/create)，选择「从 GitHub 仓库快速创建」。
4. 按下表填写并创建，等待 README 自动解析。

| 表单字段 | 填写内容 |
| --- | --- |
| GitHub 地址 | `https://github.com/wrecallo/date-tool-mcp` |
| 英文名称 | `date-tool-mcp` |
| 展示名称 | 今日日期工具 |
| 所有者 | 你的魔搭账号或组织 |
| 是否公开 | 公开 |
| 托管类型 | **可托管部署** |

5. 在服务设置里确认提取出的配置与本仓库「Server config」一致，环境变量留空。
6. 等待自动部署检测通过，在工具测试页用参数 `{}` 调用 `get_today`；通过后即可获取魔搭分配的远程连接地址。

部署检测会依次检查服务配置、`uvx` 安装 PyPI 包、连接 MCP 服务并调用 `list_tools`。若失败，优先排查：包是否已发布、配置里的包名与实际包名是否一致、`command` 是否为 `uvx`、JSON 中是否混入注释。本仓库示例里的 `127.0.0.1` 地址仅用于本地，不能填作魔搭的公网服务地址。

> 若托管部署条件不满足，魔搭会把服务退化为「仅本地可用」，此时只能下发本地 `uvx` 配置，无法生成远程端点。

## 本地开发与验证

只装 MCP 服务依赖（不需要大模型 API Key）：

```bash
uv sync
uv run python -m unittest discover -s tests -v
uv run date-tool-mcp
```

也可以用 pip：

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m date_tool_mcp
```

测试会从项目外的临时目录启动已安装的两个入口（`python -m date_tool_mcp` 与 `date-tool-mcp`），验证初始化、工具发现、日期返回值，并覆盖 UTC 与北京时间跨日的边界情况。

### 可选：本地 HTTP 传输示例

| 传输方式 | 启动命令 | 客户端连接方式 |
| --- | --- | --- |
| stdio | `python mcp_server_stdio.py` | 客户端以子进程启动 |
| SSE | `python mcp_server_sse.py` | `http://127.0.0.1:8000/sse` |
| Streamable HTTP | `python mcp_server_streamable.py` | `http://127.0.0.1:8000/mcp` |

SSE 与 Streamable HTTP 都监听本机 8000 端口，请分别启动。

### 可选：LangChain 大模型客户端

```bash
python -m pip install -r requirements.txt
```

在 PowerShell 中配置模型 Key 后运行：

```powershell
$env:DASHSCOPE_API_KEY="你的 DashScope API Key"
python mcp_client.py
```

客户端默认以 stdio 启动已安装的 `date_tool_mcp`，无需硬编码本地路径。若改用 SSE 或 Streamable HTTP，请切换文件中的连接配置，并先启动对应服务。`.env.example` 仅提供变量示例，代码不会自动加载 `.env`。

## 项目结构

```text
.
├── pyproject.toml              # PyPI 打包、依赖与命令入口（魔搭部署依据）
├── src/date_tool_mcp/
│   ├── __init__.py             # stdio 启动入口 main()
│   ├── __main__.py             # python -m date_tool_mcp
│   └── server.py               # get_today 工具实现
├── tests/test_mcp.py           # 时区边界与 MCP 协议测试
├── .github/workflows/
│   ├── ci.yml                  # 推送 / PR 时跑测试
│   └── publish.yml             # 打 v* 标签自动发布 PyPI
├── mcp_server_stdio.py         # 本地 stdio 示例
├── mcp_server_sse.py           # 本地 SSE 示例
├── mcp_server_streamable.py    # 本地 Streamable HTTP 示例
├── mcp_client.py               # 可选 LangChain 客户端
├── requirements.txt            # 本地完整示例依赖
├── .env.example
└── LICENSE
```

## License

[MIT](LICENSE)
