from ibkr_mcp.ibkr.service import IBService

if __name__ == "__main__":
    ib = IBService()
    ib.connect()

    results = ib.get_fundamentals("INTC")

    ib.client.disconnect()