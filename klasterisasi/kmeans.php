<?php
require 'vendor/autoload.php';

use Rubix\ML\Clusterers\KMeans;
use Rubix\ML\Datasets\Dataset;
use Rubix\ML\Transformers\NumericStringConverter;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $json_filename = 'data.json';
    $json_content = file_get_contents($json_filename);
    $data = json_decode($json_content, true);

    $type = $_POST['centroid_type']; // "average" or "random"
    $num_clusters = (int)$_POST['num_clusters'];
    $max_iterations = (int)$_POST['max_iterations'];

    $samples = [];
    foreach ($data as $row) {
        $samples[] = array_values($row);
    }

    // Convert samples to a Dataset
    $dataset = new Dataset($samples);

    // Create K-Means instance
    $clusterer = new KMeans($num_clusters, $max_iterations, $type);

    // Train the clusterer
    $clusterer->train($dataset);

    // Get cluster assignments
    $predictions = $clusterer->predict($dataset);

    // Print the cluster assignments
    echo '<h2>K-Means Clustering Results</h2>';
    echo '<table border="1">';
    echo '<tr><th>Data</th><th>Cluster</th></tr>';
    foreach ($predictions as $index => $cluster) {
        echo '<tr><td>' . implode(', ', $data[$index]) . '</td><td>' . $cluster . '</td></tr>';
    }
    echo '</table>';
}
?>

<!DOCTYPE html>
<html>

<head>
    <title>K-Means Clustering</title>
</head>

<body>
    <h2>K-Means Clustering</h2>
    <form action="" method="POST">
        <label for="centroid_type">Centroid Type:</label>
        <select name="centroid_type" id="centroid_type">
            <option value="random">Random</option>
            <option value="mean">Average</option>
        </select><br><br>

        <label for="num_clusters">Number of Clusters:</label>
        <input type="number" name="num_clusters" required><br><br>

        <label for="max_iterations">Max Iterations:</label>
        <input type="number" name="max_iterations" required><br><br>

        <button type="submit">Run K-Means</button>
    </form>
</body>

</html>