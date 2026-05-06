from collections import deque

from ibkr_classes.ibkrPortfolio import IbkrPortfolio


class IbkrCalculator:

    @staticmethod
    def calculate_year_summary(portfolio: IbkrPortfolio, year: int) -> dict:
        by_symbol = {}
        total_profit = 0.0
        total_revenue = 0.0
        total_cost = 0.0

        for symbol, position in portfolio.positions.items():
            long_queue = deque()
            short_queue = deque()
            realized_pln = 0.0
            revenue_pln = 0.0
            cost_pln = 0.0

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

                if asset == "Stocks":
                    if signed_qty > 0:
                        remaining_qty = signed_qty

                        while remaining_qty > 0 and short_queue:
                            oldest_short = short_queue[0]
                            matched_qty = min(remaining_qty, oldest_short["qty"])

                            matched_revenue = matched_qty * oldest_short["unit_credit"]
                            matched_cost = matched_qty * unit_value

                            if trade.date.year == year:
                                revenue_pln += matched_revenue
                                cost_pln += matched_cost
                                realized_pln += matched_revenue - matched_cost

                            oldest_short["qty"] -= matched_qty
                            remaining_qty -= matched_qty

                            if oldest_short["qty"] <= 1e-12:
                                short_queue.popleft()

                        if remaining_qty > 0:
                            long_queue.append({
                                "qty": remaining_qty,
                                "unit_cost": unit_value,
                            })

                    else:
                        remaining_qty = abs(signed_qty)

                        while remaining_qty > 0 and long_queue:
                            oldest_long = long_queue[0]
                            matched_qty = min(remaining_qty, oldest_long["qty"])

                            matched_revenue = matched_qty * unit_value
                            matched_cost = matched_qty * oldest_long["unit_cost"]

                            if trade.date.year == year:
                                revenue_pln += matched_revenue
                                cost_pln += matched_cost
                                realized_pln += matched_revenue - matched_cost

                            oldest_long["qty"] -= matched_qty
                            remaining_qty -= matched_qty

                            if oldest_long["qty"] <= 1e-12:
                                long_queue.popleft()

                        if remaining_qty > 0:
                            short_queue.append({
                                "qty": remaining_qty,
                                "unit_credit": unit_value,
                            })

                elif asset == "Equity and Index Options":
                    if signed_qty < 0:
                        remaining_qty = abs(signed_qty)

                        while remaining_qty > 0 and long_queue:
                            oldest_long = long_queue[0]
                            matched_qty = min(remaining_qty, oldest_long["qty"])

                            matched_revenue = matched_qty * unit_value
                            matched_cost = matched_qty * oldest_long["unit_cost"]

                            if trade.date.year == year:
                                revenue_pln += matched_revenue
                                cost_pln += matched_cost
                                realized_pln += matched_revenue - matched_cost

                            oldest_long["qty"] -= matched_qty
                            remaining_qty -= matched_qty

                            if oldest_long["qty"] <= 1e-12:
                                long_queue.popleft()

                        if remaining_qty > 0:
                            short_queue.append({
                                "qty": remaining_qty,
                                "unit_credit": unit_value,
                            })

                    else:
                        remaining_qty = signed_qty

                        while remaining_qty > 0 and short_queue:
                            oldest_short = short_queue[0]
                            matched_qty = min(remaining_qty, oldest_short["qty"])

                            matched_revenue = matched_qty * oldest_short["unit_credit"]
                            matched_cost = matched_qty * unit_value

                            if trade.date.year == year:
                                revenue_pln += matched_revenue
                                cost_pln += matched_cost
                                realized_pln += matched_revenue - matched_cost

                            oldest_short["qty"] -= matched_qty
                            remaining_qty -= matched_qty

                            if oldest_short["qty"] <= 1e-12:
                                short_queue.popleft()

                        if remaining_qty > 0:
                            long_queue.append({
                                "qty": remaining_qty,
                                "unit_cost": unit_value,
                            })

                else:
                    raise ValueError(
                        f"Nieobsługiwany asset '{asset}' dla symbolu {symbol} w dniu {trade.date}."
                    )

            by_symbol[symbol] = {
                "profit": round(realized_pln, 2),
                "revenue": round(revenue_pln, 2),
                "cost": round(cost_pln, 2),
            }
            total_profit += realized_pln
            total_revenue += revenue_pln
            total_cost += cost_pln

        return {
            "by_symbol": by_symbol,
            "total_profit": round(total_profit, 2),
            "total_revenue": round(total_revenue, 2),
            "total_cost": round(total_cost, 2),
        }

    @staticmethod
    def calculate_proceeds_by_symbol(portfolio: IbkrPortfolio, year: int) -> dict[str, float]:
        summary = IbkrCalculator.calculate_year_summary(portfolio, year)
        return {
            symbol: values["profit"]
            for symbol, values in summary["by_symbol"].items()
        }

    @staticmethod
    def calculate_total_proceeds(portfolio: IbkrPortfolio, year: int) -> float:
        summary = IbkrCalculator.calculate_year_summary(portfolio, year)
        return summary["total_profit"]

    @staticmethod
    def calculate_total_revenue(portfolio: IbkrPortfolio, year: int) -> float:
        summary = IbkrCalculator.calculate_year_summary(portfolio, year)
        return summary["total_revenue"]

    @staticmethod
    def calculate_total_cost(portfolio: IbkrPortfolio, year: int) -> float:
        summary = IbkrCalculator.calculate_year_summary(portfolio, year)
        return summary["total_cost"]
