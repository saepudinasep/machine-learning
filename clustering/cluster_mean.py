import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

# Membaca data dari file Excel
# Gantilah 'contoh.xlsx' dengan nama file Excel Anda
df = pd.read_excel('Dataset Bahan Skripsi.xlsx')

# Pilih kolom yang ingin digunakan untuk pengelompokan menggunakan iloc
data_for_clustering = df.iloc[:, 1:]

# Langkah 1: Tentukan jumlah cluster (k)
k = 3

# Inisialisasi kolom 'Cluster' dengan nilai acak untuk memulai
df['Cluster'] = np.random.randint(1, k + 1, size=len(df))

# Langkah 2: Inisialisasi pusat cluster dengan rata-rata
initial_centroids = data_for_clustering.groupby(df['Cluster']).mean()

# Tampilkan inisialisasi pusat cluster
print("Iterasi 0:")
print("Pusat Cluster Awal:")
print(initial_centroids)

# Inisialisasi variabel untuk menyimpan informasi cluster pada setiap iterasi
previous_clusters = None

# Langkah 3-5: Iterasi hingga konvergensi
max_iterations = 100
for iteration in range(max_iterations):
    # Langkah 3: Hitung jarak antara titik dengan centroid menggunakan Euclidean Distance
    distances = []
    for i in range(k):
        distances.append(np.sqrt(
            np.sum((data_for_clustering.values - initial_centroids.values[i])**2, axis=1)))

    # Buat DataFrame jarak
    distance_df = pd.DataFrame(distances).T
    distance_df.columns = ['Distance_to_C{}'.format(i+1) for i in range(k)]

    # Langkah 4: Kelompokkan objek berdasarkan jarak ke centroid terdekat
    df['Cluster'] = distance_df.idxmin(axis=1)
    df['Cluster'] = df['Cluster'].apply(lambda x: int(x[-1]))

    # Menyimpan informasi cluster pada iterasi saat ini
    current_clusters = df['Cluster'].copy()

    # Membandingkan dengan informasi cluster pada iterasi sebelumnya
    if previous_clusters is not None and current_clusters.equals(previous_clusters):
        print(f"\nIterasi {iteration + 1}: Konvergensi tercapai.")
        break
    else:
        print(f"\nIterasi {iteration + 1}:")
        print("Pusat Cluster Baru:")
        print(initial_centroids)
        print("Anggota Cluster:")
        print(df)
        # Update cluster pada iterasi sebelumnya
        previous_clusters = current_clusters.copy()

    # Langkah 5: Perbarui pusat cluster
    new_centroids = data_for_clustering.groupby(df['Cluster']).mean()

    # Cek konvergensi
    if initial_centroids.equals(new_centroids):
        print(f"\nIterasi {iteration + 1}: Konvergensi tercapai.")
        break
    else:
        initial_centroids = new_centroids.copy()
