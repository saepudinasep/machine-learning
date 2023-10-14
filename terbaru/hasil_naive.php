<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Hasil Klasifikasi Naive Bayes</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9" crossorigin="anonymous">
</head>

<body>
    <div class="container mt-5">
        <h1>Hasil Klasifikasi Naive Bayes</h1>
    </div>

    <?php
    $naive_bayes_results = json_decode(file_get_contents('naive_bayes_results.json'), true);
    $naive_bayes_evaluation = json_decode(file_get_contents('naive_bayes_evaluation.json'), true);
    ?>

    <div class="container mt-5">

        <table class="table">
            <thead>
                <tr>
                    <th scope="col">No</th>
                    <th scope="col">Text</th>
                    <th scope="col">Sentiment</th>
                    <th scope="col">Predict</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($naive_bayes_results['text'] as $index => $text) : ?>
                    <tr>
                        <th scope="row"><?= $index + 1; ?></th>
                        <td><?= $text; ?></td>
                        <td><?= $naive_bayes_results['sentiment_true'][$index]; ?></td>
                        <td><?= $naive_bayes_results['sentiment_predicted'][$index]; ?></td>
                    </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js" integrity="sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.min.js" integrity="sha384-Rx+T1VzGupg4BHQYs2gCW9It+akI2MM/mndMCy36UVfodzcJcF0GGLxZIzObiEfa" crossorigin="anonymous"></script>
</body>

</html>