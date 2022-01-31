import pandas as pd
import numpy as np
import logging as lg
import matplotlib.pyplot as plt
from pandas.core.common import count_not_none
from datetime import datetime
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV


class ROUE():
    """Class implementing rolling-origin-update evaluation (ROUE).
    """

    def __init__(self,
                 model,
                 param_grid,
                 scoring="neg_mean_absolute_error",
                 n_splits=None,
                 forecast_window=None,
                 refit=False,
                 verbose=0):
        """
        Parameters
        ----------
        model {object}
            A regression model compatible with GridSearchCV().

        params {dict}
            Dictionary with parameters names as keys and lists of paramater

        scoring {str} -- (default: {"neg_mean_absolute_error"})
            Strategy to evaluate the performance of the cross-validated model
            on the test set.

        n_splits {int} -- (default: {None})
            Number of splits.

        forecast_window {tuple} -- (default: {None})
            A tuple of two strings: the 1st indicates the last date supposed
            to be observed when training `model` for the first time, the 2nd one
            indicates the last date for which an out-of-sample prediction is
            computed. Concretely, a oot prediction is made for all dates such
            that forecast_window[1] < date =< forecast_window[2] (must be in
            YYYY/MM/DD format).

        refit {bool} -- (default: {False})
            Refit the best estimator on the rolling train/test indexes to get
            fitted and predicted values.
        """
        if count_not_none(forecast_window, n_splits) != 1:
            raise ValueError("Exactly one of forecast_window and n_splits",
                             "must be specified.")

        if n_splits is None:
            lg.warning("As n_splits is not specified, its value is deduced",
                       "from forecast_window assuming that data are at a",
                       "monthly freq. This can be misleading if you\'re",
                       "not working with monthly data")
            self.n_splits = ROUE.month_diff(self.forecast_window[1],
                                            self.forecast_window[2])

        self.model = model
        self.param_grid = param_grid
        self.scoring = scoring
        self.forecast_window = forecast_window
        self.n_splits = n_splits
        self.refit = refit
        self.verbose = verbose

    def fit(self, X, y):
        """
        Parameters
        ----------
        X {pd.DataFrame}
            Features data.

        y {pd.DataFrame}
            Target relative to X.
        """
        if "date" in y.columns:
            y = y.drop(["date"], axis=1)
        if "date" in X.columns:
            X = X.drop(["date"], axis=1)

        tscv = TimeSeriesSplit(n_splits=self.n_splits, test_size=1)
        self.gridcv = GridSearchCV(estimator=self.model,
                                   cv=tscv,
                                   scoring=self.scoring,
                                   param_grid=self.param_grid,
                                   verbose=self.verbose).fit(X, y)

        if self.refit:
            out_values = []
            best_model = self.gridcv.best_estimator_
            indexes = tscv.split(X)
            first_idx, *other_idx = indexes

            # Get fitted pred
            best_model.fit(X.loc[first_idx[0]], y.loc[first_idx[0]])
            in_values = best_model.predict(X.loc[first_idx[0]])
            out_values.append(best_model.predict(X.loc[first_idx[1]]))

            # Get test pred
            for train_index, test_index in other_idx:
                best_model.fit(X.loc[train_index], y.loc[train_index])
                y_pred = best_model.predict(
                    X.loc[test_index].values.reshape(1, -1))
                out_values.append(y_pred)

            out_values = np.concatenate(out_values)
            pred = np.concatenate([in_values, out_values])
            pred = pd.DataFrame(pred, columns=["pred"])
            self.predicted_df = pd.concat(
                [y.rename(columns={y.columns[0]: "obs"}), pred], axis=1
            )

    def plot(self, date=None):
        """
        Parameters
        ----------
        date {str} -- (default: {None})
            String indicating the first and the last date of the plot
            (dates must be in YYYY/MM/DD format).

        Returns
        -------
        Matplotlib Axes object.
        """
        if not self.refit:
            raise ValueError("cannot call plot() when refit is False")
        else:
            predicted_df = self.predicted_df

        if date is None:
            abscissa = range(predicted_df.shape[0])
        else:
            abscissa = pd.date_range(start=date,
                                     periods=predicted_df.shape[0],
                                     freq="MS")

        fig, ax = plt.subplots(figsize=(16, 9))
        ax.plot(abscissa, predicted_df.obs)
        ax.plot(abscissa, predicted_df.pred)
        plt.legend(["obs", "pred"])
        return ax

    def plot_params_score(self, figsize=(15, 5)):
        """
        Returns
        -------
        Matplotlib Axes object.
        """
        if not hasattr(self, "gridcv"):
            raise ValueError("cannot call plot_params_score() before fit()")

        gridcv = self.gridcv
        cv_results = self.gridcv.cv_results_
        means_test = cv_results['mean_test_score']
        stds_test = cv_results['std_test_score']

        masks = []
        masks_names = list(gridcv.best_params_.keys())
        for p_k, p_v in gridcv.best_params_.items():
            masks.append(list(cv_results['param_'+p_k].data == p_v))

        params = gridcv.param_grid

        fig, ax = plt.subplots(1, len(params), figsize=figsize)
        fig.suptitle('Score per parameter')
        fig.text(0.04, 0.5, 'MEAN SCORE', va='center', rotation='vertical')
        for i, p in enumerate(masks_names):
            m = np.stack(masks[:i] + masks[i+1:])
            best_parms_mask = m.all(axis=0)
            best_index = np.where(best_parms_mask)[0]
            x = np.array(params[p])
            y_1 = np.array(means_test[best_index])
            e_1 = np.array(stds_test[best_index])
            ax[i].errorbar(x, y_1, e_1, linestyle='--',
                           marker='o', label='oot')
            ax[i].set_xlabel(p.upper())
        plt.legend()
        return ax

    @staticmethod
    def month_diff(date1, date2):
        date1 = datetime.strptime(date1, "%Y-%m-%d")
        date2 = datetime.strptime(date2, "%Y-%m-%d")
        diff = (date2.year - date1.year) * 12 + date2.month - date1.month
        return diff
