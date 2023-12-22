from core.models.stock_data_dict import StockDataDict


class ExchangeRestApi(object):
    def __init__(self):
        pass

    def get_ohlcv(self, market: str, time_frame: int, limit: int, start_time: int) -> [StockDataDict]:
        raise NotImplementedError("get_ohlcv_data method must be override")
