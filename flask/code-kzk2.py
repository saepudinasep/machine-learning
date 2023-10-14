import numpy as np

# Menginisialisasi array data
data = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])

# Menginisialisasi centroid awal
centroid_1 = np.array([0, 0])
centroid_2 = np.array([9, 9])

# Melakukan perulangan hingga konvergen atau batas iterasi tertentu
max_iter = 10
for i in range(max_iter):
    # Membuat list kosong untuk menyimpan jarak antara setiap titik dengan centroid yang terdekat
    distances_centroid_1 = []
    distances_centroid_2 = []

    # Menghitung jarak tiap titik ke masing-masing centroid menggunakan rumus Euclidean dan menyimpannya dalam list distances_centroid_1 dan distances_centroid_2
    for point in data:
        distance_to_centroid_1 = np.linalg.norm(point - centroid_1)
        distance_to_centroid_2 = np.linalg.norm(point - centroid_2)
        distances_centroid_1.append(distance_to_centroid_1)
        distances_centroid_2.append(distance_to_centroid_2)

    # Menetapkan label cluster berdasarkan jarak terdekat ke centroid (label_cluster=0: anggota kluster pertama; label_cluster=1: anggota kluster kedua)
    labels_cluster = []
    for dist_cen1, dist_cen2 in zip(distances_centroid[0]):
        if dist_cen < dist_cen:
            labels_cluster.append(0)
        else:
            labels_cluster.append(1)

    # Memperbarui posisi centroid dengan mengambil rata-rata dari setiap kluster
    cluster_1 = data[np.array(labels_cluster) == 0]
    cluster_2 = data[np.array(labels_cluster) == 1]

    centroid_1 = np.mean(cluster_1, axis=0)
    centroid_2 = np.mean(cluster_2, axis=0)

# Menampilkan hasil perulangan dan label kluster terakhir
print("Hasil Perulangan:")
for point, label in zip(data, labels_cluster):
    print(f"{point} - Cluster {label}")
