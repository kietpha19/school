import numpy as np
import warnings
from collections import Counter
from cvxopt import matrix, solvers

class KNN:
    def __init__(self, k=5):
        self.k = k
        
    def fit(self, X, y):
        if len(np.unique(y)) >= self.k:
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
    
    def accuracy(self, y_predict, y_test):
        return np.mean(y_predict == y_test)*100

'''

This implementation uses the simplified version of the SVM algorithm 
that estimates the weights and bias directly from the Lagrange multipliers. 
It also uses the random selection of two Lagrange multipliers to update at each iteration, 
which is a simple heuristic that improves convergence speed.
Finally, it stores the support vectors and their corresponding Lagrange multipliers 
to use them in the prediction phase.

The implementation is combination of my code (which is from the class lecture) and ChatGPT code

https://math.mit.edu/~edelman/publications/support_vector.pdf
https://pages.cs.wisc.edu/~dpage/cs760/SMOlecture.pdf
the paper and the slides were used as reference (SVM with Largrange Multiplier and SMO)

'''

class SVM:
    def __init__(self, C=1.0, tol=1e-3, max_iter=1000):
        self.C = C #regularization parameter
        self.tol = tol # tolerance parameter
        '''
        The algorithm continues to update the Lagrange multipliers until the KKT conditions are satisfied, 
        or until the difference between the previous and current values of the Lagrange multipliers is less than tol. 
        In other words, if the change in the Lagrange multipliers is smaller than tol, 
        the algorithm considers that it has converged and stops iterating. 
        A smaller value of tol means that the algorithm will continue to update the Lagrange multipliers 
        until a more precise solution is obtained, at the cost of potentially longer training time.
        '''
        self.max_iter = max_iter
        self.w = None
        self.b = None
        self.support_vectors = None
        self.alphas = None # the learning rate

    def fit(self, X, y):
        n_samples, n_features = X.shape

        # Initialize Lagrange multipliers and bias
        self.alphas = np.zeros(n_samples)
        self.b = 0.0

        # Compute Gram matrix
        K = np.dot(X, X.T)

        # Optimization loop
        # using SMO algorithm to solve the poly optimization problem
        for i in range(self.max_iter):
            # Compute predictions and errors
            y_pred = np.dot(self.alphas * y, K) + self.b
            errors = y_pred - y

            # Compute violation of KKT conditions
            y_times_error = y * errors
            is_violating_KKT = np.logical_or(self.alphas == 0, self.alphas == self.C)
            is_violating_KKT[is_violating_KKT == True] = y_times_error[is_violating_KKT == True] < 0
            is_violating_KKT[is_violating_KKT == False] = y_times_error[is_violating_KKT == False] > 0

            # Check if KKT conditions are satisfied, if satified then optimized
            if np.all(np.logical_not(is_violating_KKT)):
                break

            # Select two Lagrange multipliers to update
            i, j = np.random.choice(np.where(is_violating_KKT)[0], size=2, replace=False)

            # Compute the boundaries for the new Lagrange multiplier of the second sample
            if y[i] == y[j]:
                L = max(0, self.alphas[j] + self.alphas[i] - self.C)
                H = min(self.C, self.alphas[j] + self.alphas[i])
            else:
                L = max(0, self.alphas[j] - self.alphas[i])
                H = min(self.C, self.C + self.alphas[j] - self.alphas[i])

            # Compute the second derivative of the Lagrangian function with respect to alpha_j
            eta = 2 * K[i,j] - K[i,i] - K[j,j]

            # Skip if second derivative is non-positive
            if eta >= 0:
                continue

            # Update the Lagrange multipliers of the two samples
            alpha_j_new = self.alphas[j] - (y[j] * (errors[i] - errors[j])) / eta
            alpha_j_new = np.clip(alpha_j_new, L, H) # clip the interval edge
            alpha_i_new = self.alphas[i] + y[i] * y[j] * (self.alphas[j] - alpha_j_new)

            # Compute the bias
            b1 = self.b - errors[i] - y[i] * (alpha_i_new - self.alphas[i]) * K[i,i] - y[j] * (alpha_j_new - self.alphas[j]) * K[i,j]
            b2 = self.b - errors[j] - y[i] * (alpha_i_new - self.alphas[i]) * K[i,j] - y[j] * (alpha_j_new - self.alphas[j]) * K[i,j]

            # Choose the bias based on the support vectors
            if alpha_i_new > 0 and alpha_i_new < self.C:
                self.b = b1
            elif alpha_j_new > 0 and alpha_j_new < self.C:
                self.b = b2
            else:
                self.b = (b1 + b2) / 2

            # Update the Lagrange multipliers
            self.alphas[i] = alpha_i_new
            self.alphas[j] = alpha_j_new

        # Compute the weights and the support vectors
        self.w = np.dot(self.alphas * y, X)
        self.support_vectors = X[self.alphas > self.tol]
    
    def predict(self, X):
        y_pred = np.dot(self.w, X.T) + self.b
        return np.sign(y_pred)

    def accuracy(self, y_predict, y_test):
        return np.mean(y_predict == y_test)*100

