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


# Initialize a list to store information for each iteration
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

    # Collect information for this iteration
    iteration_info = {
        'Iterasi': iteration + 1,
        'Pusat_Cluster_Baru': initial_centroids.to_dict(),
        'Anggota_Cluster': df.to_dict(orient='records'),
        'Perhitungan_Jarak_Euclidean': distance_df.to_dict(orient='records')
    }

    iterations_info.append(iteration_info)

    # Membandingkan dengan informasi cluster pada iterasi sebelumnya
    if previous_clusters is not None and current_clusters.equals(previous_clusters):
        iteration_message = f"\nIterasi {iteration + 1}: Konvergensi tercapai."
        cluster_result = "\nHasil Cluster Terakhir:\n" + df.to_string()
        print(iteration_message)
        print(cluster_result)

        # Collect information for this iteration
        hasil_info = []
        hasil_info = {
            'Iterasi_Pesan': iteration + 1,
            'Hasil_Cluster_Terakhir': df.to_dict(orient='records')
        }

        # Save this information to a JSON file after each iteration
        file_hasil = 'hasil_akhir.json'
        with open(file_hasil, 'w') as file:
            json.dump(hasil_info, file, indent=2)

        break
    else:
        print(f"\nIterasi {iteration + 1}:")
        print("Pusat Cluster Baru:")
        print(initial_centroids)
        print("Anggota Cluster:")
        print(df)
        print("Hasil Perhitungan Jarak Euclidean:")
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
output_filename = 'output_kmeans.json'

final_result = {
    'Jumlah_Cluster': k,
    'Metode_Inisialisasi_Pusat_Cluster': init_method,
    'Iterasi_Clustering': iterations_info
}

with open(output_filename, 'w') as output_file:
    # Use indent to format the JSON for readability
    json.dump(final_result, output_file, indent=4)

print(
    f'Informasi iterasi dan hasil clustering disimpan ke dalam {output_filename}')
