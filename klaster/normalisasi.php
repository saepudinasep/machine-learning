<?php
// Baca isi file JSON
$json_data = file_get_contents('data.json');
$data = json_decode($json_data, true);

// Menghitung mean dan standard deviation untuk setiap kolom
foreach ($data as $item) {
    foreach ($item as $key => $value) {
        if (!isset($mean_values[$key])) {
            $mean_values[$key] = 0;
            $std_dev_values[$key] = 0;
            $count_values[$key] = 0;
        }

        // Cek tipe data dan tambahkan hanya jika tipe datanya numerik
        if (is_numeric($value)) {
            $mean_values[$key] += $value;
            $count_values[$key]++;
        }
    }
}

$column_count = count($data);
foreach ($mean_values as $key => $value) {
    if ($count_values[$key] > 0) {
        $mean_values[$key] /= $count_values[$key];

        foreach ($data as $item) {
            if (isset($item[$key]) && is_numeric($item[$key])) {
                $std_dev_values[$key] += pow($item[$key] - $mean_values[$key], 2);
            }
        }

        if ($count_values[$key] > 1) {
            $std_dev_values[$key] = sqrt($std_dev_values[$key] / ($count_values[$key] - 1));
        }
    }
}


// Normalisasi data
$normalized_data = array();
foreach ($data as $item) {
    $normalized_item = array();
    foreach ($item as $key => $value) {
        // Cek tipe data dan pastikan variabel $mean_values dan $std_dev_values memiliki nilai numerik
        if (is_numeric($value) && isset($mean_values[$key]) && isset($std_dev_values[$key]) && is_numeric($mean_values[$key]) && is_numeric($std_dev_values[$key]) && $std_dev_values[$key] != 0) {
            $normalized_item[$key] = ($value - $mean_values[$key]) / $std_dev_values[$key];
        } else {
            $normalized_item[$key] = $value; // Jika ada masalah, gunakan nilai asli
        }
    }
    $normalized_data[] = $normalized_item;
}

?>
<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Klasterisasi Guru</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
    <!-- ... -->
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
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
                <a href="klaster.php" class="list-group-item list-group-item-action">Data Awal</a>
                <a href="normalisasi.php" class="list-group-item list-group-item-action active" aria-current="true">Normalisasi Data</a>
                <a href="elbow.php" class="list-group-item list-group-item-action">Elbow Method</a>
                <a href="centroid.php" class="list-group-item list-group-item-action">Centroid & Loop</a>
                <a href="k-means.php" class="list-group-item list-group-item-action">Proses K-Means</a>
                <a href="hasil.php" class="list-group-item list-group-item-action">Hasil K-Means</a>
            </div>
            <!-- </div> -->


            <div class="col-md-8 col-8">
                <h3 style="text-align: center;">Normalisasi Data</h3>
                <!-- Tombol untuk menyimpan hasil normalisasi ke dalam normalisasi.json -->
                <form method="post">
                    <button type="submit" name="save" class="btn btn-primary">Normalize</button>
                </form>

                <?php
                // Simpan hasil normalisasi ke dalam normalisasi.json
                $normalized_json = json_encode($normalized_data, JSON_PRETTY_PRINT);
                file_put_contents('normalisasi.json', $normalized_json);

                // Tindakan saat tombol "Simpan" ditekan
                if (isset($_POST['save'])) {
                    // Tulis data ke file normalisasi.json
                    file_put_contents('normalisasi.json', $normalized_json);

                    // Menampilkan pemberitahuan SweetAlert
                    echo '<script>';
                    echo 'Swal.fire("Data berhasil di Normalisasi", "Silahkan Lanjut ke tahap berikutnya", "success");';
                    echo '</script>';
                }
                ?>

                <!-- Tabel HTML dengan data dinormalisasi -->
                <table class="table mt-5">
                    <thead>
                        <tr>
                            <?php foreach ($normalized_data[0] as $key => $value) { ?>
                                <th scope="col"><?php echo ucfirst($key); ?></th>
                            <?php } ?>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($normalized_data as $index => $row) { ?>
                            <tr>
                                <?php foreach ($row as $value) { ?>
                                    <td><?php echo $value; ?></td>
                                <?php } ?>
                            </tr>
                        <?php } ?>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
</body>

</html>