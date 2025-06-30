import asyncio

from mcp import ClientSession
from mcp.client.sse import sse_client


async def main():
    # Specify the URL of the MCP server's SSE endpoint
    server_url = "http://localhost:8000/sse"

    # Create an SSE client to connect to the MCP server
    async with sse_client(server_url) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            #  List available tools
            tools = await session.list_tools()
            print("利用可能なツール:", [tool.name for tool in tools.tools])

            # Call the tool to suggest an onsen destination
            result = await session.call_tool("suggest_onsen_destination")

            # Show the result
            print(f"おすすめの旅行先は{result.content[0].text}です。")

            # Call the tool to estimate travel budget
            result = await session.call_tool(
                "estimate_travel_budget",
                {"days": 3, "people": 2, "per_day_per_person": 15000},
            )

            # Present the result
            print(f"旅行予算は{result.content[0].text}円です。")

            # Call the tool to check the best season for a destination
            result = await session.call_tool(
                "check_best_season", {"destination": "北海道"}
            )

            # Present the result
            print(f"北海道のベストシーズンは{result.content[0].text}です。")


if __name__ == "__main__":
    asyncio.run(main())
