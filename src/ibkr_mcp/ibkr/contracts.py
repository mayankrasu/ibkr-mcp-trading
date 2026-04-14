from ibapi.contract import Contract


def create_stock_contract(symbol: str, exchange="SMART", currency="USD"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.exchange = exchange
    contract.currency = currency
    return contract