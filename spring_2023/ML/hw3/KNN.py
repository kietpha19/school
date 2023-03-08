import numpy as np
import warnings
from collections import Counter

class KNN:
    def __init__(self, k=5):
        self.k = k
        
    def fit(self, X, y):
        if y.nunique() >= self.k:
            warnings.warn("K is set to a value less than total voting groups")
        self.X = X
        self.y = y
        
    def predict(self, X_test):
        # y_test is column vector
        y_predict = np.zeros(X_test.shape[0], dtype=self.y.dtype)
        
        # using vectorized approach so that only need to use single for-loop
        # loop through the test set
        for i, x_test in enumerate(X_test):
            # a list of all distances between the ONE sameple x and  ALL the training X
            distances = np.linalg.norm(self.X - x_test, axis=1)
            # pick out the k nearest neighbor
            nearest_indices = np.argsort(distances)[:self.k]
            # get the label of those k nearest neighbor
            nearest_labels = self.y[nearest_indices]
            # pick the label with most frequency
            y_predict[i] = Counter(nearest_labels).most_common()[0][0]
            
        return y_predict
