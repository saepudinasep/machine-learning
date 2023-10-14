<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $text = $_POST['text'];
    $command = "python sentiment_analysis.py \"$text\"";
    $sentiment = shell_exec($command);
}
?>

<!DOCTYPE html>
<html>

<head>
    <title>Sentiment Analysis Result</title>
</head>

<body>
    <h1>Sentiment Analysis Result</h1>
    <p><strong>Input Text:</strong> <?php echo $text; ?></p>
    <?php if (isset($sentiment)) : ?>
        <p><strong>Sentiment:</strong> <?php echo $sentiment; ?></p>
    <?php endif; ?>
    <p><a href="naive_bayes_sentiment.php">Back to Analysis</a></p>
</body>

</html>