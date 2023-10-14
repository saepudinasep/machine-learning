<?php

// Fungsi untuk menghitung jarak Euclidean antara dua titik
function euclideanDistance($point1, $point2)
{
    $sum = 0;
    $dimensions = count($point1);

    for ($i = 0; $i < $dimensions; $i++) {
        $sum += pow($point1[$i] - $point2[$i], 2);
    }

    return sqrt($sum);
}

// Fungsi untuk mengelompokkan data ke dalam cluster
function assignToClusters($data, $centroids)
{
    $clusters = [];

    foreach ($data as $point) {
        $minDistance = INF;
        $closestCluster = null;

        foreach ($centroids as $clusterId => $centroid) {
            $distance = euclideanDistance($point, $centroid);

            if ($distance < $minDistance) {
                $minDistance = $distance;
                $closestCluster = $clusterId;
            }
        }

        $clusters[$closestCluster][] = $point;
    }

    return $clusters;
}

// Fungsi untuk menghitung pusat baru dari setiap cluster
function calculateNewCentroids($clusters)
{
    $newCentroids = [];

    foreach ($clusters as $clusterId => $clusterPoints) {
        $numPoints = count($clusterPoints);
        $dimensions = count($clusterPoints[0]);

        $sum = array_fill(0, $dimensions, 0);

        foreach ($clusterPoints as $point) {
            for ($i = 0; $i < $dimensions; $i++) {
                $sum[$i] += $point[$i];
            }
        }

        $newCentroid = array_map(function ($value) use ($numPoints) {
            return $value / $numPoints;
        }, $sum);

        $newCentroids[$clusterId] = $newCentroid;
    }

    return $newCentroids;
}

// Membaca data dari file JSON
$jsonData = file_get_contents('data.json');
$data = json_decode($jsonData, true);

// Mengambil nilai yang diperlukan dari setiap data
$features = [];
$labelNames = [];
foreach ($data as $index => $entry) {
    $values = [];
    foreach ($entry as $value) {
        $values[] = $value;
    }

    $labelNames[$index] = $values[0]; // Kecamatan berada pada posisi pertama
    $features[] = array_slice($values, 1); // Mengambil nilai setelah kunci pertama (kecamatan)
}

// Jumlah cluster yang diinginkan
$numClusters = 3;

// Inisialisasi pusat awal
$centroids = array_slice($features, 0, $numClusters);

// Iterasi hingga konvergensi
$maxIterations = 100;
for ($iteration = 0; $iteration < $maxIterations; $iteration++) {
    echo "Iterasi $iteration:<br>";

    $clusters = assignToClusters($features, $centroids);
    $newCentroids = calculateNewCentroids($clusters);

    // Menampilkan anggota setiap cluster
    foreach ($clusters as $clusterId => $clusterPoints) {
        echo "Cluster $clusterId:<br>";
        foreach ($clusterPoints as $index => $point) {
            echo "Kecamatan: {$labelNames[$index]} - Ijazah: {$data[$index]['Ijazah']} - Status Kepegawaian: {$data[$index]['Status Kepegawaian']} - Sertifikasi: {$data[$index]['Sertifikasi']}<br>";
        }
        echo "<br>";
    }

    // Cek konvergensi
    $converged = true;
    foreach ($centroids as $clusterId => $centroid) {
        if (euclideanDistance($centroid, $newCentroids[$clusterId]) > 0.0001) {
            $converged = false;
            break;
        }
    }

    if ($converged) {
        echo "Konvergensi tercapai pada iterasi $iteration.<br>";
        break;
    }

    $centroids = $newCentroids;
    echo "<br>";
}

// Menampilkan hasil cluster
foreach ($clusters as $clusterId => $clusterPoints) {
    echo "Cluster $clusterId:<br>";
    foreach ($clusterPoints as $index => $point) {
        echo "Kecamatan: {$labelNames[$index]} - Ijazah: {$data[$index]['Ijazah']} - Status Kepegawaian: {$data[$index]['Status Kepegawaian']} - Sertifikasi: {$data[$index]['Sertifikasi']}<br>";
    }
    echo "<br>";
}
