from api.constants import URL_API, TOKEN
import pandas as pd
import requests
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