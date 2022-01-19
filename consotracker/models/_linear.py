import statsmodels.api as sm
import pandas as pd
from dateutil.relativedelta import relativedelta

class LinearRegression(Model):
    """Class for linear model
    """

    def __init__(self, endog, exog):
        super().__init__(endog, exog)

    def fit(self):
        X = sm.add_constant(self.exog)
        y = self.endog
        lm = sm.OLS(y, X)
        self.model = lm.fit()
        self.in_values = self.model.fittedvalues

    def predict(self, X):
        X = X.values.reshape(1, -1)
        X = sm.add_constant(X, has_constant="add")
        self.out_values = self.model.predict(X)

        first_date = exog.index.min()
        self.dates = pd.date_range(start=first_date, end=first_date + relativedelta(months=1))

        self.predicted_values = pd.DataFrame(
            {
                "date": self.dates,
                "values": np.concatenate([self.in_values, self.out_values])
            }
    )
