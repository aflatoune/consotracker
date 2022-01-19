import statsmodels.api as sm

class LinearRegression(Model):
    """Class for linear model
    """

    def __init__(self):
        super().__init__()

    def fit(self, X, y):
        X = sm.add_constant(X)
        lm = sm.OLS(y, X)
        self.model = lm.fit()
        self.ins_values = lm.fittedvalues
