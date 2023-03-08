import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.preprocessing import LabelEncoder
import argparse
from MyModel import KNN, SVM

import warnings
warnings.filterwarnings( "ignore" )

le = LabelEncoder()

class MLChoice:
    def __init__(self, ML, df):
        if ML == "KNN":
            self.model = KNN()
            self.lib_model = KNeighborsClassifier(n_neighbors=5)
        elif ML == "SVM":
            self.model = SVM()
            self.lib_model = svm.SVC(kernel='linear')
        else:
            print("not an available model")
            exit(0)

        self.pre_process(df)
    
    def pre_process(self, df):
        X = df.iloc[:, :-1].to_numpy()
        y = df.iloc[:, -1].to_numpy()

        #convert y class label t0 -1, 1 for SVM
        y = le.fit_transform(y)
        y = (2*y - 1)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    
    def get_output(self, dataset = "", alg_name= "", output_file="output.txt", n_print=1):
        f = open(output_file, 'w')
        f.write("Dataset: " + dataset + "\n")
        f.write("Machine Learning algorithm chosen: " + alg_name + "\n")

        self.model.fit(self.X_train, self.y_train)
        y_predict = self.model.predict(self.X_test)
        my_accuracy = self.model.accuracy(y_predict, self.y_test)
        f.write("Accuracy of training (Scratch): " + str(my_accuracy)+ "\n")

        self.lib_model.fit(self.X_train, self.y_train)
        lib_y_predict = self.lib_model.predict(self.X_test)
        lib_accuracy = np.mean(lib_y_predict==self.y_test)*100
        f.write("Accuracy of Scikit-learn model: " + str(lib_accuracy) + "\n")

        for i in range(n_print):
            f.write("Prediction Point: " + str(self.X_test[i]) + "\n")
            f.write("Predicted Class: " + str(y_predict[i]) + "\n")
            f.write("Actual class: " + str(self.y_test[i]) + "\n")


def main():
    # parse the command line parameter
    # Create argument parser object
    parser = argparse.ArgumentParser()

    # Add arguments to the parser
    parser.add_argument('--model', type=str, help='what model to utilize KNN or SVM')
    parser.add_argument('--data', type=str, help='name of the data file')

    # Parse the arguments from the command line
    args = parser.parse_args()
    model = args.model
    file_name = args.data
    df = pd.read_csv(file_name,sep= ",")

    my_model = MLChoice(model, df)

    if file_name == "bank.txt":
        dataset = "Bank Note"
    elif file_name == "sonar.txt":
        dataset = "sonar"

    my_model.get_output(dataset=dataset, alg_name=model, output_file="output.txt", n_print=5)
    

if __name__ == "__main__":
    main()