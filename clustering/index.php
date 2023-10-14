<?php
$jsonString = file_get_contents('output_kmeans.json');
$data = json_decode($jsonString, true);
?>

<!DOCTYPE html>
<html>

<head>
    <title>Data JSON dalam Tabel</title>
</head>

<body>
    <h1>Data JSON dalam Tabel</h1>

    <?php foreach ($data['Iterasi_Clustering'] as $iterasi) : ?>
        <h2>Iterasi: <?php echo $iterasi['Iterasi']; ?></h2>

        <!-- Tabel untuk Pusat Cluster Baru -->
        <h3>Pusat Cluster Baru</h3>
        <table border="1">
            <tr>
                <th>Fitur</th>
                <?php
                $firstFeature = reset($iterasi['Pusat_Cluster_Baru']); // Ambil salah satu fitur pertama sebagai referensi 
                $counter = 1;
                ?>
                <?php foreach ($firstFeature as $kunci => $nilai) : ?>
                    <th>Cluster <?php echo $counter; ?></th>
                <?php
                    $counter++;
                endforeach; ?>
            </tr>
            <?php foreach ($iterasi['Pusat_Cluster_Baru'] as $kunciBaris => $baris) : ?>
                <tr>
                    <td><?php echo $kunciBaris; ?></td>
                    <?php foreach ($baris as $kunciKolom => $nilaiKolom) : ?>
                        <td><?php echo $nilaiKolom; ?></td>
                    <?php endforeach; ?>
                </tr>
            <?php endforeach; ?>
        </table>


        <!-- Tabel fleksibel untuk Anggota Cluster -->
        <h3>Anggota Cluster</h3>
        <table border="1">
            <tr>
                <?php foreach ($iterasi['Anggota_Cluster'][0] as $key => $value) : ?>
                    <th><?php echo $key; ?></th>
                <?php endforeach; ?>
            </tr>
            <?php foreach ($iterasi['Anggota_Cluster'] as $anggota) : ?>
                <tr>
                    <?php foreach ($anggota as $value) : ?>
                        <td><?php echo $value; ?></td>
                    <?php endforeach; ?>
                </tr>
            <?php endforeach; ?>
        </table>

        <!-- Tabel fleksibel untuk Perhitungan Jarak Euclidean -->
        <h3>Perhitungan Jarak Euclidean</h3>
        <table border="1">
            <tr>
                <?php foreach ($iterasi['Perhitungan_Jarak_Euclidean'][0] as $key => $value) : ?>
                    <th><?php echo $key; ?></th>
                <?php endforeach; ?>
            </tr>
            <?php foreach ($iterasi['Perhitungan_Jarak_Euclidean'] as $jarak) : ?>
                <tr>
                    <?php foreach ($jarak as $value) : ?>
                        <td><?php echo $value; ?></td>
                    <?php endforeach; ?>
                </tr>
            <?php endforeach; ?>
        </table>
    <?php endforeach; ?>


    <?php
    $jsonHasil = file_get_contents('hasil_akhir.json');
    $hasil = json_decode($jsonHasil, true);
    ?>
    <h2>Iterasi Berakhir pada Iterasi ke <?= $hasil['Iterasi_Pesan']; ?></h2>
    <h3>Hasil Cluster Terakhir</h3>
    <table border="1">
        <tr>
            <?php foreach ($hasil['Hasil_Cluster_Terakhir'][0] as $kunci => $nilai) : ?>
                <th><?php echo $kunci; ?></th>
            <?php endforeach; ?>
        </tr>
        <?php foreach ($hasil['Hasil_Cluster_Terakhir'] as $baris) : ?>
            <tr>
                <?php foreach ($baris as $nilai) : ?>
                    <td><?php echo $nilai; ?></td>
                <?php endforeach; ?>
            </tr>
        <?php endforeach; ?>
    </table>
</body>

</html>