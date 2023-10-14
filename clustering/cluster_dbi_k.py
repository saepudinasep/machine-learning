import numpy as np
import pandas as pd

# Custom K-means implementation to handle empty clusters


class CustomKMeans:
    def __init__(self, n_clusters, max_iterations=100, init_method='random'):
        self.n_clusters = n_clusters
        self.max_iterations = max_iterations
        self.init_method = init_method

    def initialize_centroids(self, data):
        if self.init_method == 'random':
            centroids_indices = np.random.choice(
                data.shape[0], self.n_clusters, replace=False)
            centroids = data[centroids_indices]
        elif self.init_method == 'k-means++':
            centroids = [data[np.random.choice(data.shape[0])]
                         for _ in range(self.n_clusters)]
        else:
            raise ValueError("Invalid initialization method.")
        return np.array(centroids)

    def fit(self, data):
        centroids = self.initialize_centroids(data)
        cluster_dataframes = []

        for iteration in range(self.max_iterations):
            # Calculate distances using Euclidean distance
            distances = np.sqrt(
                ((data[:, np.newaxis] - centroids) ** 2).sum(axis=2))
            labels = np.argmin(distances, axis=1)

            new_centroids = np.array(
                [data[labels == i].mean(axis=0) for i in range(self.n_clusters)])

            if np.all(centroids == new_centroids):
                break

            centroids = new_centroids

            # Create a DataFrame for the current iteration's results
            iteration_df = data_for_clustering.copy()
            # Adding 1 to labels to match cluster numbering
            iteration_df['Cluster'] = labels + 1

            cluster_dataframes.append(iteration_df)

            # Print cluster membership and centroids for this iteration
            print(f"Iteration {iteration + 1}:")
            for i in range(self.n_clusters):
                cluster_data = iteration_df[iteration_df['Cluster'] == i + 1]
                cluster_centroid = centroids[i]
                print(f"Cluster {i + 1}:")
                print(f"Centroid: {cluster_centroid}")
                print(f"Members:")
                print(cluster_data)
                print()

        return labels, centroids, cluster_dataframes

# Function to calculate the Davies-Bouldin Index


def davies_bouldin_index(data, labels, centers):
    n_clusters = len(np.unique(labels))
    cluster_distances = np.zeros((n_clusters, n_clusters))
    db_indices = []

    for i in range(n_clusters):
        for j in range(i + 1, n_clusters):
            cluster_distances[i, j] = np.sqrt(
                np.sum((centers[i] - centers[j]) ** 2))
            cluster_distances[j, i] = cluster_distances[i, j]

    max_cluster_distances = np.max(cluster_distances, axis=1)

    for i in range(n_clusters):
        if i != np.argmax(max_cluster_distances):
            db_indices.append(np.mean(
                (np.sqrt(np.sum((data[labels == i] - centers[i]) ** 2)) / sum(labels == i) +
                 np.sqrt(np.sum((data[labels == np.argmax(max_cluster_distances)] - centers[i]) ** 2)) /
                 sum(labels == np.argmax(max_cluster_distances))) / cluster_distances[i, np.argmax(max_cluster_distances)]))

    return np.mean(db_indices)


# Read data from an Excel file (change the file name accordingly)
df = pd.read_excel('Dataset Bahan Skripsi.xlsx')

# Select columns for clustering
data_for_clustering = df.iloc[:, 1:]

# Prompt the user for the initial and final values of k
start_k = int(input("Masukkan nilai awal k: "))
end_k = int(input("Masukkan nilai batas k: "))

# Prompt the user to choose the initialization method for cluster centers
init_method = input(
    "Pilih metode inisialisasi pusat cluster (random/k-means++): ")

# Initialize dictionaries to store DBI for each k
dbi_values = {}

# Iterate over different values of k
for k in range(start_k, end_k + 1):
    # Create a custom KMeans instance
    kmeans = CustomKMeans(n_clusters=k, init_method=init_method)

    # Fit the data and get cluster labels, centroids, and cluster DataFrames
    labels, centroids, cluster_dataframes = kmeans.fit(
        data_for_clustering.values)

    # Calculate the Davies-Bouldin Index
    dbi = davies_bouldin_index(data_for_clustering.values, labels, centroids)
    dbi_values[k] = dbi

    # Print the DBI for this k
    print(f"Davies-Bouldin Index (k={k}): {dbi}")

# Print DBI values for all k values
print("\nDBI Values:")
for k, dbi in dbi_values.items():
    print(f"k={k}: {dbi}")
