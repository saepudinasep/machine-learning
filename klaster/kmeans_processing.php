<?php

if (isset($_POST["num_clusters"], $_POST["max_iterations"], $_POST["centroid_type"])) {
    $numClusters = $_POST["num_clusters"];
    $maxIterations = $_POST["max_iterations"];
    $centroid_type = $_POST["centroid_type"];

    // Lanjutkan dengan pemrosesan variabel yang sudah diatur
} else {
    // Handle jika variabel-post tidak diatur
    header("Location: k-klaster.php");
    exit; // Pastikan untuk keluar dari skrip setelah mengarahkan
}

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
// $numClusters = 3;

// Inisialisasi pusat awal
// $centroids = array_slice($features, 0, $numClusters);
if ($centroid_type === "average") {
    $centroids = array_slice($features, 0, $numClusters);
} else {
    // Inisialisasi pusat klaster secara acak
    $keys = array_rand($features, $numClusters);
    $centroids = array_map(function ($key) use ($features) {
        return $features[$key];
    }, $keys);
}



?>

<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Klasterisasi Guru</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
</head>

<body>
    <!-- <div class="container"> -->
    <nav class="navbar navbar-expand-lg bg-light">
        <div class="container">
            <a class="navbar-brand" href="#">WCTV</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="index.php">Dashboard</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="klaster.php">K-Means</a>
                    </li>
                </ul>
                <ul class="navbar-nav">
                    <li class="nav-item d-flex">
                        <a class="nav-link" href="">Logout</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    <div class="container mt-3">
        <div class="row">
            <div class="col-md-4 col-4 list-group">
                <a href="#" class="list-group-item list-group-item-action">Dataset</a>
                <a href="k-klaster.php" class="list-group-item list-group-item-action">Tentukan Klaster</a>
                <a href="k-means.php" class="list-group-item list-group-item-action active" aria-current="true">Proses K-Means</a>
                <a href="elbow.php" class="list-group-item list-group-item-action">Evaluasi DBI</a>
                <a href="hasil.php" class="list-group-item list-group-item-action">Hasil K-Means</a>
            </div>


            <div class="col-md-8 col-8">
                <?php
                function getRandomColor()
                {
                    return sprintf('#%06X', mt_rand(0, 0xFFFFFF));
                }

                // Iterasi hingga konvergensi
                // $maxIterations = 100;
                $jumlahKunci = count(array_keys($data));
                ?>
                <!-- <div class="mb-3"></div> -->
                <?php
                // start iteration
                for ($iteration = 0; $iteration < $maxIterations; $iteration++) {
                    // Capture the iteration data
                    $iterationData = [];
                    $iterationColor = getRandomColor();
                    // Tidak memberikan margin atas pada tabel pertama
                    $tableStyle = ($iteration === 0) ? '' : 'margin-top: 100px;';
                ?>
                    <table class="table" style="<?= $tableStyle; ?>">
                        <thead class="table-primary">
                            <th colspan="<?= $jumlahKunci; ?>" style="color: <?= $iterationColor; ?>">Iterasi ke <?= $iteration; ?></th>
                        </thead>
                        <tbody>
                            <tr>
                                <?php
                                $keys = array_keys($data[0]);
                                foreach ($keys as $key) {
                                    echo "<th>$key</th>";
                                }
                                ?>
                                <th>Cluster</th>
                            </tr>
                            <?php

                            $clusters = assignToClusters($features, $centroids);
                            $newCentroids = calculateNewCentroids($clusters);
                            ?>
                            <?php foreach ($clusters as $clusterId => $clusterPoints) : ?>
                                <?php
                                $clusterColor = getRandomColor();
                                ?>
                                <?php foreach ($clusterPoints as $index => $point) : ?>
                                    <tr>
                                        <?php foreach ($data[$index] as $key => $value) : ?>
                                            <td><?= $value; ?></td>
                                        <?php endforeach; ?>
                                        <td style="color: <?= $clusterColor; ?>"><?= $clusterId; ?></td>
                                    </tr>
                                <?php endforeach; ?>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                <?php



                    // Cek konvergensi
                    $converged = true;
                    foreach ($centroids as $clusterId => $centroid) {
                        if (euclideanDistance($centroid, $newCentroids[$clusterId]) > 0.0001) {
                            $converged = false;
                            break;
                        }
                    }

                    if ($converged) {
                        // echo "Konvergensi tercapai pada iterasi $iteration.<br>";
                        break;
                    }

                    $centroids = $newCentroids;

                    // Capture the iteration data
                    $iterationData['iteration'] = $iteration;
                    $iterationData['clusters'] = $clusters;
                    $iterationData['centroids'] = $centroids;

                    // Add iteration data to the results array
                    $iterationResults[] = $iterationData;
                }
                // end iterations
                ?>
                <?php

                // Convert the iteration results array to JSON format
                $jsonData = json_encode($iterationResults, JSON_PRETTY_PRINT);

                // Define the path for the JSON file
                $jsonFilePath = 'iteration_results.json';

                // Save the JSON data to the file
                $fileWriteResult = file_put_contents($jsonFilePath, $jsonData);

                // if ($fileWriteResult !== false) {
                //     echo "Iteration results saved to $jsonFilePath successfully.";
                // } else {
                //     echo "Error saving iteration results to $jsonFilePath.";
                // }
                ?>
                <h1>Konvergensi tercapat pada iterasi <?= $iteration; ?></h1>
            </div>
        </div>



        <table class="table">
            <thead>
                <tr>
                    <?php
                    $keys = array_keys($data[0]);
                    foreach ($keys as $key) {
                        echo "<th>$key</th>";
                    }
                    ?>
                    <th>Cluster</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($clusters as $clusterId => $clusterPoints) : ?>
                    <?php foreach ($clusterPoints as $index => $point) : ?>
                        <tr>
                            <?php foreach ($data[$index] as $key => $value) : ?>
                                <td><?= $value; ?></td>
                            <?php endforeach; ?>
                            <td><?= $clusterId; ?></td>
                        </tr>
                    <?php endforeach; ?>
                <?php endforeach; ?>
            </tbody>
        </table>
        <?php

        $clusteredData = [];

        foreach ($clusters as $clusterId => $clusterPoints) {
            foreach ($clusterPoints as $index => $point) {
                $clusteredData[] = array_merge($data[$index], ["Cluster" => $clusterId]);
            }
        }
        print_r($clusteredData);

        // // Convert the cluster data to JSON format
        // $jsonDataCluster = json_encode($clusterData, JSON_PRETTY_PRINT);

        // // Define the path for the JSON file
        // $jsonFilePathCluster = 'cluster_results.json';

        // // Save the JSON data to the file
        // $fileWriteResult = file_put_contents($jsonFilePathCluster, $jsonDataCluster);

        // if ($fileWriteResult !== false) {
        //     echo "Iteration results saved to $jsonFilePathCluster successfully.";
        // } else {
        //     echo "Error saving iteration results to $jsonFilePath.";
        // }

        ?>
    </div>
    <!-- </div> -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
</body>

</html>