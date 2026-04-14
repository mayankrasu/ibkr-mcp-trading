from ibkr_mcp.engine.runner import StrategyRunner
from ibkr_mcp.engine.manager import StrategyManager
from ibkr_mcp.strategies.moving_average import MovingAverageStrategy

import time

if __name__ == "__main__":
    strategy = MovingAverageStrategy(window=3)
    runner = StrategyRunner(strategy)

    manager = StrategyManager()
    manager.start_strategy("ma_strategy", runner)

    time.sleep(10)

    manager.stop_strategy("ma_strategy")