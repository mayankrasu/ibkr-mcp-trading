from .base import BaseStrategy


class MovingAverageStrategy(BaseStrategy):
    def __init__(self, window=5):
        self.window = window
        self.prices = []

    def on_start(self):
        print("Moving Average Strategy started")

    def on_data(self, price):
        self.prices.append(price)

        if len(self.prices) > self.window:
            self.prices.pop(0)

            avg = sum(self.prices) / len(self.prices)
            print(f"Price: {price}, MA: {avg}")

            if price > avg:
                print("Signal: BUY")
            elif price < avg:
                print("Signal: SELL")

    def on_stop(self):
        print("Strategy stopped")