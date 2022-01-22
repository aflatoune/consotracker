import pandas as pd
import logging as lg
from pandas.core.common import count_not_none
from consotracker.models import Model
from datetime import datetime
from sklearn.model_selection import TimeSeriesSplit


class ROUE():
    """"Class implementing rolling-origin-update evaluation (ROUE).
    Relies on sklearn.model_selection.TimeSeriesSplit.
    """

    def __init__(self, model: Model, forecast_origin=None, n_splits=None):
        """
        Parameters
        ----------
        model {Model}
            A regression model supposed to implement the Model interface.

        forecast_origin {str} -- (default: {None})
            A string indicating the last date supposed to be observed when
            training `model` for the first time.

        n_splits {int} -- (default: {None})
            Number of splits.
        """
        if count_not_none(forecast_origin, n_splits) != 1:
            raise ValueError("Exactly one of forecast_origin and n_splits",
                             "must be specified.")
        if n_splits is None:
            lg.warning("Not specifying n_splits can be misleading if you\'re",
            "not working with monthly data.")

        self.model = model
        self.forecast_origin = forecast_origin
        self.n_splits = n_splits

    def fit(self):
        endog = self.model.endog
        exog = self.model.exog
        self.in_values = []
        self.out_values = []

        if self.n_splits is None:
            lg.warning("As n_splits is not specified, its value is deduced",
            "from forecast_origin assuming that data are at a monthly freq.")
            last_date = exog.date.max()
            self.n_splits = ROUE.month_diff(self.forecast_origin, last_date)

        tscv = TimeSeriesSplit(n_splits=self.n_splits, test_size=1)
        for train_index, test_index in tscv.split(endog):
            pass

    @staticmethod
    def month_diff(date1, date2):
        date1 = datetime.strptime(date1, "%Y-%m-%d")
        date2 = datetime.strptime(date2, "%Y-%m-%d")
        diff = (date2.year - date1.year) * 12 + date2.month - date1.month
        return diff
