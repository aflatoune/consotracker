import logging as lg
import pandas as pd
from statsmodels.tsa.seasonal import STL


class Processing:
    '''Class for processing Google Trends interest over time.
    '''

    def __init__(
        self,
        base_date='2004-01-01',
        seasonality='stl',
        pct_change=False,
        lag_order=0
    ):
        '''
        Parameters
        ----------
        base_date {str} -- (default: {'2004-01-01'})
            Express the data wrt to this date. Set to None to keep the
            original data.

        seasonality {str} -- {'stl', 'yoy'}, (default: {'stl'})
            Method used to handle seasonality. Set to None to keep the
            original data.

            - 'stl': Deseasonalize the data using STL decomposition.
            - 'yoy': Deseasonalize the data by taking year-over-year
            difference.

        pct_change {bool} -- (default: {False})
            Computes the percentage change from the immediately previous row.
            Generated missing values are automatically dropped.

        lag_order {int} -- (default: {0})
            Whether to add or not lagged variable. If different from 0
            the data are augmented with lag of the chosen order.

        Notes
        -----
        Processing is performed in accordance with the order of the arguments.
        E.g.: if `seasonality=='stl'`, `pct_change=='True'` and
        `lag_order != 0`, lagged data are added after deseasonalization is
        performed and pct change computed.
        '''
        self.base_date = base_date
        self.seasonality = seasonality
        self.pct_change = pct_change
        self.lag_order = lag_order

    def fit(self, X):
        '''Implement processing

        Parameters
        ----------
        X {pandas.DataFrame}
            The input samples.

        Returns
        -------
        A processed pandas DataFrame.
        '''
        if self.base_date is not None:
            X = self._growth_wrt_date(X, self.base_date)
        if self.seasonality is not None:
            X = X.apply(self._deseasonalize, method=self.seasonality)
        if self.pct_change:
            X = self._to_growth_rate(X)
        if self.lag_order != 0:
            X = self._add_lag(X, order=self.lag_order)

        lg.info(f'Processed X has {X.shape[0]} rows and {X.shape[1]} columns')
        return X

    def _growth_wrt_date(self, X, date):
        def inner_growth(x, date=date):
            if x[date] == 0:
                x[date] = 1
                msg = (f'{date} value in {x.name} is equal to 0. The value has '
                       f'been set to 1 to avoid nan and infinite values')
                lg.warning(msg)
            return (x/x[date] - 1)*100
        return X.apply(inner_growth)

    def _deseasonalize(self, X, method):
        if method == 'stl':
            stl = STL(X, seasonal=13, robust=True)
            res = stl.fit()
            return res.trend
        elif method == 'yoy':
            if pd.infer_freq(X.index) in ['M', 'MS']:
                return X.diff(12).dropna()
            elif pd.infer_freq(X.index) in ['W']:
                return X.diff(52).dropna()

    def _to_growth_rate(self, X):
        X = (X/X.shift(1) - 1)*100
        return X.dropna()

    def _add_lag(self, X, order):
        X[[str(col) + '_lag' + str(order) for col in X.columns]] = X.apply(
            lambda x: x.shift(order), result_type='expand'
        )
        return X
