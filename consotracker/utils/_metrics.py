import numpy as np


def _check_length(*arrays):
    samples = [array.shape[0] for array in arrays]
    if len(np.unique(samples)) != 1:
        raise ValueError("Arrays do not have the same number of samples.")


def mae(obs, pred, round_value=3):
    """Mean Absolute (Forecast) Error
    """
    _check_length(obs, pred)
    mae_value = np.mean(np.absolute(pred - obs), axis=0)
    return np.round(mae_value, round_value)


def rmse(obs, pred, round_value=3):
    """Root Mean Square (Forecast) Error
    """
    _check_length(obs, pred)
    rmse_value = np.sqrt(np.mean((pred - obs)**2, axis=0))
    return np.round(rmse_value, round_value)

def mda(obs, pred, round_value=3):
    """Mean Directional Accuracy
    """
    _check_length(obs, pred)
    obs_diff = np.sign(obs[1:] - obs[:-1])
    pred_diff = np.sign(pred[1:] - pred[:-1])
    mda_value = np.mean(obs_diff == pred_diff, axis=0)
    return np.round(mda_value, round_value)
