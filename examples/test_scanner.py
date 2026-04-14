from ibkr_mcp.ibkr.service import IBService

if __name__ == "__main__":
    ib = IBService()
    ib.connect()

    results = ib.scan_top_volume_us_major(5)

    # for r in results:
    #     print(r)

    ib.client.disconnect()