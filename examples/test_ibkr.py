from ibkr_mcp.ibkr.service import IBService

if __name__ == "__main__":
    ib = IBService()

    ib.connect()

    print("Fetching account summary...")
    acc = ib.get_account_summary()

    print("Fetching pnl details...")
    acc = ib.get_pnl("DU2296545")

    print("\nFetching contract details...")
    contracts = ib.get_contract_details("AAPL","STK")

    ib.client.disconnect()