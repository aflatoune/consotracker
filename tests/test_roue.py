from random import random
import pytest
from sklearn.ensemble import RandomForestRegressor
from consotracker.roue import ROUE
from pandas.util.testing import makeTimeDataFrame


class TestROUE:
    DF = makeTimeDataFrame()
    RANDOM_PARAM = {"n_estimators": 100}
    RANDOM_MODEL = RandomForestRegressor(random_state=123)

    def test_count_not_none(self):
        with pytest.raises(ValueError):
            roue = ROUE(model=self.RANDOM_MODEL,
                        param_grid=self.RANDOM_PARAM,
                        n_splits=4,
                        forecast_window=("2003-01-01", "2003-05-01"))

    def test_month_diff(self):
        roue_1 = ROUE(model=self.RANDOM_MODEL,
                      param_grid=self.RANDOM_PARAM,
                      n_splits=4)
        roue_2 = ROUE(model=self.RANDOM_MODEL,
                      param_grid=self.RANDOM_PARAM,
                      forecast_window=("2003-01-01", "2003-05-01"))
        assert roue_1.n_splits == roue_2.n_splits

    def test_refit_consistency(self):
        pass
