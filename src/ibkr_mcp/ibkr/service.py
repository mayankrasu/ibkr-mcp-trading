import time
from ibkr_mcp.ibkr.client import IBClient
from ibapi.contract import Contract
from ibkr_mcp.ibkr.contracts import create_stock_contract
from ibkr_mcp.ibkr.orders import market_order, limit_order
from ibkr_mcp.utils.fundamentals import extract_fundamentals
from ibapi.scanner import ScannerSubscription
import time
import subprocess
from tabulate import tabulate
from typing import Dict, Optional
import threading
import xml.etree.ElementTree as ET


class IBService:
    def __init__(self):
        self.client = IBClient()
        self.thread = None

    def launch_tws(self):
        if self.client.isConnected():
            return {"status": "Already connected"}

        try:
            # Launch TWS (update path if needed)
            subprocess.Popen(r"C:\Jts\tws.exe")

            return {
                "status": "TWS launched",
                "message": "Please login manually. Then run connect command."
            }

        except Exception as e:
            return {"error": str(e)}
    
    def connect_ibkr(self):
        if self.client.isConnected():
            return {"status": "Already connected"}
        
        time.sleep(10)   # wait for user login
        self.connect()
        
        return {"status": "Connected to IBKR"}

    # -------------------------
    # Connect
    # -------------------------
    def connect(self, host="127.0.0.1", port=7497, client_id=1):
        self.client.connect(host, port, client_id)

        self.thread = threading.Thread(target=self.client.run, daemon=True)
        self.thread.start()

        time.sleep(1)  # some lag to ensure connection

    # -------------------------
    # Disconnect
    # -------------------------

    def disconnect(self):
        if self.client.isConnected():
            self.client.disconnect()

        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)

    # -------------------------
    # Account Summary
    # -------------------------
    def get_account_summary(self):
        req_id = 1
        self.client.reqAccountSummary(req_id, "All", "$LEDGER")

        results = []

        while True:
            item = self.client.account_queue.get()

            if item is None:
                break

            results.append(item)

            if self.client.account_queue.empty():
                break

        return results
    
    # -------------------------
    # PnL Summary
    # -------------------------
    def get_pnl(self, account):
        req_id = 1
        self.client.reqPnL(req_id, account, "")

        results = []

        while True:
            item = self.client.pnl_queue.get()

            if item is None:
                break

            results.append(item)

            if self.client.pnl_queue.empty():
                break

        return results

    # -------------------------
    # Contract Details
    # -------------------------
    def get_contract_details(self, symbol: str, secType: str, currency: str = "USD"):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = secType
        contract.exchange = "SMART"
        contract.currency = currency

        req_id = 2
        self.client.reqContractDetails(req_id, contract)

        results = []

        while True:
            item = self.client.contract_queue.get()

            if item == "END":
                break

            results.append(item)

        return results
    
    # -------------------------
    # historical data
    # -------------------------
    def get_historical_data(self, symbol: str, duration="30 D", candle_size="30 mins"):
        contract = create_stock_contract(symbol)
        req_id = 1
        # reset state
        self.client.hist_data = []
        self.client.hist_data_done = False
        self.client.reqHistoricalData(reqId=req_id, 
                                        contract=contract,
                                        endDateTime='',
                                        durationStr=duration,
                                        barSizeSetting=candle_size,
                                        whatToShow='ADJUSTED_LAST',
                                        useRTH=1,
                                        formatDate=1,
                                        keepUpToDate=False,
                                        chartOptions=[])

        # wait until IBKR finishes
        while not self.client.hist_data_done:
            time.sleep(0.1)

        return self.client.hist_data
    

    # -------------------------
    # streaming data
    # -------------------------
    def start_market_data_stream(self, symbol: str):
        contract = create_stock_contract(symbol)

        req_id = 100  # ideally generate dynamically

        self.client.reqMktData(
            reqId=req_id,
            contract=contract,
            genericTickList="",
            snapshot=False,
            regulatorySnapshot=False,
            mktDataOptions=[]
        )

        return req_id
    
    def get_next_tick(self, timeout=5):
        try:
            return self.client.market_data_queue.get(timeout=timeout)
        except:
            return None
        
    # -------------------------
    # Get Fundamental Data
    # -------------------------
        
    def get_fundamentals(self, symbol: str):
        contract = create_stock_contract(symbol)

        req_id = 400

        self.client.fundamental_done[req_id] = False

        self.client.reqFundamentalData(
            reqId=req_id,
            contract=contract,
            reportType="ReportSnapshot",
            fundamentalDataOptions=[]
        )

        while not self.client.fundamental_done.get(req_id, False):
            time.sleep(0.1)

        xml_data = self.client.fundamental_data[req_id]

        parsed = extract_fundamentals(xml_data)

        return parsed

    # -------------------------
    # scanners
    # -------------------------
    def scan_top_volume_us_major(self, num_results=5):
        sub = ScannerSubscription()

        sub.instrument = "STK"
        sub.locationCode = "STK.US.MAJOR"
        sub.scanCode = "HOT_BY_VOLUME"

        req_id = 300

        # reset state
        self.client.scanner_data = []
        self.client.scanner_done = False

        self.client.reqScannerSubscription(
            reqId=req_id,
            subscription=sub,
            scannerSubscriptionOptions=[],
            scannerSubscriptionFilterOptions=[]
        )

        # wait for completion
        while not self.client.scanner_done:
            time.sleep(0.1)

        # cancel scanner
        self.client.cancelScannerSubscription(req_id)

        results = self.client.scanner_data[:num_results]
        
        if results:
            print("\nTop Stocks by Volume:\n")
            print(tabulate(results, headers="keys", tablefmt="fancy_grid"))

        return results

    
    def scan_top_percent_gainers_us_major(self, num_results=5):
        sub = ScannerSubscription()

        sub.instrument = "STK"
        sub.locationCode = "STK.US.MAJOR"
        sub.scanCode = "TOP_PERC_GAIN"

        req_id = 300

        # reset state
        self.client.scanner_data = []
        self.client.scanner_done = False

        self.client.reqScannerSubscription(
            reqId=req_id,
            subscription=sub,
            scannerSubscriptionOptions=[],
            scannerSubscriptionFilterOptions=[]
        )

        # wait for completion
        while not self.client.scanner_done:
            time.sleep(0.1)

        # cancel scanner
        self.client.cancelScannerSubscription(req_id)

        results = self.client.scanner_data[:num_results]
        if results:
            print("\nTop Gainers:\n")
            print(tabulate(results, headers="keys", tablefmt="fancy_grid"))

        return results
    

    def scan_top_percent_losers_us_major(self, num_results=5):
        sub = ScannerSubscription()

        sub.instrument = "STK"
        sub.locationCode = "STK.US.MAJOR"
        sub.scanCode = "TOP_PERC_LOSE"

        req_id = 300

        # reset state
        self.client.scanner_data = []
        self.client.scanner_done = False

        self.client.reqScannerSubscription(
            reqId=req_id,
            subscription=sub,
            scannerSubscriptionOptions=[],
            scannerSubscriptionFilterOptions=[]
        )

        # wait for completion
        while not self.client.scanner_done:
            time.sleep(0.1)

        # cancel scanner
        self.client.cancelScannerSubscription(req_id)

        results = self.client.scanner_data[:num_results]
        if results:
            print("\nTop Losers:\n")
            print(tabulate(results, headers="keys", tablefmt="fancy_grid"))

        return results

    def scan_top_rapid_movers_us_major(self, num_results=5):
        sub = ScannerSubscription()

        sub.instrument = "STK"
        sub.locationCode = "STK.US.MAJOR"
        sub.scanCode = "HOT_BY_PRICE"

        req_id = 300

        # reset state
        self.client.scanner_data = []
        self.client.scanner_done = False

        self.client.reqScannerSubscription(
            reqId=req_id,
            subscription=sub,
            scannerSubscriptionOptions=[],
            scannerSubscriptionFilterOptions=[]
        )

        # wait for completion
        while not self.client.scanner_done:
            time.sleep(0.1)

        # cancel scanner
        self.client.cancelScannerSubscription(req_id)

        results = self.client.scanner_data[:num_results]
        if results:
            print("\nTop Hot Stocks:\n")
            print(tabulate(results, headers="keys", tablefmt="fancy_grid"))

        return results
    
    # -------------------------
    # Placing Orders
    # -------------------------
    def place_order(self, symbol: str, action: str, quantity: int, order_type="MKT", price=None):
        contract = create_stock_contract(symbol)

        order_id = self.client.next_order_id

        if order_id is None:
            raise Exception("Order ID not initialized")

        # Build order
        if order_type == "MKT":
            order = market_order(action, quantity)
        elif order_type == "LMT":
            if price is None:
                raise ValueError("Limit price required")
            order = limit_order(action, quantity, price)
        else:
            raise ValueError("Unsupported order type")

        # Reset state
        self.client.order_done = False

        # Place order
        self.client.placeOrder(order_id, contract, order)

        # Increment ID
        if self.client.next_order_id is not None:
            self.client.next_order_id += 1

        # Wait for completion
        while not self.client.order_done:
            time.sleep(0.1)

        return self.client.order_status.get(order_id)
    
