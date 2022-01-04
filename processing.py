from statsmodels.tsa.seasonal import STL


class Processing:
    def __init__(self, base_date="2004-01-01", seasonality=None, lag_order=0):
        self.base_date = base_date
        self.seasonality = seasonality
        self.lag_order = lag_order

    def fit(self, X):
        if self.base_date is not None:
            X = self._growth_wrt_date(X, self.base_date)
        if self.seasonality is not None:
            X = X.apply(self._deseasonalize, mode=self.seasonality)
        if self.lag_order != 0:
            X = self._add_lag(X, order=self.lag_order)
        return X

    def _deseasonalize(self, X, mode):
        if mode == "stl":
            stl = STL(X, seasonal=13, robust=True)
            res = stl.fit()
            return res.trend
        if mode == "yoy":
            return X.diff(12)

    def _growth_wrt_date(self, X, date):
        X = X.apply(lambda x: (x/x[date] - 1)*100)
        return X

    def _add_lag(self, X, order):
        X[[str(col) + "lag" for col in X.columns]] = X.apply(
            lambda x: x.shift(order), result_type="expand"
        )
        return X
