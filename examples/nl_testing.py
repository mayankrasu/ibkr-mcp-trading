from ibkr_mcp.llm.parser import parse_natural_language
from ibkr_mcp.mcp.server import MCPServer
from ibkr_mcp.ibkr.service import IBService

import time


def main():
    ib = IBService()
    ib.connect()

    mcp = MCPServer(ib)

    print("\n🚀 NL Trading Console (type 'exit' to quit)\n")

    try:
        while True:
            user_input = input(">> ")

            if user_input.lower() in ["exit", "quit"]:
                break

            try:
                # Step 1: NL → structured tool call
                tool_call = parse_natural_language(user_input)

                print("\n🔍 Parsed Tool Call:")
                print(tool_call)

                # Step 2: Execute MCP tool
                result = mcp.call_tool(
                    tool_call["tool"],
                    tool_call["arguments"]
                )

                print("\n✅ Result:")
                print(result)

            except Exception as e:
                print("\n❌ Error:", str(e))

            print("\n" + "-" * 50 + "\n")

    finally:
        print("Disconnecting IBKR...")
        ib.disconnect()


if __name__ == "__main__":
    main()