from ibapi.order import Order


def market_order(action: str, quantity: int):
    order = Order()
    order.action = action  # BUY / SELL
    order.orderType = "MKT"
    order.totalQuantity = quantity
    order.eTradeOnly = False
    order.firmQuoteOnly = False
    return order


def limit_order(action: str, quantity: int, price: float):
    order = Order()
    order.action = action
    order.orderType = "LMT"
    order.totalQuantity = quantity
    order.lmtPrice = price
    order.eTradeOnly = False
    order.firmQuoteOnly = False
    return order