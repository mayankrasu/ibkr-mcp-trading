from ibkr_mcp.ibkr.service import IBService
import time

if __name__ == "__main__":
    ib = IBService()
    ib.connect()

    req_id = ib.start_market_data_stream("TSLA")

    print("Streaming started...\n")

    for _ in range(10):
        tick = ib.get_next_tick()

        if tick:
            print(tick)


    time.sleep(10)
    ib.client.disconnect()