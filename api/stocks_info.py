from api.constants import URL_API, TOKEN, URL_API_BRAPI, TOKEN_BRAPI
from data.select import select_table
import pandas as pd
import requests
from re import sub
from json import loads
from time import sleep

def get_indexes(date_init, date_end):
    url = URL_API + f"tickers/IBOV/quotes?period_init={date_init}&period_end={date_end}"
    headers = {'Authorization': 'Bearer ' + TOKEN}
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        print(f'problem in api: ibov {response.status_code}: {response.text}')
        return None
    response = loads(response.content)
    ibov = pd.DataFrame(response)
    ibov = ibov[['date', 'close']]
    ibov.rename(columns={'close': 'ibov'}, inplace=True)

    sleep(1)
    url = URL_API + "macro/selic"
    headers = {'Authorization': 'Bearer ' + TOKEN}
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        print(f'problem in api: macro-selic {response.status_code}: {response.text}')
        return None
    response = loads(response.content)
    selic = pd.DataFrame(response)
    selic = selic[['date', 'value']]
    selic = selic[(selic['date'] >= date_init) & (selic['date'] <= date_end)]
    selic.rename(columns={'value': 'selic'}, inplace=True)

    sleep(1)
    url = URL_API + "macro/ipca"
    headers = {'Authorization': 'Bearer ' + TOKEN}
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        print(f'problem in api: macro-ipca {response.status_code}: {response.text}')
        return None
    response = loads(response.content)
    ipca = pd.DataFrame(response)
    ipca = ipca[['date', 'value']]
    ipca = ipca[(ipca['date'] >= date_init) & (ipca['date'] <= date_end)]
    ipca.rename(columns={'value': 'ipca'}, inplace=True)

    sleep(1)
    market = pd.merge(ibov, selic, on='date', how='outer').reset_index(drop=True)
    market = pd.merge(market, ipca, on='date', how='outer').reset_index(drop=True)
    market.sort_values(by=['date'], ignore_index=True, ascending=False, inplace=True)
    return market

def fix_stock_name(stocks_df):
    replacements = {
        'ENGIE BRASILON NM': 'ENGIE BRASIL ON NM',
        'TRAN PAULISTPN N1': 'TRAN PAULIST PN N1',
        'ITAUUNIBANCOPN N1': 'ITAUUNIBANCO PN N1'
    }
    stocks_df['b3_name'] = stocks_df['b3_name'].replace(replacements)
    return stocks_df

def get_stocks():
    url = URL_API + "tickers"
    headers = {'Authorization': 'Bearer ' + TOKEN}
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        print(f'problem in api: tickers {response.status_code}: {response.text}')
        return None
    response = loads(response.content)
    stocks_list = pd.DataFrame(response)
    columns = ['type', 'market_type', 'market', 'isin', 'issuer_code', 'ticker', 'name']
    stocks_list = stocks_list[columns]
    stocks_list = stocks_list[stocks_list['type'].isin(['stock', 'unit'])]

    stocks_tickers = stocks_list['ticker'].tolist()
    columns = ['shortName', 'longName', 'symbol']
    company_names = pd.DataFrame(columns=columns)
    for i in stocks_tickers:
        url = URL_API_BRAPI + "quote/" + i
        headers = {'Authorization': 'Bearer ' + TOKEN_BRAPI}
        response = requests.request("GET", url, headers=headers)
        if response.status_code != 200:
            continue
        response = loads(response.content)['results'][0]
        company = pd.DataFrame([response])
        if 'shortName' in company:
            company_names = pd.concat(objs=[company_names, company[columns]], ignore_index=True)
    stocks = pd.merge(left=stocks_list, right=company_names, how='left', left_on='ticker', right_on='symbol')
    stocks.drop('symbol', axis=1, inplace=True)
    stocks.rename(columns={'shortName': 'b3_name', 'longName': 'long_name'}, inplace=True)
    stocks['b3_name'] = stocks['b3_name'].apply(lambda x: sub(r' +', ' ', x) if not pd.isna(x) else x)
    stocks = fix_stock_name(stocks)

    url = URL_API + "companies"
    headers = {'Authorization': 'Bearer ' + TOKEN}
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        print(f'problem in api: companies {response.status_code}: {response.text}')
        return None
    response = loads(response.content)
    companies_info = pd.DataFrame(response)
    columns = [
        'cvm_code', 'b3_listing_segment', 'b3_segment', 'b3_issuer_code', 
        'b3_sector', 'b3_subsector', 'main_activity','is_b3_listed',
        'is_foreign', 'is_state_owned', 'name'
    ]
    companies_info = companies_info[columns]

    stocks = pd.merge(left=stocks, right=companies_info, how='left', left_on='issuer_code', right_on='b3_issuer_code')
    stocks.drop(['name_y', 'b3_issuer_code'], axis=1, inplace=True)
    stocks.rename(columns={'name_x': 'name'}, inplace=True)
    stocks.sort_values(by=['issuer_code', 'ticker'], ascending=True, ignore_index=True, inplace=True)
    return stocks

def get_stocks_dividend():
    stock_dividends = select_table('Operation')
    stock_dividends = stock_dividends['stock_name'].unique().tolist()
    cvm_codes = select_table('Stock')
    cvm_codes = cvm_codes[cvm_codes['b3_name'].isin(stock_dividends)]
    cvm_codes = cvm_codes['cvm_code'].to_list()
    cvm_codes = [int(num) for num in cvm_codes]

    columns = [
        'payable_date', 'record_date', 'cvm_code',
        'type', 'ticker', 'amount'
    ]
    headers = {'Authorization': 'Bearer ' + TOKEN}
    dividends = pd.DataFrame(columns=columns)
    for i in cvm_codes:
        url = URL_API + "companies/" + str(i) + "/dividends"
        sleep(1)
        response = requests.request("GET", url, headers=headers)
        if response.status_code != 200:
            print(f'problem in api: companies_dividends {response.status_code}: {response.text}')
            continue
        response = loads(response.content)
        each_dividends = pd.DataFrame(response)
        dividends = pd.concat(objs=[dividends, each_dividends[columns]], ignore_index=True)
    dividends.sort_values(by=['record_date', 'payable_date', 'ticker', 'type'], inplace=True, ignore_index=True, ascending=False)
    return dividends
