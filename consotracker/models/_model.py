import logging as lg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod


class Model(ABC):
    """Parent class for all models
    """

    predicted_df = None

    def __init__(self, params):
        self.params = params

    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def predict(self):
        pass

    def plot(self, start=None, **kwargs):
        """Plot method for class Model

        Parameters
        ----------
        start {str} -- (default: {None})
            Indicates the begining of the x axis (must be in YYYY/MM/DD format).

        Returns
        -------
        Matplotlib Axes object.
        """
        predicted_df = self.predicted_df
        if predicted_df is None:
            raise ValueError("cannot call plot() before predict().")

        if start is not None:
            predicted_df = predicted_df[predicted_df.date >= start]

        figsize = kwargs.get("figsize", (11, 6))
        title = kwargs.get("title", None)
        pred_color = kwargs.get("pred_color", "darkorange")
        obs_color = kwargs.get("obs_color", "darkblue")
        xlabel = kwargs.get("xlabel", None)
        ylabel = kwargs.get("ylabel", None)

        fig, ax = plt.subplots(figsize=figsize)
        ax.grid(visible=True, which="major")
        ax.plot(predicted_df.date, predicted_df.obs, c=obs_color)
        ax.plot(predicted_df.date, predicted_df.pred, c=pred_color)
        ax.set_label(xlabel)
        ax.set_ylabel(ylabel)
        ax.margins(x=0)
        fig.autofmt_xdate(rotation=90)
        ax.set_title(title)
        ax.legend(["obs", "pred"], bbox_to_anchor=[0.5, 0],
                  loc="lower center", ncol=2)
        return (fig, ax)

    def _check_data(self, *arrays):
        if not all(isinstance(array.index, pd.DatetimeIndex) for array in arrays):
            raise TypeError("Data must have a DatetimeIndex.")
        dates = np.array([array.index.min() for array in arrays])
        if len(np.unique(dates)) != 1:
            lg.warning("Arrays have been modified so that they all have the "
                       "same starting date.")
            return tuple(array[array.index >= dates.max()] for array in arrays)
        else :
            return arrays
