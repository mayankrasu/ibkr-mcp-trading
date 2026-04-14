from ibkr_mcp.ibkr.service import IBService

ib = IBService()
ib.connect()


def scan_market(scan_type: str, num_results: int = 5):
    if scan_type == "volume":
        return ib.scan_top_volume_us_major(num_results)

    elif scan_type == "gainers":
        return ib.scan_top_percent_gainers_us_major(num_results)

    elif scan_type == "losers":
        return ib.scan_top_percent_losers_us_major(num_results)
    
    elif scan_type == "hot stocks":
        return ib.scan_top_rapid_movers_us_major(num_results)

    else:
        raise ValueError("Unknown scan type")