<?php
$pythonScript = "sentiment_analysis.py"; // Ganti dengan path ke skrip Python Anda

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $text = $_POST['text'];

    $output = shell_exec("python $pythonScript \"$text\"");
    $sentiment = json_decode($output, true);

    if ($sentiment['compound'] >= 0.05) {
        $sentimentLabel = "Positive";
    } elseif ($sentiment['compound'] <= -0.05) {
        $sentimentLabel = "Negative";
    } else {
        $sentimentLabel = "Neutral";
    }
}
?>

<!DOCTYPE html>
<html>

<head>
    <title>Sentiment Analysis</title>
</head>

<body>
    <h1>Sentiment Analysis</h1>
    <form method="post" action="">
        <textarea name="text" rows="4" cols="50"></textarea><br><br>
        <input type="submit" value="Analyze">
    </form>

    <?php if (isset($sentiment)) : ?>
        <h2>Result:</h2>
        <p><strong>Sentiment:</strong> <?php echo $sentimentLabel; ?></p>
        <p><strong>Positive:</strong> <?php echo $sentiment['pos']; ?></p>
        <p><strong>Negative:</strong> <?php echo $sentiment['neg']; ?></p>
        <p><strong>Neutral:</strong> <?php echo $sentiment['neu']; ?></p>
        <p><strong>Compound:</strong> <?php echo $sentiment['compound']; ?></p>
    <?php endif; ?>
</body>

</html>