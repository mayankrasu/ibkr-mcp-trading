from ibkr_mcp.llm.parser import parse_natural_language
from ibkr_mcp.mcp.server import MCPServer
from ibkr_mcp.ibkr.service import IBService

import time


if __name__ == "__main__":
    ib = IBService()
    ib.connect()
    mcp = MCPServer(ib)

    user_input = input("Enter instruction: ")

    try:
        # Step 1: NL → tool call
        tool_call = parse_natural_language(user_input)
        print("Parsed:", tool_call)

        # Step 2: Execute via MCP
        result = mcp.call_tool(
            tool_call["tool"],
            tool_call["arguments"]
        )

        print("Result:", result)

    except Exception as e:
        print("Error:", str(e))
