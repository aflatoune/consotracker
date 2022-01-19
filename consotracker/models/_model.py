import pandas as pd
import matplotlib.pyplot as plt

class Model():
    """
    Parent class for all models
    """

    self.predicted_df = None

    def __init__(self, endog=None, exog=None):
        self.endog = endog
        self.exog = exog
        if endog is not None and pd.infer_freq(endog) == "N":
            raise ValueError("Unrecognised frequency for endog.")
        if exog is not None and pd.infer_freq(exog) == "N":
            raise ValueError("Unrecognised frequency for exog.")
        if endog is not None and exog is not None:
            if pd.infer_freq(endog) != pd.infer_freq(exog):
                raise ValueError("endog and exog must have the same frequency.")

    def fit(self):
        """abstract method
        """
        pass

    def predict(self):
        """abstract method
        """
        pass

    def plot(self):
        predicted_values = self.predicted_values
        if predicted_values is None:
            raise ValueError("cannot call plot() before fit() and predict().")