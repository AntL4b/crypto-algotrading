import logging
import time

from core.exchange_api.kraken.kraken_rest_api import KrakenRestApi
from core.stock_data_acquisition.crypto_pair_manager import CryptoPairManager
from core.strategy.strategy import Strategy


class DummyStrategy(Strategy):
    """The dummy strategy"""

    def __init__(self):
        """The dummy strategy constructor"""

        logging.info("DummyStrategy run strategy")
        super(DummyStrategy, self).__init__()
        self.api = KrakenRestApi()
        self.btcusd_manager: CryptoPairManager = CryptoPairManager("PF_XBTUSD", self.api)
        self.btcusd_manager.add_time_frame(60)
        self.btcusd_manager.start_all_time_frame_acq()

    def before_loop(self) -> None:
        pass

    def loop(self) -> None:
        """The strategy core"""
        logging.info("Looping")

        btcusd_stock_data_manager = self.btcusd_manager.get_time_frame(60).stock_data_manager
        if len(btcusd_stock_data_manager.stock_data_list) > 20:
            atr14 = btcusd_stock_data_manager.stock_indicators["atr_14"]
            logging.info("atr_14")
            logging.info(atr14.iloc[-1])

    def after_loop(self) -> None:
        time.sleep(5)

    def cleanup(self) -> None:
        """Clean strategy execution"""
        logging.info("DummyStrategy cleanup")
