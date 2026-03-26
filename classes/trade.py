from datetime import datetime

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

    def __init__(
        self,
        asset: str,
        currency: str,
        symbol: str,
        date: datetime,
        quantity: int,
        proceeds: float,
        comm_fee: float,
        rate: float,
        proceeds_in_PLN: float,
        comm_in_PLN: float
    ):
        self.asset = asset
        self.currency = currency
        self.symbol = symbol
        self.date = date
        self.quantity = quantity
        self.proceeds = proceeds
        self.comm_fee = comm_fee
        self.rate = rate
        self.proceeds_in_PLN = proceeds_in_PLN
        self.comm_in_PLN = comm_in_PLN

