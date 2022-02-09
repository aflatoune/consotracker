from sklearn.metrics import mean_absolute_error, mean_squared_error
import pandas as pd
import numpy as np


def RMSE(data: pd.DataFrame, y_true: str, y_pred: str, round_value=3):
    rmse = np.sqrt(mean_squared_error(y_true=data[y_true], y_pred=data[y_pred]))
    return np.round(rmse, round_value)

def MAE(data: pd.DataFrame, y_true: str, y_pred: str, round_value=3):
    mae = mean_absolute_error(y_true=data[y_true], y_pred=data[y_pred])
    return np.round(mae, round_value)