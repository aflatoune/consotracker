import pandas as pd
import numpy as np
import statsmodels.api as sm
from consotracker.models import Model
from dateutil.relativedelta import relativedelta


class LinearRegression(Model):
    """Class for linear model
    """

    def __init__(self, endog, exog):
        super().__init__(endog, exog)

    def fit(self):
        X = sm.add_constant(self.exog)
        X = X.drop(["date"], axis=1)
        y = self.endog
        y = y.drop(["date"], axis=1)
        lm = sm.OLS(y, X)
        self.model = lm.fit()
        self.in_values = self.model.fittedvalues

    def predict(self, X):
        X = X.values.reshape(1, -1)
        X = sm.add_constant(X, has_constant="add")
        self.out_values = self.model.predict(X)

        first_date = self.exog.date.min()
        last_date = self.exog.date.max() + relativedelta(months=1)
        freq = pd.infer_freq(self.exog.date)
        self.dates = pd.date_range(start=first_date, end=last_date, freq=freq)

        self.predicted_df = pd.DataFrame(
            {
                "date": self.dates,
                "obs": self.endog,
                "pred": np.concatenate([self.in_values, self.out_values])
            }
        )

        def __str__(self):
            return "Linear regression"
