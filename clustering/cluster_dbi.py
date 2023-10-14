import numpy as np
import pandas as pd
import json
from sklearn.metrics import pairwise_distances
from sklearn.datasets import make_blobs

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
        for iteration in range(self.max_iterations):
            distances = pairwise_distances(data, centroids)
            labels = np.argmin(distances, axis=1)

            new_centroids = np.array(
                [data[labels == i].mean(axis=0) for i in range(self.n_clusters)])

            if np.all(centroids == new_centroids):
                break

            centroids = new_centroids

        return labels, centroids


# Function to calculate the Davies-Bouldin Index
def davies_bouldin_index(data, labels, centers):
    n_clusters = len(np.unique(labels))
    cluster_distances = np.zeros((n_clusters, n_clusters))
    db_indices = []

    for i in range(n_clusters):
        for j in range(i + 1, n_clusters):
            cluster_distances[i, j] = np.sum(
                pairwise_distances(centers[i].reshape(1, -1), centers[j].reshape(1, -1)))
            cluster_distances[j, i] = cluster_distances[i, j]

    max_cluster_distances = np.max(cluster_distances, axis=1)

    for i in range(n_clusters):
        if i != np.argmax(max_cluster_distances):
            db_indices.append(np.mean(
                (np.sum(pairwise_distances(data[labels == i], [centers[i]], metric='euclidean')) / sum(labels == i) +
                 np.sum(pairwise_distances(data[labels == np.argmax(max_cluster_distances)], [centers[i]], metric='euclidean')) /
                 sum(labels == np.argmax(max_cluster_distances))) / cluster_distances[i, np.argmax(max_cluster_distances)]))

    return np.mean(db_indices)


# Membaca data dari file Excel
# Gantilah 'contoh.xlsx' dengan nama file Excel Anda
df = pd.read_excel('Dataset Bahan Skripsi.xlsx')

# Pilih kolom yang ingin digunakan untuk pengelompokan menggunakan iloc
data_for_clustering = df.iloc[:, 1:]

# Meminta pengguna untuk memasukkan jumlah cluster (k)
k = int(input("Masukkan jumlah cluster (k): "))

# Meminta pengguna untuk memilih metode inisialisasi pusat cluster
init_method = input(
    "Pilih metode inisialisasi pusat cluster (random/k-means++): ")

# Create a custom KMeans instance
kmeans = CustomKMeans(n_clusters=k, init_method=init_method)

# Fit the data and get cluster labels and centroids
labels, centroids = kmeans.fit(data_for_clustering.values)

# Calculate the Davies-Bouldin Index
dbi = davies_bouldin_index(data_for_clustering.values, labels, centroids)

# Print the DBI
print(f"Centroid: {centroids}")
print(f"Labels: {labels}")
print(f"Davies-Bouldin Index: {dbi}")
