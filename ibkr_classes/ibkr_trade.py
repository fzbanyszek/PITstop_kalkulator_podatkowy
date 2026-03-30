from dataclasses import dataclass
from datetime import datetime

@dataclass
class Trade:
    asset: str
    currency: str
    symbol: str
    date: datetime
    quantity: int
    proceeds: float
    comm_fee: float
    rate: float
    proceeds_in_PLN: float
    comm_in_PLN: float

    def __repr__(self):
        return (
            f"Trade("
            f"symbol={self.symbol}, "
            f"asset={self.asset}, "
            f"currency={self.currency}, "
            f"date={self.date}, "
            f"quantity={self.quantity}, "
            f"proceeds={self.proceeds}, "
            f"comm_fee={self.comm_fee}, "
            f"rate={self.rate}, "
            f"proceeds_pln={self.proceeds_in_PLN}, "
            f"comm_pln={self.comm_in_PLN}"
            f")"
        )