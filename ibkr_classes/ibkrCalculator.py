from collections import deque
from ibkr_classes.ibkrPortfolio import IbkrPortfolio

class IbkrCalculator:

    @staticmethod
    def calculate_proceeds_by_symbol(portfolio: IbkrPortfolio, year: int) -> dict[str, float]:
        results = {}

        for symbol, position in portfolio.positions.items():
            long_queue = deque()
            short_queue = deque()
            realized_pln = 0.0

            for trade in position.trades:
                if trade.date is None or trade.date.year > year:
                    continue

                asset = str(trade.asset).strip()
                signed_qty = float(trade.quantity)

                if signed_qty == 0:
                    continue

                proceeds_pln = float(trade.proceeds_in_PLN)
                comm_pln = float(trade.comm_in_PLN)
                net_cash_pln = proceeds_pln + comm_pln
                abs_qty = abs(signed_qty)
                unit_value = abs(net_cash_pln) / abs_qty

                # STOCK
                if asset == "Stocks":
                    if signed_qty > 0:
                        remaining_qty = signed_qty

                        while remaining_qty > 0 and short_queue:
                            oldest_short = short_queue[0]
                            matched_qty = min(remaining_qty, oldest_short["qty"])

                            realized = matched_qty * oldest_short["unit_credit"] - matched_qty * unit_value

                            if trade.date.year == year:
                                realized_pln += realized

                            oldest_short["qty"] -= matched_qty
                            remaining_qty -= matched_qty

                            if oldest_short["qty"] <= 1e-12:
                                short_queue.popleft()

                        if remaining_qty > 0:
                            long_queue.append({
                                "qty": remaining_qty,
                                "unit_cost": unit_value
                            })

                    else:
                        remaining_qty = abs(signed_qty)

                        while remaining_qty > 0 and long_queue:
                            oldest_long = long_queue[0]
                            matched_qty = min(remaining_qty, oldest_long["qty"])

                            realized = matched_qty * unit_value - matched_qty * oldest_long["unit_cost"]

                            if trade.date.year == year:
                                realized_pln += realized

                            oldest_long["qty"] -= matched_qty
                            remaining_qty -= matched_qty

                            if oldest_long["qty"] <= 1e-12:
                                long_queue.popleft()

                        if remaining_qty > 0:
                            short_queue.append({
                                "qty": remaining_qty,
                                "unit_credit": unit_value
                            })

                # OPTIONS
                elif asset == "Equity and Index Options":
                    if signed_qty < 0:
                        remaining_qty = abs(signed_qty)

                        while remaining_qty > 0 and long_queue:
                            oldest_long = long_queue[0]
                            matched_qty = min(remaining_qty, oldest_long["qty"])

                            realized = matched_qty * unit_value - matched_qty * oldest_long["unit_cost"]

                            if trade.date.year == year:
                                realized_pln += realized

                            oldest_long["qty"] -= matched_qty
                            remaining_qty -= matched_qty

                            if oldest_long["qty"] <= 1e-12:
                                long_queue.popleft()

                        if remaining_qty > 0:
                            short_queue.append({
                                "qty": remaining_qty,
                                "unit_credit": unit_value
                            })

                    else:
                        remaining_qty = signed_qty

                        while remaining_qty > 0 and short_queue:
                            oldest_short = short_queue[0]
                            matched_qty = min(remaining_qty, oldest_short["qty"])

                            realized = matched_qty * oldest_short["unit_credit"] - matched_qty * unit_value

                            if trade.date.year == year:
                                realized_pln += realized

                            oldest_short["qty"] -= matched_qty
                            remaining_qty -= matched_qty

                            if oldest_short["qty"] <= 1e-12:
                                short_queue.popleft()

                        if remaining_qty > 0:
                            long_queue.append({
                                "qty": remaining_qty,
                                "unit_cost": unit_value
                            })

                else:
                    raise ValueError(
                        f"Nieobsługiwany asset '{asset}' dla symbolu {symbol} w dniu {trade.date}."
                    )

            results[symbol] = round(realized_pln, 2)

        return results


    @staticmethod
    def calculate_total_proceeds(portfolio, year: int) -> float:
        by_symbol = IbkrCalculator.calculate_proceeds_by_symbol(portfolio, year)
        return round(sum(by_symbol.values()), 2)