from ibkr_classes.ibkr_trade import Trade

class Position:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.trades = []

    def add_trade(self, trade):
        self.trades.append(trade)

    def __repr__(self):
        trades_str = "\n  ".join(repr(t) for t in self.trades)
        return f"Position(symbol={self.symbol}):\n  {trades_str}\n\n\n"