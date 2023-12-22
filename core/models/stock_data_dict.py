from typing import TypedDict


class StockDataDict(TypedDict):
    """stock data dict"""

    id: int
    time: int
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float
