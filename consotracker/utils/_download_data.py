import pandas as pd
import logging as lg
import os
import json
from distutils.util import strtobool
from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError
from dbnomics import fetch_series

STREAMLIT_DOWNLOAD_INFO = strtobool(
    os.environ.get('STREAMLIT_DOWNLOAD_INFO', 'true'))
LEVEL = lg.INFO if STREAMLIT_DOWNLOAD_INFO == 'true' else None
lg.basicConfig(level=LEVEL)


class Download:
    def __init__(self, path_config, db=None):
        with open(os.path.join(path_config, "gtrends.json")) as f1:
            self.dict_kw = json.load(f1)
        with open(os.path.join(path_config, "dbnomics.json")) as f2:
            self.dict_dbcodes = json.load(f2)
        self.db = db

    def dl_data(self):
        self.match_dict(self.dict_kw, self.dict_dbcodes)
        dict_dfs = self.download_gtrends(self.dict_kw, redis_db=self.db, time=86400)
        dict_series = self.download_dbseries(self.dict_dbcodes, redis_db=self.db, time=86400)
        return dict_dfs, dict_series

    def check_db_key(self, redis_db, key):
        df = None
        if redis_db is not None:
            if redis_db.get(key) is not None:
                df = pd.read_json(redis_db.get(key))
                lg.info(f'Reading {key} sector in redis')
        return df

    def write_db_key(self, redis_db, key: str, value: pd.DataFrame, **kwargs):
        if redis_db:
            redis_db.setex(name=key,
                           time=kwargs.get('time', 100),
                           value=value.to_json())
            lg.info(f'Writing {key} sector in redis')

    def download_gtrends(
            self, dict_kw, timeframe="all", geo="FR", redis_db=None, **kwargs):
        dict_dfs = {}
        pytrends = TrendReq()

        for sect, subdict in dict_kw.items():
            l = []
            df = self.check_db_key(redis_db=redis_db, key=sect)

            if not isinstance(df, pd.DataFrame):
                for subsubdict in subdict.values():
                    kw = subsubdict["kw"]
                    cat = subsubdict["cat"]
                    try:
                        pytrends.build_payload([kw],
                                               cat=cat,
                                               timeframe=timeframe,
                                               geo=geo, gprop='')
                        gtrends = pytrends.interest_over_time()
                        l.append(gtrends)
                        lg.info(f'Download success for {kw}')
                    except ResponseError as e:
                        lg.warning(
                            f"Download failed for {kw}",
                            ". Check your keyword.")

                if l:
                    df = pd.concat(l, axis=1).drop(
                        labels=["isPartial"], axis=1)
                    self.write_db_key(redis_db=redis_db,
                                      key=sect,
                                      value=df,
                                      **kwargs)
                else:
                    df = pd.DataFrame([])
            dict_dfs[sect] = df

        return dict_dfs

    def download_dbseries(
            self, dict_dbcodes, start="2004-01-01", redis_db=None, **kwargs):
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

            df = self.check_db_key(redis_db=redis_db, key=sect + '_db')
            if not isinstance(df, pd.DataFrame):
                try:
                    df = fetch_series('INSEE',
                                      dataset_code,
                                      serie_code)
                    dict_series[sect] = df
                    lg.info(
                        f'Download success for {dataset_code}/{serie_code}.')
                    self.write_db_key(redis_db=redis_db,
                                      key=sect + '_db',
                                      value=df,
                                      **kwargs)
                except ValueError as e:
                    lg.warning(
                        f'Download failed for {dataset_code}',
                        f'/{serie_code}.')
            else:
                dict_series[sect] = df

        if not dict_series:
            return dict_series

        for sect, df in dict_series.items():
            df.set_index("period", drop=False, inplace=True)
            if start is not None:
                dict_series[sect] = df[pd.to_datetime(
                    df["period"]) >= start]["original_value"]
            else:
                dict_series[sect] = df["original_value"]

        return dict_series

    @staticmethod
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
