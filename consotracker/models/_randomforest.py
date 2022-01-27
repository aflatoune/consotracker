import pandas as pd
import numpy as np
import sklearn.ensemble import RandomForestRegressor
from consotracker.models import Model


class RandomForest(Model):
    """Class for Random Forest
    """
    def __init__(self, **params):
        d = params
        super().__init__(d)
        self.model = RandomForestRegressor(d)