import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings( "ignore" )
from Attribute import Attribute
from DecisionTreeClassifier import DecisionTreeClassifier

def main():
    df_train = pd.read_csv("btrain.csv")
    df_test = pd.read_csv("btest.csv")
    df_validate = pd.read_csv("bvalidate.csv")

    # Replace '?' by nan
    df_train = df_train.replace('?', np.nan)
    df_test = df_test.replace('?', np.nan)
    df_validate = df_validate.replace('?', np.nan)

    # drop rows where class label is NaN
    df_train = df_train.dropna(subset=[' winner'])
    df_test = df_test.dropna(subset=[' winner'])
    df_validate = df_validate.dropna(subset=[' winner'])

    X_train = df_train.iloc[:, :-1].astype("float64")
    y_train = df_train.iloc[:, -1].astype("float64")
    #print(y_train.unique())

    nominal_attributes = {"weather", "startingpitcher", "oppstartingpitcher", "homeaway"}
    attriutes = [] 

    for c in X_train.columns:
        if c.strip() not in nominal_attributes:
            # use interpolation to fill missing value for numeric attribute
            X_train[c] = X_train[c].interpolate()
            # then fill in the rest with mean value
            X_train[c] = X_train[c].fillna(np.mean(X_train[c].astype('float64')))
            # print(X_train[c].unique())
            attriutes.append(Attribute(name=c, is_numeric=True))
        else:
            # fill missing value of nominal attribute with the most frequent value
            X_train[c] = X_train[c].fillna(X_train[c].mode()[0])
            # print(X_train[c].unique())
            attriutes.append(Attribute(name=c, is_numeric=False))
    
    dtc = DecisionTreeClassifier(attributes=attriutes)
    dtc.fit(X_train, y_train)
    
if __name__ == "__main__":
    main()