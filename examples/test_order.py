from ibkr_mcp.ibkr.service import IBService

if __name__ == "__main__":
    ib = IBService()
    ib.connect()

    result = ib.place_order(
        symbol="AAPL",
        action="BUY",
        quantity=1,
        order_type="MKT"
    )

    print(result)

    ib.client.disconnect()