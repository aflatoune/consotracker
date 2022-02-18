import pandas as pd
import logging as lg
from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError
from dbnomics import fetch_series


def download_gtrends(dict_kw, timeframe="all", geo="FR"):
    dict_dfs = {}
    pytrends = TrendReq()
    for sect, subdict in dict_kw.items():
        l = []
        for subsubdict in subdict.values():
            kw = subsubdict["kw"]
            cat = subsubdict["cat"]
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
    for sect, subdict in dict_dbcodes.items():
        dataset_code = subdict["dataset_code"]
        serie_code = subdict["serie_code"]
        try:
            dict_series[sect] = fetch_series(
                'INSEE', dataset_code, serie_code)
        except ValueError:
            lg.warning(f'Download failed for {dataset_code}/{serie_code}.')

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
