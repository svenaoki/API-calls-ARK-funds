import pandas as pd
import numpy as np
import requests
import io


def making_pretty(mydictionary):
    df = pd.DataFrame.from_dict(mydictionary, orient='index')
    df = df.reset_index().rename(
        columns={'index': 'Company', 0: 'Market Value Share'})
    df.sort_values(by='Market Value Share', axis=0,
                   ascending=False, inplace=True)
    total_value = np.sum(df['Market Value Share'])
    df['% Share'] = np.round(df['Market Value Share']/total_value*100, 2)
    df.reset_index(drop=True, inplace=True)
    return df


def get_markets_shares(list_of_funds):
    mydict = {}
    for fund in list_of_funds:
        src = requests.get(fund)
        if src.ok:
            data = src.content.decode('utf8')
            data = pd.read_csv(io.StringIO(data))
            data.dropna(axis=0, inplace=True)
            data = data.filter(['company', 'market value($)', 'ticker'])
            for company in data['company']:
                if company in mydict.keys():
                    market_value = data[data['company']
                                        == company]['market value($)'].values
                    mydict[company] += int(market_value[0])
                else:
                    market_value = data[data['company']
                                        == company]['market value($)'].values
                    mydict[company] = int(market_value[0])

    dataframe = making_pretty(mydict)
    return dataframe


ark_etfs = [
    'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv',
    'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_AUTONOMOUS_TECHNOLOGY_&_ROBOTICS_ETF_ARKQ_HOLDINGS.csv',
    'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS.csv',
    'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_GENOMIC_REVOLUTION_MULTISECTOR_ETF_ARKG_HOLDINGS.csv',
    'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS.csv'
]


overview = get_markets_shares(ark_etfs)
print(overview)
