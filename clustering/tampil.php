<!DOCTYPE html>
<html>

<head>
    <title>K-Means Output</title>
    <style>
        table {
            border-collapse: collapse;
            width: 80%;
            margin: 20px auto;
        }

        th,
        td {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }

        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
    </style>
</head>

<body>
    <?php
    // Read the JSON file
    $jsonData = file_get_contents('kmeans_output.json');

    // Decode the JSON data
    $data = json_decode($jsonData, true);

    if ($data === null) {
        die('Error decoding JSON data');
    }

    foreach ($data as $iterationInfo) {
        echo "<h2>Iteration: " . ($iterationInfo['Iteration'] == 1 ? 1 : $iterationInfo['Iteration'] - 1) . "</h2>";

        echo "<table>";
        echo "<tr><th>Feature</th>";

        // Determine the unique clusters present in the data
        $uniqueClusters = [];
        foreach ($iterationInfo['Initial_Centroids'] as $feature => $clusterValues) {
            foreach ($clusterValues as $cluster => $centroidValue) {
                if (!in_array($cluster, $uniqueClusters)) {
                    $uniqueClusters[] = $cluster;
                }
            }
        }

        // Generate table headers for each unique cluster
        foreach ($uniqueClusters as $cluster) {
            $clusterNumber = ($iterationInfo['Iteration'] == 1) ? $cluster + 1 : $cluster; // Menambahkan 1 hanya pada iterasi pertama
            echo "<th>Cluster $clusterNumber</th>";
        }

        echo "</tr>";

        foreach ($iterationInfo['Initial_Centroids'] as $feature => $clusterValues) {
            echo "<tr>";
            echo "<td>$feature</td>";
            foreach ($clusterValues as $cluster => $centroidValue) {
                echo "<td>$centroidValue</td>";
            }
            echo "</tr>";
        }

        echo "</table>";

        echo "<h3>Cluster Info:</h3>";
        echo "<table>";
        echo "<tr><th>Kecamatan</th><th>Ijazah</th><th>Status Kepegawaian</th><th>Sertifikasi</th><th>Cluster</th></tr>";
        foreach ($iterationInfo['Cluster_Info'] as $clusterData) {
            echo "<tr>";
            echo "<td>" . $clusterData['kecamatan'] . "</td>";
            echo "<td>" . $clusterData['Ijazah'] . "</td>";
            echo "<td>" . $clusterData['Status Kepegawaian'] . "</td>";
            echo "<td>" . $clusterData['Sertifikasi'] . "</td>";
            echo "<td>" . $clusterData['Cluster'] . "</td>";
            echo "</tr>";
        }
        echo "</table>";

        echo "<hr>";
    }
    ?>
</body>

</html>