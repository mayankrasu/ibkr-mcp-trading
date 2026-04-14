from pydantic import BaseModel, Field
from typing import Literal


# -------------------------
# Strategy
# -------------------------
class RunStrategyArgs(BaseModel):
    strategy_name: Literal["moving_average"]
    symbol: str = Field(..., min_length=1)
    window: int = Field(default=5, ge=1, le=200)

# -------------------------
# Scanner
# -------------------------
class ScanMarketArgs(BaseModel):
    scan_type: Literal["volume", "gainers", "losers", "hot stocks"]
    num_results: int = 10

# -------------------------
# Historical Data
# -------------------------
class HistoricalDataArgs(BaseModel):
    symbol: str
    duration: str  # e.g. "3 M"
    candle_size: str  # e.g. "1 hour"

# -------------------------
# Market Data (stream)
# -------------------------
class MarketDataArgs(BaseModel):
    symbol: str

# -------------------------
# Fundamentals
# -------------------------
class FundamentalsArgs(BaseModel):
    symbol: str

# -------------------------
# Orders
# -------------------------
class PlaceOrderArgs(BaseModel):
    symbol: str
    action: Literal["BUY", "SELL"]
    quantity: int = Field(..., gt=0)
    order_type: Literal["MKT", "LMT"] = "MKT"
    price: float | None = None

# -------------------------
# Account / PnL
# -------------------------
class EmptyArgs(BaseModel):
    pass