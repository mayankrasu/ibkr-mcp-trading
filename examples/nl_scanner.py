from ibkr_mcp.llm.parser import parse_natural_language
from ibkr_mcp.mcp.server import MCPServer
from ibkr_mcp.ibkr.service import IBService
import time


if __name__ == "__main__":
    ib = IBService()
    ib.connect()
    mcp = MCPServer(ib)

    user_input = input("Enter instruction: ")

    tool_call = parse_natural_language(user_input)

    result = mcp.call_tool(
        tool_call["tool"],
        tool_call["arguments"]
    )

    print("Disconnecting...")
    ib.disconnect()

    #print(result)