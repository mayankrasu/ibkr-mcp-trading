import threading
from queue import Queue
import logging

logger = logging.getLogger(__name__)


class StrategyRunner:
    def __init__(self, strategy, data_source=None):
        self.strategy = strategy
        self.data_queue = Queue()
        self.running = False

        self.data_thread = None
        self.strategy_thread = None

    def start(self):
        logger.info("Starting strategy runner...")
        self.running = True

        self.data_thread = threading.Thread(target=self._data_loop, daemon=True)
        self.strategy_thread = threading.Thread(target=self._strategy_loop, daemon=True)

        self.data_thread.start()
        self.strategy_thread.start()

        self.strategy.on_start()

    def stop(self):
        logger.info("Stopping strategy runner...")
        self.running = False
        self.strategy.on_stop()

    def _data_loop(self):
        # Placeholder — later connect IBKR market data here
        import time
        price = 100

        while self.running:
            price += 1  # fake data
            self.data_queue.put(price)
            time.sleep(1)

    def _strategy_loop(self):
        while self.running:
            data = self.data_queue.get()
            self.strategy.on_data(data)