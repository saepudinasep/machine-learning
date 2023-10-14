<!DOCTYPE html>
<html>

<head>
    <title>Hasil K-Means Clustering</title>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }

        th,
        td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }

        th {
            background-color: #f2f2f2;
        }
    </style>
</head>

<body>
    <h1>Hasil K-Means Clustering</h1>
    <?php
    // Baca isi file JSON
    $jsonData = file_get_contents('kmeans_output.json');

    // Ubah JSON menjadi array PHP
    $data = json_decode($jsonData, true);

    // Tampilkan data dalam bentuk tabel
    foreach ($data as $iterationInfo) {
        echo "<h2>Iterasi: " . $iterationInfo['Iteration'] . "</h2>";
        echo "<table>";
        echo "<tr><th>Cluster</th><th>Initial Centroids</th></tr>";
        foreach ($iterationInfo['Initial_Centroids'] as $cluster => $centroid) {
            echo "<tr><td>Cluster $cluster</td><td>" . implode(', ', $centroid) . "</td></tr>";
        }
        echo "</table>";

        echo "<table>";
        echo "<tr><th>Data Point</th><th>Cluster Assignment</th></tr>";
        foreach ($iterationInfo['Cluster_Assignments'] as $dataPoint => $cluster) {
            echo "<tr><td>Data Point $dataPoint</td><td>Cluster $cluster</td></tr>";
        }
        echo "</table>";

        echo "<table>";
        echo "<tr><th>Data Point</th><th>Cluster Info</th></tr>";
        foreach ($iterationInfo['Cluster_Info'] as $dataPointInfo) {
            echo "<tr><td>Data Point</td><td>";
            foreach ($dataPointInfo as $key => $value) {
                echo "$key: $value, ";
            }
            echo "</td></tr>";
        }
        echo "</table>";

        echo "<table>";
        echo "<tr><th>Data Point</th><th>Euclidean Distances</th></tr>";
        foreach ($iterationInfo['Euclidean_Distances'] as $dataPointDistances) {
            echo "<tr><td>Data Point</td><td>";
            foreach ($dataPointDistances as $cluster => $distance) {
                echo "Cluster $cluster: $distance, ";
            }
            echo "</td></tr>";
        }
        echo "</table>";
    }
    ?>
</body>

</html>