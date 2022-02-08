import numpy as np


def _check_length(*arrays):
    samples = [array.shape[0] for array in arrays]
    if len(np.unique(samples)) != 1:
        raise ValueError("Arrays do not have the same number of samples.")


def mae(obs, pred):
    """Mean Absolute (Forecast) Error
    """
    _check_length(obs, pred)
    return np.mean(np.absolute(pred - obs), axis=0)


def rmse(obs, pred):
    """Root Mean Square (Forecast) Error
    """
    _check_length(obs, pred)
    return np.sqrt(np.mean((pred - obs)**2, axis=0))


def mda(obs, pred):
    """Mean Directional Accuracy
    """
    _check_length(obs, pred)
    obs_diff = np.sign(obs[1:] - obs[:-1])
    pred_diff = np.sign(pred[1:] - pred[:-1])
    return np.mean(obs_diff == pred_diff, axis=0)
