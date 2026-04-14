from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibkr_mcp.utils.fundamentals import extract_fundamentals
import threading
import logging
from tabulate import tabulate
from queue import Queue

logger = logging.getLogger(__name__)


class IBClient(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

        self.next_order_id = None
        self.order_status = {}
        self.order_done = False
        self.callback_error = {}

        # Queues for responses
        self.account_queue = Queue()
        self.contract_queue = Queue()
        self.pnl_queue = Queue()
        self.hist_data_queue = Queue()
        self.market_data_queue = Queue()

        self.acc_summary = []
        self.pnl_summary = []
        self.hist_data = []
        self.hist_data_done = False
        self.market_data = {}

        self.scanner_data = []
        self.scanner_done = False

        self.fundamental_data = {}
        self.fundamental_done = {}


    # -------------------------
    # Connection
    # -------------------------
    def nextValidId(self, orderId: int):
        logger.info(f"Next valid order id: {orderId}")
        self.next_order_id = orderId

    # -------------------------
    # Order Callback
    # -------------------------
    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice,
                    permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):

        self.order_status[orderId] = {
            "status": status,
            "filled": filled,
            "remaining": remaining,
            "avgFillPrice": avgFillPrice
        }

        if status in ["Filled", "Cancelled", "Inactive"]:
            self.order_done = True

    # -------------------------
    # error callback
    # -------------------------
    def error(self, reqId, errorCode, errorString):
        # Capture historical + fundamentals errors
        if reqId != -1:
            print("{} : {}".format(errorCode,errorString))
            self.callback_error[reqId] = (errorCode, errorString)
            self.fundamental_done[reqId] = True
            self.hist_data_done = True
            self.order_done = True

    # -------------------------
    # Account Info
    # -------------------------
    def accountSummary(self, reqId, account, tag, value, currency):
        #print("Account : {}, Tag : {}, Value : {}, Currency : {}".format(account,tag,value,currency))
        row = {
            "ReqId": reqId,
            "Account": account,
            "Tag": tag,
            "Value": value,
            "Currency": currency
        }
        self.account_queue.put(row)
        self.acc_summary.append(row)

    def accountSummaryEnd(self, reqId):
        print("\nAccount Summary:\n")
        print(tabulate(self.acc_summary, headers="keys"))

    # -------------------------
    # PnL Info
    # -------------------------
    def pnl(self, reqId, dailyPnL, unrealizedPnL, realizedPnL):
        print("DailyPnL : {}, UnrealizedPnL : {}, RealizedPnL : {}".format(dailyPnL,unrealizedPnL,realizedPnL))
        self.pnl_queue.put({
            "ReqId": reqId,
            "DailyPnL": dailyPnL,
            "UnrealizedPnL": unrealizedPnL,
            "RealizedPnL": realizedPnL
        })

    # -------------------------
    # Contract Details
    # -------------------------
    def contractDetails(self, reqId, contractDetails):
        print("contract:{}".format(contractDetails))
        self.contract_queue.put(contractDetails)

    def contractDetailsEnd(self, reqId):
        self.contract_queue.put("END")

    # -------------------------
    # Historical Data
    # -------------------------
    def historicalData(self, reqId, bar):
        row = {
            "ReqId": reqId,
            "date": bar.date,
            "open": bar.open,
            "high": bar.high,
            "low": bar.low,
            "close": bar.close,
            "volume": bar.volume
        }
        self.hist_data_queue.put(row)
        self.hist_data.append(row)

    def historicalDataEnd(self, reqId, start, end):
        self.hist_data_done = True
        print("\nHistorical Data from {} to {}:\n".format(start, end))
        print(tabulate(self.hist_data, headers="keys"))

    # -------------------------
    # Streaming Data
    # -------------------------
    def tickPrice(self, reqId, tickType, price, attrib):
        # Only process last traded price
        if tickType == 4:  # LAST price
            self.market_data[reqId] = price

            self.market_data_queue.put({
                "reqId": reqId,
                "price": price
            })


    # -------------------------
    # Global Scanners
    # -------------------------
    def scannerData(self, reqId, rank, contractDetails, distance, benchmark, projection, legsStr):
        row = {
            "rank": rank,
            "symbol": contractDetails.contract.symbol,
            "secType": contractDetails.contract.secType,
            "exchange": contractDetails.contract.exchange
        }

        self.scanner_data.append(row)


    def scannerDataEnd(self, reqId):
        self.scanner_done = True
        # print("\nScanner Output:\n")
        # print(tabulate(self.scanner_data, headers="keys"))

    # -------------------------
    # Fundamental Data
    # -------------------------
    def fundamentalData(self, reqId, data):
        self.fundamental_data[reqId] = data
        self.fundamental_done[reqId] = True
        # result = extract_fundamentals(data)
        # print(tabulate(result.items(), headers=["Field", "Value"], tablefmt="simple"))


class IBConnection:
    def __init__(self, host="127.0.0.1", port=7497, client_id=1):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.client = IBClient()
        self.thread = None

    def connect(self):
        logger.info("Connecting to IBKR TWS...")
        self.client.connect(self.host, self.port, self.client_id)

        self.thread = threading.Thread(target=self.client.run, daemon=True)
        self.thread.start()

    def disconnect(self):
        logger.info("Disconnecting from IBKR...")
        self.client.disconnect()

    def is_connected(self):
        return self.client.isConnected()