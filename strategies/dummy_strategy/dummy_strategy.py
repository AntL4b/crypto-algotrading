import logging
import time

from core.strategy.strategy import Strategy


class DummyStrategy(Strategy):
    """The dummy strategy"""

    def __init__(self):
        """The dummy strategy constructor"""

        logging.info("DummyStrategy run strategy")
        super(DummyStrategy, self).__init__()

    def before_loop(self) -> None:
        pass

    def loop(self) -> None:
        """The strategy core"""
        logging.info("Looping")

    def after_loop(self) -> None:
        time.sleep(5)

    def cleanup(self) -> None:
        """Clean strategy execution"""
        logging.info("DummyStrategy cleanup")
