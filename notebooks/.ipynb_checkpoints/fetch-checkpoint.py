import requests
import pandas as pd
import json

def fetch_timeseries(url):
    response = requests.get(url)
    response

    data = json.loads(response.content.decode())

    dfs = []
    for country, items in data.items():
        dfs.append(pd.DataFrame(items).assign(country=country))

    df = (pd.concat(dfs)
          .assign(date=lambda f: pd.to_datetime(f['date']))
          .set_index(['country', 'date'])
         )
    return df

TS_URL = 'https://pomber.github.io/covid19/timeseries.json'
