import pandas as pd
import numpy as np
import statsmodels.api as sm
from consotracker.models import Model


class LinearRegression(Model):
    """Class for linear model
    """

    def __init__(self, params=None):
        super().__init__(params)

    def fit(self, X, y):
        """
        Parameters
        ----------
        X {pd.DataFrame}
            Features data.

        y {pd.DataFrame}
            Target relative to X.
        """
        self.dates = X.index
        self.endog = y.values.flatten()
        X = sm.add_constant(X)
        lm = sm.OLS(y.values, X)
        self.model = lm.fit()
        self.in_values = self.model.fittedvalues

    def predict(self, X):
        """
        Parameters
        ----------
        X {pd.DataFrame or pd.Series}
            The input samples.
        """
        if not isinstance(X, (pd.DataFrame, pd.Series)):
            raise TypeError("X must be a pandas DataFrame or Series.")

        if isinstance(X, pd.Series):
            X = X.values.reshape(1, -1)

        X = sm.add_constant(X, has_constant="add")
        self.out_values = self.model.predict(X)

        first_date = self.dates.min()
        periods = self.in_values.shape[0] + X.shape[0]
        freq = pd.infer_freq(self.dates)
        dates = pd.date_range(
            start=first_date, periods=periods, freq=freq
        )

        self.predicted_df = pd.DataFrame(
            {
                "date": dates,
                "obs": np.append(self.endog, [np.nan]*X.shape[0]),
                "pred": np.concatenate([self.in_values, self.out_values])
            }
        )

        def __str__(self):
            return "Linear regression"
