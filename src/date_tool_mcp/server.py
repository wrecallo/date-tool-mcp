from datetime import datetime
from zoneinfo import ZoneInfo

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("date-tool")
DATE_TIMEZONE = ZoneInfo("Asia/Shanghai")


@mcp.tool()
def get_today() -> str:
    """返回北京时间（Asia/Shanghai，UTC+8）的今天日期，格式 YYYY-MM-DD。"""
    return datetime.now(DATE_TIMEZONE).strftime("%Y-%m-%d")
