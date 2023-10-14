import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import random

# Membuat contoh data
random.seed(42)
data = {'Fitur1': [random.uniform(0, 100) for _ in range(20)],
        'Fitur2': [random.uniform(0, 100) for _ in range(20)]}
df = pd.DataFrame(data)

# Langkah 1: Tentukan jumlah cluster (k)
k = 3

# Langkah 2: Inisialisasi pusat cluster secara acak
random.seed(42)
initial_centroids = df.sample(n=k)

# Tampilkan inisialisasi pusat cluster
print("Iterasi 0:")
print("Pusat Cluster Awal:")
print(initial_centroids)

# Langkah 3-5: Iterasi hingga konvergensi
max_iterations = 100
for iteration in range(max_iterations):
    # Langkah 3: Hitung jarak antara titik dengan centroid menggunakan Euclidean Distance
    df['Distance_to_C1'] = np.sqrt((df['Fitur1'] - initial_centroids.iloc[0]['Fitur1'])**2 +
                                   (df['Fitur2'] - initial_centroids.iloc[0]['Fitur2'])**2)

    df['Distance_to_C2'] = np.sqrt((df['Fitur1'] - initial_centroids.iloc[1]['Fitur1'])**2 +
                                   (df['Fitur2'] - initial_centroids.iloc[1]['Fitur2'])**2)

    df['Distance_to_C3'] = np.sqrt((df['Fitur1'] - initial_centroids.iloc[2]['Fitur1'])**2 +
                                   (df['Fitur2'] - initial_centroids.iloc[2]['Fitur2'])**2)

    # Langkah 4: Kelompokkan objek berdasarkan jarak ke centroid terdekat
    df['Cluster'] = df[['Distance_to_C1',
                        'Distance_to_C2', 'Distance_to_C3']].idxmin(axis=1)
    df['Cluster'] = df['Cluster'].apply(lambda x: int(x[-1]))

    # Langkah 5: Perbarui pusat cluster
    new_centroids = df.groupby('Cluster')[['Fitur1', 'Fitur2']].mean()

    # Tampilkan hasil anggota setiap iterasi
    print(f"\nIterasi {iteration + 1}:")
    print("Pusat Cluster Baru:")
    print(new_centroids)
    print("Anggota Cluster:")
    print(df[['Fitur1', 'Fitur2', 'Cluster']])

    # Cek konvergensi
    if initial_centroids.equals(new_centroids):
        break
    else:
        initial_centroids = new_centroids.copy()
