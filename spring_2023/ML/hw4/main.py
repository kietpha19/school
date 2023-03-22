import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings( "ignore" )
from Attribute import Attribute
from DecisionTreeClassifier import DecisionTreeClassifier

def main():
    df_train = pd.read_csv("btrain.csv", sep=',\s*')
    df_test = pd.read_csv("btest.csv", sep=',\s*')
    df_validate = pd.read_csv("bvalidate.csv", sep=',\s*')

    X_test_original = df_test.iloc[:, :-1] # use to write to prediction file

    # Replace '?' by nan
    df_train = df_train.replace('?', np.nan)
    df_test = df_test.replace('?', np.nan)
    df_validate = df_validate.replace('?', np.nan)

    # drop rows where class label is NaN
    df_train = df_train.dropna(subset=['winner'])
    df_validate = df_validate.dropna(subset=['winner'])

    # train dataset
    X_train = df_train.iloc[:, :-1].astype("float64")
    y_train = df_train.iloc[:, -1].astype("float64")
    #print(y_train.unique())

    # test dataset
    X_test = df_test.iloc[:, :-1].astype("float64")
    
    # validate dataset
    X_validate = df_validate.iloc[:, :-1].astype("float64")
    y_validate = df_validate.iloc[:, -1].astype("float64")


    nominal_attributes = {"weather", "startingpitcher", "oppstartingpitcher", "homeaway"}
    attriutes = [] 

    for c in X_train.columns:
        if c not in nominal_attributes:
            # use interpolation to fill missing value for numeric attribute
            X_train[c] = X_train[c].interpolate()
            X_test[c] = X_test[c].interpolate()
            X_validate[c] = X_validate[c].interpolate()
            # then fill in the rest with mean value
            X_train[c] = X_train[c].fillna(np.mean(X_train[c].astype('float64')))
            X_test[c] = X_test[c].fillna(np.mean(X_test[c].astype('float64')))
            X_validate[c] = X_validate[c].fillna(np.mean(X_test[c].astype('float64')))
            # print(X_train[c].unique())
            attriutes.append(Attribute(name=c, is_numeric=True))
        else:
            # fill missing value of nominal attribute with the most frequent value
            X_train[c] = X_train[c].fillna(X_train[c].mode()[0])
            X_test[c] = X_test[c].fillna(X_test[c].mode()[0])
            X_validate[c] = X_validate[c].fillna(X_test[c].mode()[0])
            # print(X_train[c].unique())
            attriutes.append(Attribute(name=c, is_numeric=False))
    
    dtc = DecisionTreeClassifier(attributes=attriutes)
    dtc.fit(X_train, y_train)

    # predict the test dataset and write to "predictions.csv"
    y_pred = dtc.predict(X_test)
    y_pred = np.array(y_pred).astype('int')
    result = pd.concat([X_test_original.reset_index(drop=True), pd.Series(y_pred, name='predictedwinner')], axis=1)
    result.to_csv('predictions.csv', index=False)

    # use the validate dataset to calculate the accuracy
    y_pred = dtc.predict(X_validate)
    accuracy = dtc.accuracy(y_pred, y_validate)
    print(accuracy)

if __name__ == "__main__":
    main()