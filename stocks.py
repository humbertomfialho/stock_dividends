from api.stocks_info import get_stocks, get_indexes, get_stocks_dividend
from data.insert import insert_values
from data.select import select_table

date_range = select_table('Negotiation')
date_range.sort_values(by='date', ignore_index=True, inplace=True)
first_date = date_range['date'].iloc[0][:10]
last_date = date_range['date'].iloc[-1][:10]
index = get_indexes(first_date, last_date)
insert_values(index, 'Market')

stock = get_stocks()
insert_values(stock, 'Stock')

dividends = get_stocks_dividend()
insert_values(dividends, 'Dividends')
