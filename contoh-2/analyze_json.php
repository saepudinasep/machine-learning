<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $jsonFilePath = 'data.json'; // Ganti dengan path absolut ke file JSON Anda

    $jsonData = json_decode(file_get_contents($jsonFilePath), true);
    $contents = array_column($jsonData, 'content');

    // Kode untuk menjalankan analisis sentimen
    $pythonScript = "sentiment_analysis.py"; // Ganti dengan path ke skrip Python Anda
    $results = array();

    foreach ($contents as $content) {
        $output = shell_exec("python $pythonScript \"$content\"");
        $sentiment = json_decode($output, true);

        if ($sentiment['compound'] >= 0.05) {
            $sentimentLabel = "Positive";
        } elseif ($sentiment['compound'] <= -0.05) {
            $sentimentLabel = "Negative";
        } else {
            $sentimentLabel = "Neutral";
        }

        $results[] = array(
            'content' => $content,
            'sentiment' => $sentimentLabel
        );
    }
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JSON Sentiment Analysis</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
</head>

<body>

    <div class="container">
        <h1>JSON SENTIMENT ANALYSIS</h1>
        <form action="" method="post">
            <input type="submit" value="Analyze">
        </form>

        <table class="table mt-5">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Text</th>
                    <th scope="col">Sentiment</th>
                </tr>
            </thead>
            <tbody>
                <?php if (isset($results)) : ?>
                    <?php $no = 1; ?>
                    <?php foreach ($results as $result) : ?>
                        <tr>
                            <th scope="row"><?= $no; ?></th>
                            <td><?php echo $result['content']; ?></td>
                            <td><?php echo $result['sentiment']; ?></td>
                        </tr>
                        <?php $no++; ?>
                    <?php endforeach; ?>
                <?php endif; ?>
            </tbody>
        </table>
    </div>



    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js" integrity="sha384-oBqDVmMz9ATKxIep9tiCxS/Z9fNfEXiDAYTujMAeBAsjFuCZSmKbSSUnQlmh/jp3" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.min.js" integrity="sha384-cuYeSxntonz0PPNlHhBs68uyIAVpIIOZZ5JqeqvYYIcEL727kskC66kF92t6Xl2V" crossorigin="anonymous"></script>

</body>

</html>