from core.exchange_api.exchange_rest_api import ExchangeRestApi
from core.models.stock_data_dict import StockDataDict


class KrakenRestApi(ExchangeRestApi):

    def __init__(self):
        super(KrakenRestApi, self).__init__()

    def get_ohlcv(self, market: str, time_frame: int, limit: int, start_time: int) -> [StockDataDict]:
        # TODO
        pass
