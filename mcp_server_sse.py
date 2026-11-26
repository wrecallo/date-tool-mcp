from date_tool_mcp.server import mcp

# SSE 传输：服务常驻，客户端通过 http://127.0.0.1:8000/sse 连接
mcp.settings.host = "127.0.0.1"
mcp.settings.port = 8000

if __name__ == "__main__":
    mcp.run(transport="sse")
