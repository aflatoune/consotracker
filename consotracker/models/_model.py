import logging as lg
import matplotlib.pyplot as plt

class Model():
    """
    Parent class for all models
    """

    self.predicted_values = None

    def __init__(self):
        pass

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