import pandas as pd
import logging as lg
from pytrends.request import TrendReq


def read_from_csv(csvfile, sep=';', encoding='UTF-8'):
    """ 
    Read csv containing the following columns : 'cnat_code', 'kw',
    'cat', 'label'. Relies on pandas.read_csv.

    Returns
    -------
    A dict with cnat_code (french sectors codes) as keys and pandas
    DataFrames (containing keywords, categories and labels) as values.
    """
    df = pd.read_csv(csvfile, sep=sep, encoding=encoding)

    if any(df.columns != ['cnat_code', 'kw', 'cat', 'label']):
        raise ValueError('csv file must contain the following columns:',
        'cnat_code, kw, cat, label')

    if df.isnull().values.any():
        raise ValueError("csv file contains missing values.")

    dict_kw = {sect: df for sect, df in df.groupby(by=["cnat_code"])}
    return dict_kw


def download_gtrends(d, timeframe="all", geo="FR"):
    dict_dfs = {}
    pytrends = TrendReq()
    for sect, df in d.items():
        l = []
        for kw, cat in zip(df["kw"], df["cat"]):
            try:
                pytrends.build_payload(
                    [kw], cat=cat, timeframe=timeframe, geo=geo, gprop=''
                )
                gtrends = pytrends.interest_over_time()
                l.append(gtrends)
                dict_dfs[sect] = pd.concat(l, axis=1).drop(
                    labels=["isPartial"], axis=1
                )
            except ResponseError:
                lg.warning(f"Download failed for {kw}. Check your keyword.")
    return dict_dfs
