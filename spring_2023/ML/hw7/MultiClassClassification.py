# Hoang Anh Kiet Pham
# 1001904809

import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization
from keras import optimizers
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split

data = pd.read_csv("glass.txt")
print(data)



