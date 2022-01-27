import pandas as pd
import numpy as np
import statsmodels.api as sm
from consotracker.models import Model


class LinearRegression(Model):
    """Class for linear model
    """

    def __init__(self, params=None):
        super().__init__(params)

    def fit(self, remove_obs=1):
        """
        Parameters
        ----------
        remove_obs {int} -- (default: {1})
            Number of observations to remove when fitting the model. Points are
            removed starting from the end.
        """
        X = sm.add_constant(self.exog)
        X = X.iloc[:-remove_obs,:]
        y = self.endog
        lm = sm.OLS(y, X)
        self.model = lm.fit()
        self.in_values = self.model.fittedvalues

    def predict(self, X):
        """
        Parameters
        ----------
        X {pd.DataFrame or pd.Series}
            Training data.
        """
        if not isinstance(X, (pd.DataFrame, pd.Series)):
            raise TypeError("X must be a pandas DataFrame or Series.")

        if isinstance(X, pd.Series):
            X = X.values.reshape(1, -1)

        X = sm.add_constant(X, has_constant="add")
        self.out_values = self.model.predict(X)

        first_date = self.index.min()
        periods = self.endog.shape[0] + X.shape[0]
        freq = pd.infer_freq(self.endog.date)
        self.dates = pd.date_range(
            start=first_date, periods=periods, freq=freq
        )

        self.predicted_df = pd.DataFrame(
            {
                "date": self.dates,
                "obs": self.endog,
                "pred": np.concatenate([self.in_values, self.out_values])
            }
        )

        def __str__(self):
            return "Linear regression"
