import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Contoh data dalam bentuk array NumPy dengan nama kecamatan
data = np.array([['Kecamatan A', 2, 3],
                 ['Kecamatan B', 4, 5],
                 ['Kecamatan C', 10, 12],
                 ['Kecamatan D', 8, 9],
                 ['Kecamatan E', 3, 2],
                 ['Kecamatan F', 9, 11],
                 ['Kecamatan G', 11, 13],
                 ['Kecamatan H', 2, 1],
                 ['Kecamatan I', 8, 7],
                 ['Kecamatan J', 12, 10],
                 ['Kecamatan K', 3, 4],
                 ['Kecamatan L', 10, 11],
                 ['Kecamatan M', 1, 2],
                 ['Kecamatan N', 9, 10],
                 ['Kecamatan O', 2, 4],
                 ['Kecamatan P', 8, 8],
                 ['Kecamatan Q', 11, 12],
                 ['Kecamatan R', 3, 3],
                 ['Kecamatan S', 9, 9],
                 ['Kecamatan T', 12, 11]], dtype=object)

# Konversi data menjadi DataFrame
df = pd.DataFrame(data, columns=['Kecamatan', 'Fitur1', 'Fitur2'])

# Menghapus kolom 'Kecamatan' dari data yang digunakan untuk pengelompokan
data_for_clustering = df[['Fitur1', 'Fitur2']].astype(float)

# Langkah 1: Tentukan jumlah cluster (k)
k = 3

# Langkah 2: Inisialisasi pusat cluster secara acak
initial_centroids = data_for_clustering.sample(n=k, random_state=42)

# Tampilkan inisialisasi pusat cluster
print("Iterasi 0:")
print("Pusat Cluster Awal:")
print(initial_centroids)

# Inisialisasi variabel untuk melacak perubahan cluster
previous_cluster_assignment = None

# Langkah 3-5: Iterasi hingga konvergensi
max_iterations = 100
for iteration in range(max_iterations):
    # Langkah 3: Hitung jarak antara titik dengan centroid menggunakan Euclidean Distance
    df['Distance_to_C1'] = np.sqrt((data_for_clustering['Fitur1'] - initial_centroids.iloc[0]['Fitur1'])**2 +
                                   (data_for_clustering['Fitur2'] - initial_centroids.iloc[0]['Fitur2'])**2)

    df['Distance_to_C2'] = np.sqrt((data_for_clustering['Fitur1'] - initial_centroids.iloc[1]['Fitur1'])**2 +
                                   (data_for_clustering['Fitur2'] - initial_centroids.iloc[1]['Fitur2'])**2)

    df['Distance_to_C3'] = np.sqrt((data_for_clustering['Fitur1'] - initial_centroids.iloc[2]['Fitur1'])**2 +
                                   (data_for_clustering['Fitur2'] - initial_centroids.iloc[2]['Fitur2'])**2)

    # Langkah 4: Kelompokkan objek berdasarkan jarak ke centroid terdekat
    df['Cluster'] = df[['Distance_to_C1',
                        'Distance_to_C2', 'Distance_to_C3']].idxmin(axis=1)
    df['Cluster'] = df['Cluster'].apply(lambda x: int(x[-1]))

    # Tampilkan hasil anggota setiap iterasi
    print(f"\nIterasi {iteration + 1}:")
    print("Pusat Cluster Baru:")
    print(initial_centroids)
    print("Anggota Cluster:")
    print(df[['Kecamatan', 'Fitur1', 'Fitur2', 'Cluster']])

    # Cek perubahan cluster pada iterasi saat ini
    current_cluster_assignment = df['Cluster'].values
    if previous_cluster_assignment is not None and not np.array_equal(current_cluster_assignment, previous_cluster_assignment):
        print("Perubahan Cluster Terdeteksi!")
        for idx, row in df.iterrows():
            kecamatan = row['Kecamatan']
            cluster_sebelumnya = previous_cluster_assignment[idx]
            cluster_sekarang = current_cluster_assignment[idx]
            if cluster_sebelumnya != cluster_sekarang:
                print(
                    f"{kecamatan} berpindah dari Cluster {cluster_sebelumnya} ke Cluster {cluster_sekarang}")

    # Simpan hasil cluster saat ini sebagai hasil cluster sebelumnya
    previous_cluster_assignment = current_cluster_assignment

    # Langkah 5: Perbarui pusat cluster
    new_centroids = df.groupby('Cluster')[['Fitur1', 'Fitur2']].mean()

    # Cek konvergensi
    if initial_centroids.equals(new_centroids):
        break
    else:
        initial_centroids = new_centroids.copy()
