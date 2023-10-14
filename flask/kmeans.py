import pandas as pd
from sklearn.cluster import KMeans

# Membaca data dari file CSV (misalnya 'data.csv')
data = pd.read_csv('data.csv', delimiter=';')

# Mengambil kolom yang akan digunakan dalam klasterisasi
X = data[['Nilai Matematika', 'Nilai Bahasa Inggris', 'Nilai IPA']]

# Menentukan jumlah cluster yang diinginkan
n_clusters = 3

# Membuat objek k-means dan melakukan klasterisasi
kmeans = KMeans(n_clusters=n_clusters)
kmeans.fit(X)

# Mendapatkan label hasil klasterisasi untuk setiap data point
labels = kmeans.labels_

# Menambahkan kolom "label" ke dataframe sebagai hasil klasterisasi
data['label'] = labels
# Melihat hasil iterasi dan nilai inersia pada setiap iterasinya
print("Hasil Cluster:")
for i in range(len(kmeans.cluster_centers_)):
    print(f"Cluster ke-{i+1}:")
    print(f"Centroid: {kmeans.cluster_centers_[i]}")
    print(f"Inersia: {kmeans.inertia_}")
    # Memfilter baris berdasarkan label/kluster saat ini dan menyimpannya dalam dataframe baru
    current_cluster_data = data[data['label'] == i].copy()
    # Set index ulang agar dimulai dari 0 pada setiap iterasi menggunakan reset_index()
    current_cluster_data.reset_index(drop=True, inplace=True)
    print(current_cluster_data)
    print()

# Melihat hasil klasterisasi pada dataframe utuhnya
print("Dataframe Hasil Klasterisasi:")
print(data)
# print(data)
