import numpy as np
import pandas as pd
import json
from sklearn.cluster import KMeans

# Membaca data dari file Excel
# Gantilah 'contoh.xlsx' dengan nama file Excel Anda
df = pd.read_excel('Dataset Bahan Skripsi.xlsx')

# Pilih kolom yang ingin digunakan untuk pengelompokan menggunakan iloc
data_for_clustering = df.iloc[:, 1:]

# Meminta pengguna untuk memasukkan jumlah cluster (k)
k = int(input("Masukkan jumlah cluster (k): "))

# Meminta pengguna untuk memilih metode inisialisasi pusat cluster
init_method = input(
    "Pilih metode inisialisasi pusat cluster (rata-rata/random): ")

# Gantilah ini
if init_method == "rata-rata":
    # Inisialisasi pusat cluster dengan rata-rata setiap cluster
    initial_centroids = data_for_clustering.groupby(
        np.random.randint(0, k, len(data_for_clustering))).mean()
else:
    # Inisialisasi pusat cluster secara acak
    initial_centroids = data_for_clustering.sample(n=k)

# Inisialisasi variabel untuk menyimpan informasi cluster pada setiap iterasi
previous_clusters = None

# List untuk menyimpan informasi dari setiap iterasi
iterations_info = []

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

    # Menyimpan informasi iterasi saat ini
    iteration_info = {
        'Iteration': iteration + 1,
        'Initial_Centroids': initial_centroids.to_dict(),
        'Cluster_Assignments': df['Cluster'].tolist(),
        'Cluster_Info': df.to_dict(orient='records'),
        'Euclidean_Distances': distance_df.to_dict(orient='records')
    }

    iterations_info.append(iteration_info)

    # Membandingkan dengan informasi cluster pada iterasi sebelumnya
    if previous_clusters is not None and current_clusters.equals(previous_clusters):
        print(f"\nIterasi {iteration + 1}: Konvergensi tercapai.")
        # Menampilkan hasil cluster terakhir ketika iterasi berakhir
        print("\nHasil Cluster Terakhir:")
        print(df)

        break
    else:
        print(f"\nIterasi {iteration + 1}:")
        print("Pusat Cluster Baru:")
        print(initial_centroids)
        print("Anggota Cluster:")
        print(df)
        print("Hasil Perhitungan Euclidean Distance:")
        print(distance_df)
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

# Simpan informasi dari setiap iterasi ke dalam file JSON
output_filename = 'kmeans_output.json'

with open(output_filename, 'w') as output_file:
    json.dump(iterations_info, output_file)


print(
    f'Informasi iterasi dan hasil clustering disimpan ke dalam {output_filename}')
