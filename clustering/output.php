<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Output K-Means</title>
</head>

<body>
    <?php
    $jsonData = file_get_contents('output_kmeans.json');
    $data = json_decode($jsonData, true);

    $jumlahCluster = $data['Jumlah_Cluster'];
    $metodeInisiasi = $data['Metode_Inisialisasi_Pusat_Cluster'];

    echo "<h1>Clustering Results</h1>";
    echo "<p>Jumlah Cluster: $jumlahCluster</p>";
    echo "<p>Metode Inisialisasi Pusat Cluster: $metodeInisiasi</p>";

    foreach ($data['Iterasi_Clustering'] as $iteration) {
        echo "<hr>";
        echo "<h2>Iterasi " . $iteration['Iterasi'] . "</h2>";

        // Display Pusat Cluster Baru in a table
        echo "<h3>Pusat Cluster Baru</h3>";
        echo "<table border='1'>";
        echo "<tr><th>Cluster</th><th>Value</th></tr>";
        foreach ($iteration['Pusat_Cluster_Baru'] as $kunci => $nilai) {
            foreach ($nilai as $index => $nilai_cluster) {
                echo "<tr><td>Cluster $index</td><td>$nilai_cluster</td></tr>";
            }
        }
        echo "</table>";

        // Display Anggota Cluster in a table
        echo "<h3>Anggota Cluster</h3>";
        echo "<table border='1'>";
        echo "<tr><th>Kecamatan</th><th>Key</th><th>Value</th></tr>";
        foreach ($iteration['Anggota_Cluster'] as $anggota) {
            echo "<tr><td>" . $anggota['kecamatan'] . "</td>";
            foreach ($anggota as $key => $value) {
                if ($key != 'kecamatan') {
                    echo "<td>$key</td><td>$value</td>";
                }
            }
            echo "</tr>";
        }
        echo "</table>";

        // Display Perhitungan Jarak Euclidean in a table
        echo "<h3>Perhitungan Jarak Euclidean</h3>";
        echo "<table border='1'>";
        echo "<tr><th>Key</th><th>Value</th></tr>";
        foreach ($iteration['Perhitungan_Jarak_Euclidean'] as $jarak) {
            foreach ($jarak as $key => $value) {
                echo "<tr><td>$key</td><td>$value</td></tr>";
            }
        }
        echo "</table>";
    }
    ?>

</body>

</html>