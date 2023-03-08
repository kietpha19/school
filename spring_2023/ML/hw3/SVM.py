import numpy as np

# use a hyperplane to classify 
class SVM:
    def __init__(self):
        self.w = None # weights
        self.b = None # bias
    
    # have to make class label to be -1 and 1
    def fit(self, X, y):
        X = np.array(X)
        y = np.array(y)
        opt_predict = {}
        transforms = [[1,1], [-1,1], [-1,-1], [1,-1]]

        max_X_value = np.max(X)
        min_X_value = np.min(X)

        step_sizes = [max_X_value*0.1, max_X_value*0.01, max_X_value*0.001]

        b_range_multiple = 5
        b_multiple = 5
        latest_optimum = max_X_value*10

        for step in step_sizes:
            w = np.array([latest_optimum, latest_optimum])
            optimized = False
            while not optimized:
                for b in np.arange(-1*(max_X_value*b_range_multiple), max_X_value*b_range_multiple, step*b_multiple):
                    for transformation in transforms:
                        w_t = w*transformation
                        found_option = True

                        # Check the KKT conditions
                        for i in range(len(X)):
                            # Calculate the value of the decision function for sample i
                            yi = y[i]
                            xi = X[i]
                            if not yi*(np.dot(xi, w_t) - b) >= 1:
                                found_option = False

                        # If all KKT conditions are satisfied, save the optimized values
                        if found_option:
                            opt_predict[np.linalg.norm(w_t)] = [w_t, b]

                if w[0] < 0:
                    optimized = True
                    print('Optimized a step.')
                else:
                    w = w - step

            # Select the optimal values of w and b with the smallest L2 norm
            norms = sorted([n for n in opt_predict])
            opt_choice = opt_predict[norms[0]]
            self.w = opt_choice[0]
            self.b = opt_choice[1]
            latest_optimum = opt_choice[0][0] + step*2

    def predict(self, X_test):
        y_predict = np.sign(np.dot(np.array(X_test), self.w) + self.b)
        return y_predict
