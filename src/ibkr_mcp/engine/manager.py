import logging

logger = logging.getLogger(__name__)


class StrategyManager:
    def __init__(self):
        self.runners = {}

    def start_strategy(self, name, runner):
        logger.info(f"Starting strategy: {name}")
        self.runners[name] = runner
        runner.start()

    def stop_strategy(self, name):
        if name in self.runners:
            logger.info(f"Stopping strategy: {name}")
            self.runners[name].stop()
            del self.runners[name]

    def list_strategies(self):
        return list(self.runners.keys())