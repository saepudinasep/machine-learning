import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

# Membaca data dari file Excel
# Gantilah 'contoh.xlsx' dengan nama file Excel Anda
df = pd.read_excel('contoh.xlsx')

# Pilih kolom yang ingin digunakan untuk pengelompokan menggunakan iloc
data_for_clustering = df.iloc[:, 1:]

# Langkah 1: Tentukan jumlah cluster (k)
k = 3

# Langkah 2: Inisialisasi pusat cluster secara acak
initial_centroids = data_for_clustering.sample(n=k, random_state=42)

# Tampilkan inisialisasi pusat cluster
print("Iterasi 0:")
print("Pusat Cluster Awal:")
print(initial_centroids)

# Langkah 3-5: Iterasi hingga konvergensi
max_iterations = 100
for iteration in range(max_iterations):
    # Langkah 3: Hitung jarak antara titik dengan centroid menggunakan Euclidean Distance
    distances = []
    for i in range(k):
        centroid = initial_centroids.values[i]
        distance_to_centroid = np.sqrt(
            np.sum((data_for_clustering.values - centroid)**2, axis=1))
        distances.append(distance_to_centroid)

    # Buat DataFrame jarak
    distance_df = pd.DataFrame(distances).T
    distance_df.columns = ['Distance_to_C{}'.format(i+1) for i in range(k)]

    # Langkah 4: Kelompokkan objek berdasarkan jarak ke centroid terdekat
    df['Cluster'] = distance_df.idxmin(axis=1)
    df['Cluster'] = df['Cluster'].apply(lambda x: int(x[-1]))

    # Langkah 5: Perbarui pusat cluster
    new_centroids = df.groupby('Cluster').mean(numeric_only=True)

    # Tampilkan hasil anggota setiap iterasi
    print(f"\nIterasi {iteration + 1}:")
    print("Pusat Cluster Baru:")
    print(new_centroids)
    print("Anggota Cluster:")
    print(df)

    # Cek apakah ada perubahan dalam cluster
    if not df['Cluster'].equals(df['OldCluster']):
        changed_objects = df[df['Cluster'] != df['OldCluster']]
        print("\nObjek yang berpindah cluster:")
        print(changed_objects)

    # Cek konvergensi
    if initial_centroids.equals(new_centroids):
        break
    else:
        initial_centroids = new_centroids.copy()
        df['OldCluster'] = df['Cluster'].copy()
