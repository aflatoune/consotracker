import pandas as pd
import matplotlib.pyplot as plt
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from abc import ABC, abstractmethod


class Model(ABC):
    """Parent class for all models
    """

    predicted_df = None

    def __init__(self, endog=None, exog=None):
        self.endog = endog
        self.exog = exog
        if endog is not None:
            self._check_validity(endog)
        if exog is not None:
            self._check_validity(exog)

    def _check_validity(self, data):
        if "date" not in data.columns:
            raise ValueError(
                "Both endog and exog must contain a \"date\" column.")
        else:
            if not is_datetime(data["date"]):
                raise ValueError("\"date\" must be of type datetime64.")

    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def predict(self):
        pass

    def plot(self, start=None, figsize=None, **kwargs):
        predicted_df = self.predicted_df
        if predicted_df is None:
            raise ValueError("cannot call plot() before predict().")

        if figsize is None:
            figsize = (11, 6)

        title = kwargs.get(title, "")
        pred_color = kwargs.get(pred_color, "darkorange")
        obs_color = kwargs.get(obs_color, "darkblue")
        xlabel = kwargs.get(xlabel, "")
        ylabel = kwargs.get(ylabel, "")
        anchor = [0.5, 0]

        fig, ax = plt.subplots(figsize=figsize)
        ax.grid(visible=True, which="major")
        ax.plot(predicted_df.date, predicted_df.obs, c=obs_color)
        ax.plot(predicted_df.date, predicted_df.pred, c=pred_color)
        ax.set_label(xlabel)
        ax.set_ylabel(ylabel)
        ax.margins(x=0)
        fig.autofmt_xdate(rotation=90)
        plt.title(title)
        plt.legend(["obs", "pred"], bbox_to_anchor=anchor,
                   loc="lower center", ncol=2)
        return ax
