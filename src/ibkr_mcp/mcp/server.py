class MCPServer:
    def __init__(self, ib_service):
        self.ib = ib_service
        self.tools = {}
        self._register_default_tools()

    # -------------------------
    # TOOL REGISTRATION
    # -------------------------
    def _register_default_tools(self):
        self.register_tool("scan_market", self.scan_market)
        self.register_tool("run_strategy", self.run_strategy)
        self.register_tool("get_account_summary", self.get_account_summary)
        self.register_tool("get_pnl", self.get_pnl)
        self.register_tool("get_historical_data", self.get_historical_data)
        self.register_tool("get_market_data", self.get_market_data)
        self.register_tool("get_fundamentals", self.get_fundamentals)
        self.register_tool("place_order", self.place_order)
        self.register_tool("launch_tws", self.launch_tws)
        self.register_tool("connect_ibkr", self.connect_ibkr)

    def register_tool(self, name: str, func):
        self.tools[name] = func

    # -------------------------
    # TOOL EXECUTION
    # -------------------------
    def call_tool(self, tool_name: str, args: dict):
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found")

        try:
            return self.tools[tool_name](**args)
        except Exception as e:
            return {"error": str(e)}

    # -------------------------
    # TOOL IMPLEMENTATIONS
    # -------------------------
    def scan_market(self, scan_type: str, num_results: int = 5):
        if scan_type == "volume":
            return self.ib.scan_top_volume_us_major(num_results)
        elif scan_type == "gainers":
            return self.ib.scan_top_percent_gainers_us_major(num_results)
        elif scan_type == "losers":
            return self.ib.scan_top_percent_losers_us_major(num_results)
        else:
            return self.ib.scan_top_rapid_movers_us_major(num_results)

    def run_strategy(self, strategy_name: str, symbol: str, window: int = 5):
        return {"status": "strategy triggered"}  # your existing logic

    def get_account_summary(self):
        return self.ib.get_account_summary()

    def get_pnl(self):
        return self.ib.get_pnl()

    def get_historical_data(self, symbol: str, duration: str, candle_size: str):
        return self.ib.get_historical_data(symbol, duration, candle_size)

    def get_market_data(self, symbol: str):
        return self.ib.start_market_data_stream(symbol)

    def get_fundamentals(self, symbol: str):
        return self.ib.get_fundamentals(symbol)

    def place_order(self, symbol: str, action: str, quantity: int, order_type="MKT", price=None):
        return self.ib.place_order(symbol, action, quantity, order_type, price)
    
    def launch_tws(self):
        return self.ib.launch_tws()

    def connect_ibkr(self):
        return self.ib.connect_ibkr()

    # -------------------------
    def list_tools(self):
        return list(self.tools.keys())