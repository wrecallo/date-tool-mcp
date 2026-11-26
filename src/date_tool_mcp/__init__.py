from .server import mcp


def main() -> None:
    """date-tool MCP Server 入口，默认使用 stdio 传输。"""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
