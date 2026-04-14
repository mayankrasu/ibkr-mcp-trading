from ibkr_mcp.engine.runner import StrategyRunner
from ibkr_mcp.engine.manager import StrategyManager
from ibkr_mcp.strategies.moving_average import MovingAverageStrategy

manager = StrategyManager()


def run_strategy(strategy_name: str, symbol: str, window: int = 5):
    if strategy_name == "moving_average":
        strategy = MovingAverageStrategy(window=window)
    else:
        raise ValueError("Unknown strategy")

    runner = StrategyRunner(strategy)

    manager.start_strategy(f"{strategy_name}_{symbol}", runner)

    return {"status": "started"}