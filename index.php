<?php
require 'vendor/autoload.php'; // Pastikan path menuju autoload.php benar

use PhpOffice\PhpSpreadsheet\IOFactory;

// Fungsi untuk membaca data dari file Excel
function bacaDataDariExcel($file)
{
    $spreadsheet = IOFactory::load($file);
    $sheet = $spreadsheet->getActiveSheet();
    $data = [];

    foreach ($sheet->getRowIterator() as $row) {
        $rowData = [];
        foreach ($row->getCellIterator() as $cell) {
            $rowData[] = $cell->getValue();
        }
        $data[] = $rowData;
    }

    return $data;
}

// Fungsi perhitungan Euclidean Distance
function euclideanDistance($data1, $data2)
{
    $distance = 0;
    for ($i = 0; $i < count($data1); $i++) {
        // Pastikan mengkonversi nilai ke tipe data numerik sebelum perhitungan
        $value1 = (float)$data1[$i];
        $value2 = (float)$data2[$i];
        $distance += pow($value1 - $value2, 2);
    }
    return sqrt($distance);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_FILES['excel_file'])) {
        $uploadedFile = $_FILES['excel_file']['tmp_name'];
        $data = bacaDataDariExcel($uploadedFile);

        // Proses pengolahan data dan clustering di sini
        $clusterCount = $_POST['cluster_count'];

        // Inisialisasi data dan variabel centroid
        $dataPoints = []; // Array untuk menyimpan data mahasiswa
        $centroids = [];  // Array untuk menyimpan nilai centroid

        foreach ($data as $row) {
            // Misalnya, jika kolom pertama adalah tanggungan, kolom kedua k_pekerjaan, dan kolom ketiga k_penghasilan
            $dataPoints[] = [$row[0], $row[1], $row[2]];
        }


        // Memilih nilai centroid awal berdasarkan tipe yang dipilih
        if ($_POST['centroid_type'] === 'rata_rata') {
            // Menggunakan nilai rata-rata dari data sebagai centroid awal
            for ($i = 0; $i < $clusterCount; $i++) {
                $randomIndex = array_rand($dataPoints);
                $centroids[$i] = $dataPoints[$randomIndex];
            }
        } else if ($_POST['centroid_type'] === 'random') {
            // Menggunakan nilai centroid acak sebagai centroid awal
            for ($i = 0; $i < $clusterCount; $i++) {
                $centroids[$i] = [$rand1, $rand2, $rand3]; // Isi dengan nilai acak
            }
        }

        $loop = 0;
        $status = 'false';
        $result = []; // Hasil clustering per iterasi
        while ($status === 'false') {
            // Perhitungan K-Means
            $clusterakhir = []; // Array untuk menyimpan hasil cluster per iterasi

            foreach ($dataPoints as $point) {
                // Perhitungan jarak ke semua centroid
                $distances = [];
                foreach ($centroids as $centroid) {
                    $distances[] = euclideanDistance($point, $centroid);
                }

                // Menentukan cluster berdasarkan jarak terdekat
                $minDistance = min($distances);
                $closestCluster = array_search($minDistance, $distances);
                $clusterakhir[] = 'C' . ($closestCluster + 1);
            }

            // // Simpan hasil per iterasi ke dalam $result
            // $result[] = $clusterakhir;

            // Update centroid baru
            // Update centroid baru
            $newCentroids = []; // Array untuk menyimpan centroid baru

            for ($i = 0; $i < $clusterCount; $i++) {
                $clusterPoints = []; // Array untuk menyimpan data dalam satu cluster
                for ($j = 0; $j < count($clusterakhir); $j++) {
                    if ($clusterakhir[$j] === 'C' . ($i + 1)) {
                        $clusterPoints[] = $dataPoints[$j];
                    }
                }

                if (!empty($clusterPoints)) {
                    $newCentroid = [];
                    $clusterSize = count($clusterPoints);

                    for ($k = 0; $k < count($dataPoints[0]); $k++) {
                        $sum = 0;
                        foreach ($clusterPoints as $point) {
                            $sum += (float)$point[$k]; // Konversi ke float sebelum penjumlahan
                        }
                        $newCentroid[] = $sum / $clusterSize;
                    }


                    $newCentroids[$i] = $newCentroid;
                } else {
                    $newCentroids[$i] = $centroids[$i]; // Jika cluster kosong, gunakan centroid sebelumnya
                }
            }

            $centroids = $newCentroids; // Mengganti centroid lama dengan yang baru


            // Cek kondisi berhenti
            // Cek kondisi berhenti
            $stopCondition = true;
            $threshold = 0.001; // Ganti dengan nilai ambang batas yang sesuai

            for ($i = 0; $i < $clusterCount; $i++) {
                if (euclideanDistance($centroids[$i], $newCentroids[$i]) > $threshold) {
                    $stopCondition = false;
                    break;
                }
            }

            if ($stopCondition) {
                $status = 'true'; // Berhenti jika kondisi terpenuhi
            }


            $result[] = $clusterakhir; // Menyimpan hasil clustering per iterasi
            $loop++;
        }
    }
}
?>

<!DOCTYPE html>
<html>

<head>
    <title>K-Means Clustering</title>
</head>

<body>
    <h1>K-Means Clustering</h1>
    <form method="POST" enctype="multipart/form-data">
        <label for="excel_file">Upload Excel File:</label>
        <input type="file" name="excel_file" accept=".xls,.xlsx" required>
        <br>
        <label for="cluster_count">Jumlah Cluster:</label>
        <input type="number" name="cluster_count" min="2" required>
        <br>
        <label for="centroid_type">Tipe Centroid:</label>
        <select name="centroid_type">
            <option value="rata_rata">Nilai rata-rata</option>
            <option value="random">Random centroid</option>
        </select>
        <br>
        <button type="submit">Proses</button>
    </form>

    <?php
    // Menampilkan hasil clustering setiap iterasi
    if (isset($result)) {
        echo '<h2>Hasil Clustering</h2>';
        foreach ($result as $iterasi => $clusters) {
            echo '<p>Iterasi ke-' . ($iterasi + 1) . ': ' . implode(', ', $clusters) . '</p>';
        }
    }
    ?>
</body>

</html>