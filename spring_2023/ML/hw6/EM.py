import numpy as np
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt

max_iters = 100
tol = 1e-4 #tolerant threshold

def plot(clusters, centroids, k, round):
    fig = plt.figure()
    plt.title("EM")
    plt.axis('off')
    fig.text(0.85, 0.9, "k=" + str(k), fontsize=10, color='red')
    fig.text(0.85, 0.8, "round: " + str(round), fontsize=10, color='red')
    ax = fig.add_subplot(projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # Define colors for each label
    colors = ['r', 'g', 'b', 'y', 'c', 'm', 'k', 'purple', 'orange', 'brown', 'pink']
    
    # Plot each cluster with a different color
    #print(centroids)
    for i in range(k):
        # plot the mean of each clusters
        ax.scatter(centroids[i][0], centroids[i][1], centroids[i][2], c=colors[i], s=50, marker='x');
        for x in clusters[i]:
            # Plot the data points in the current cluster with a color corresponding to the label
            ax.scatter(x[0], x[1], x[2], c=colors[i], s=1)

    plt.show()

def initialize_parameters(data, k):
    # Initialize each μ_i to a random value
    centroids = data[np.random.choice(data.shape[0], k, replace=False)]
    
    # Set each σ_i to 1
    covariances = [np.identity(data.shape[1]) for _ in range(k)]
    
    # Set each w_i equal to 1/k
    weights = [1/k] * k
    
    return centroids, covariances, weights

def EM(datasetFile, k=2):
    data = np.loadtxt(datasetFile, delimiter = ',')
    # Initialize parameters
    centroids, covariances, weights = initialize_parameters(data, k)
    last_log_likelihood = float('-inf')

    ####################################################################
    # randomly assign each datapoint to a cluster at the beginning
    # Initialize empty lists for each cluster
    clusters = [[] for _ in range(k)]
    # Iterate over data points and assign to clusters based on highest responsibility
    for j in range(data.shape[0]):
        cluster_idx = np.random.randint(0,k)
        clusters[cluster_idx].append(data[j])
    plot(clusters, centroids, k, 0)
    ####################################################################

    for i in range(max_iters):
        # E-step
        # responsibilities aka conditional probability
        responsibilities = np.zeros((data.shape[0], k))
        for j in range(k):
            # the formular given in the slide
            responsibilities[:,j] = weights[j] * multivariate_normal.pdf(data, centroids[j], covariances[j])
        responsibilities /= np.sum(responsibilities, axis=1)[:,np.newaxis]

        # M-step
        weights = np.sum(responsibilities, axis=0) / data.shape[0]
        for j in range(k):
            centroids[j] = np.sum(responsibilities[:,j][:,np.newaxis] * data, axis=0) / np.sum(responsibilities[:,j])
            covariances[j] = ((responsibilities[:,j][:,np.newaxis] * (data - centroids[j])).T @ (data - centroids[j])) / np.sum(responsibilities[:,j])

        # Calculate log likelihood
        log_likelihood = np.sum(np.log(np.sum(responsibilities, axis=1)))

        # Initialize empty lists for each cluster
        clusters = [[] for _ in range(k)]
        # Iterate over data points and assign to clusters based on highest responsibility
        for j in range(data.shape[0]):
            cluster_idx = np.argmax(responsibilities[j])
            clusters[cluster_idx].append(data[j])

        if i==0:
            plot(clusters, centroids, k, i+1)

        # Check for convergence
        if log_likelihood - last_log_likelihood < tol:
            return clusters, centroids, i

        # Update last log likelihood
        last_log_likelihood = log_likelihood

    # return centroids, covariances, weights, responsibilities #use this when we need to predict new data later
    return clusters, centroids, i

k = 4
clusters, centroids, round = EM("ClusteringData.txt", k)
plot(clusters, centroids, k, round)


