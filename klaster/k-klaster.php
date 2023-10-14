<?php

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
                        <a class="nav-link" href="index.php">Dashboard</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="klaster.php">K-Means</a>
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
    <!-- </div> -->


    <h3 style="text-align: left;" class="m-3">Metode K-Means Elbow</h3><br>
    <div class="container">
        <div class="row">
            <!-- <div class="col-md-4 col-4"> -->
            <div class="col-md-4 col-4 list-group">
                <a href="klaster.php" class="list-group-item list-group-item-action">Dataset</a>
                <a href="k-klaster.php" class="list-group-item list-group-item-action active" aria-current="true">Tentukan Klaster</a>
                <a href="k-means.php" class="list-group-item list-group-item-action">Proses K-Means</a>
                <a href="elbow.php" class="list-group-item list-group-item-action">Evaluasi DBI</a>
                <a href="hasil.php" class="list-group-item list-group-item-action">Hasil K-Means</a>
            </div>
            <!-- </div> -->


            <div class="col-md-8 col-8">
                <h3 style="text-align: center;">Tentukan Klaster</h3>

                <form method="post" action="kmeans_processing.php">
                    <div class="mb-3">
                        <label for="centroid_type" class="form-label">Tipe Centroid:</label>
                        <select name="centroid_type" id="centroid_type" class="form-select">
                            <option value="mean">Rata-rata</option>
                            <option value="random">Random</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="num_clusters" class="form-label">Jumlah Klaster:</label>
                        <input type="number" name="num_clusters" id="num_clusters" class="form-control" min="1" required>
                    </div>
                    <div class="mb-3">
                        <label for="max_iterations" class="form-label">Max Perulangan:</label>
                        <input type="number" name="max_iterations" id="max_iterations" class="form-control" min="1" required>
                    </div>
                    <input type="submit" value="Submit" class="btn btn-primary">
                </form>


                <?php if (isset($json_filename)) : ?>
                    <?php
                    $json_content = file_get_contents($json_filename);
                    $json_data = json_decode($json_content, true);
                    ?>

                    <?php if ($json_data) : ?>
                        <table class="table">
                            <thead>
                                <tr>
                                    <?php foreach ($headerValues as $header) : ?>
                                        <th scope="col"><?= $header; ?></th>
                                    <?php endforeach; ?>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($json_data as $row) : ?>
                                    <tr>
                                        <?php foreach ($headerValues as $header) : ?>
                                            <td scope="row"><?= $row[$header]; ?></td>
                                        <?php endforeach; ?>
                                    </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    <?php endif; ?>
                <?php endif; ?>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
</body>

</html>