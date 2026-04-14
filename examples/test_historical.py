from ibkr_mcp.ibkr.service import IBService

if __name__ == "__main__":
    ib = IBService()
    ib.connect()

    data = ib.get_historical_data(
        symbol="AAPL",
        duration="3 M",
        candle_size="1 hour"
    )

    print(f"Received {len(data)} candles")
    print(data)

    ib.client.disconnect()