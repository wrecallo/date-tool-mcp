import asyncio
import os
from datetime import datetime, timezone
from pathlib import Path
import sys
import sysconfig
import tempfile
import unittest
from unittest.mock import patch
from zoneinfo import ZoneInfo

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from date_tool_mcp.server import get_today


class DateTests(unittest.TestCase):
    def test_date_uses_beijing_day_at_utc_boundary(self):
        class FrozenDateTime(datetime):
            @classmethod
            def now(cls, tz=None):
                instant = datetime(2026, 11, 25, 16, 30, tzinfo=timezone.utc)
                return instant.astimezone(tz) if tz else instant.replace(tzinfo=None)

        with patch("date_tool_mcp.server.datetime", FrozenDateTime):
            self.assertEqual(get_today(), "2026-11-26")


class StdioTests(unittest.IsolatedAsyncioTestCase):
    async def check_server(self, command, args):
        # An installed package must work outside the source checkout.
        with tempfile.TemporaryDirectory() as cwd:
            params = StdioServerParameters(command=command, args=args, cwd=cwd)
            async with stdio_client(params) as (read, write):
                async with ClientSession(read, write) as session:
                    await asyncio.wait_for(self.check_protocol(session), timeout=30)

    async def check_protocol(self, session):
        await session.initialize()
        tools = await session.list_tools()
        self.assertEqual([tool.name for tool in tools.tools], ["get_today"])
        self.assertFalse(tools.tools[0].inputSchema.get("required"))

        before = datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d")
        result = await session.call_tool("get_today", {})
        after = datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d")
        self.assertFalse(result.isError)
        self.assertEqual(len(result.content), 1)
        self.assertEqual(result.content[0].type, "text")
        self.assertIn(result.content[0].text, {before, after})

    async def test_python_module(self):
        await self.check_server(sys.executable, ["-m", "date_tool_mcp"])

    async def test_installed_command(self):
        suffix = ".exe" if os.name == "nt" else ""
        command = Path(sysconfig.get_path("scripts")) / f"date-tool-mcp{suffix}"
        self.assertTrue(command.is_file(), f"Install the package first: {command}")
        await self.check_server(str(command), [])


if __name__ == "__main__":
    unittest.main()
