import numpy as np

class Attribute():
    def __init__(self, name, is_numeric, data):
        self.name = name
        self.is_numeric = is_numeric
        if not is_numeric:
            self.values = np.unique(data)
    
    # could improve this by using recursion
    def choose_thresh(self, data):
        self.thresh = np.mean(data)
        return self.thresh
    
    def get_values(self, data):
        self.values = np.unique(data)
        return self.values