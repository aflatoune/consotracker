import pandas as pd
import logging as lg
from csv import DictReader
from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError
from dbnomics import fetch_series


def read_kw_from_csv(csvfile, sep=';', encoding='UTF-8'):
    """
    Read csv containing the following columns : 'cnat_code', 'kw' (keyword),
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


def read_dbcode_from_csv(csvfile,
                         skip_first_row=True,
                         sep=';',
                         encoding='UTF-8'):
    """
    Read csv containing the sector codes as derived from the national accounts,
    and the corresponding series codes to be downloaded from DBnomics.

    Returns
    -------
    A dict with cnat_code (french sectors codes) as keys and codes to download
    series as values.
    """
    dict_dbcodes = {}
    reader = DictReader(open(csvfile, encoding=encoding), delimiter=sep,
                        fieldnames=["k", "v1", "v2", "v3"])

    if skip_first_row:
        headers = next(reader)

    for row in reader:
        dict_dbcodes.update({row["k"]: [row["v1"], row["v2"], row["v3"]]})
    return dict_dbcodes


def download_gtrends(dict_kw, timeframe="all", geo="FR"):
    dict_dfs = {}
    pytrends = TrendReq()
    for sect, df in dict_kw.items():
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


def download_dbseries(dict_dbcodes, start="2004-01-01"):
    """Download economic series

    Parameters
    ----------
    start {str} -- (default: {"2004-01-01"})
        Indicates the begining of the series (must be in YYYY/MM/DD format).
    """
    dict_series = {}
    for sect, codes in dict_dbcodes.items():
        dataset_code = codes[0]
        series_code = codes[1]
        try:
            dict_series[sect] = fetch_series(
                'INSEE', dataset_code, series_code)
        except ValueError:
            lg.warning(f'Download failed for {dataset_code}/{series_code}.')

    for sect, df in dict_series.items():
        if start is not None:
            dict_series[sect] = df[df["period"] >= start]["original_value"]
        else:
            dict_series[sect] = df["original_value"]

    return dict_series

def match_dict(d1, d2):
    """Filter two dictionnaries by keeping only common keys.

    Parameters
    ----------
    d1 {dict}

    d2 {dict}

    Returns
    -------
    Common keys between the dicitonnaries.
    """
    common_k = d1.keys() & d2.keys()
    for k1 in d1.copy().keys():
        if k1 not in common_k:
            d1.pop(k1)
    for k2 in d2.copy().keys():
        if k2 not in common_k:
            d2.pop(k2)
    return common_k