from statsmodels.tsa.seasonal import STL


class Processing:
    '''
    Class for Google Trends interest over time processing
    '''
    def __init__(self, base_date='2004-01-01', seasonality='stl', lag_order=0):
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

            lag_order {int} -- (default: {0})
            Whether to add or not lagged variable. If different from 0
            the data are augmented with lag of the chosen order.

        Notes
        -----
        Processing is performed in accordance with the order of the arguments.
        E.g.: `seasonality=='stl'` and `lag_order != 0`, lagged data are added
        after deseasonalization is performed. 
        '''
        self.base_date = base_date
        self.seasonality = seasonality
        self.lag_order = lag_order

    def fit(self, X):
        if self.base_date is not None:
            X = self._growth_wrt_date(X, self.base_date)
        if self.seasonality is not None:
            X = X.apply(self._deseasonalize, method=self.seasonality)
        if self.lag_order != 0:
            X = self._add_lag(X, order=self.lag_order)
        return X

    def _growth_wrt_date(self, X, date):
        X = X.apply(lambda x: (x/x[date] - 1)*100)
        return X

    def _deseasonalize(self, X, method):
        if method == 'stl':
            stl = STL(X, seasonal=13, robust=True)
            res = stl.fit()
            return res.trend
        if method == 'yoy':
            return X.diff(12)

    def _add_lag(self, X, order):
        X[[str(col) + '_lag' + str(order) for col in X.columns]] = X.apply(
            lambda x: x.shift(order), result_type='expand'
        )
        return X
