import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from consotracker.models import Model


class RandomForest(Model):
    """Class for Random Forest
    """

    def __init__(self, **params):
        d = params
        super().__init__(d)
        self.model = RandomForestRegressor(d)

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
        self.model = self.model.fit(X, y)
        self.in_values = self.model.predict(X)

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
        return self.out_values

    def __str__(self):
        return "Random Forest"
