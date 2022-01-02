import pandas as pd
import logging as lg
from pytrends.request import TrendReq


def read_from_csv(csvfile):
    df = pd.read_csv(csvfile, sep=";", encoding="UTF-8")
    d = {sect: df for sect, df in df.groupby(by=df.columns[0], axis=0)}
    return d


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
