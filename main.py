from classes.ibkr_portfolio import Portfolio

p1 = Portfolio('ibkr_data.csv', 'ibkr_data2.csv')
p1.load_portfolio_csv('merged.csv')
p1.createPositions()