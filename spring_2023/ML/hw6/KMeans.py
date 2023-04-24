import numpy as np
import matplotlib.pyplot as plt

#random state = 42 so that everytime we randome generate number, 
# the result will be the same for debugging purpose.
np.random.seed(42) 
max_iters = 100

def plot(clusters, centroids, k, round):
    fig = plt.figure()
    plt.title("KMeans")
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

    #plt.savefig("output.pdf")
    plt.show()


# in this implementation, we keep track of clusters for visualize purpose
def KMeans(datasetFile, k=2):
    # load the data
    data = np.loadtxt(datasetFile, delimiter = ',')

    # randomly select the mean (centroids) of k cluster
    centroids = data[np.random.choice(data.shape[0], k, replace=False)]

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
        # initialize k cluster
        clusters = [[] for _ in range(k)]

        # for each data point in the dataset
        for x in data:
            # calculate the distance from data point to each centroids
            distances = [np.linalg.norm(x-c) for c in centroids]

            # assign the data point to the cluster that it's closest
            cluster_idx = np.argmin(distances)
            clusters[cluster_idx].append(x)
        
        # update the means (centroids)
        prev_centroids = centroids
        centroids = [np.mean(c, axis=0) for c in clusters]

        if i==0:
            plot(clusters, centroids, k, i+1)

        # check if all the means are converges
        # np.allchose check if two vectors are very close to some tolerant
        if np.allclose(prev_centroids, centroids):
            return clusters, centroids, i

    return clusters, centroids

k = 4
clusters, centroids, round = KMeans("ClusteringData.txt", k)
plot(clusters, centroids, k, round)


