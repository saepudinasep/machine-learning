<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $text = $_POST['text'];
    $command = "python sentiment_analysis-2.py \"$text\"";
    $sentiment = exec($command);
}
?>

<!DOCTYPE html>
<html>

<head>
    <title>Python Sentiment Analysis</title>
</head>

<body>
    <h1>Python Sentiment Analysis</h1>
    <form method="post" action="">
        <textarea name="text" rows="4" cols="50"></textarea><br><br>
        <input type="submit" value="Analyze">
    </form>

    <?php if (isset($sentiment)) : ?>
        <h2>Result:</h2>
        <p><strong>Sentiment:</strong> <?php echo $sentiment; ?></p>
    <?php endif; ?>
</body>

</html>