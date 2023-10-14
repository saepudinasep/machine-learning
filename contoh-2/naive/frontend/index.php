<!DOCTYPE html>
<html>

<head>
    <link rel="stylesheet" type="text/css" href="style.css">
</head>

<body>
    <?php
    // Load and process data
    $pythonScript = 'data_processing.py';  // Path to your Python script
    $command = 'python ' . escapeshellarg($pythonScript);
    $output = array();
    $returnCode = 0;

    // Execute the Python script
    exec($command, $output, $returnCode);

    // Check if the execution was successful
    if ($returnCode === 0) {
        $serialized_data = implode("", $output);  // Combine the output lines into a single string
        $data = json_decode($serialized_data, true);

        if (count($data) === 4) {
            list($train_reviews, $test_reviews, $train_labels, $test_labels) = $data;

            // Now you have the processed data, you can use it in your PHP script

        } else {
            echo "Error: Unexpected data format from Python script.";
        }
    } else {
        echo "Error executing Python script: $returnCode";
        echo "<pre>";
        print_r($output); // Display the Python script's error output
        echo "</pre>";
    }

    // Train the model
    $train_script = 'model_training.py';
    $train_cmd = escapeshellcmd('python ' . $train_script);
    exec($train_cmd);

    // Evaluate the model
    $eval_script = 'model_evaluation.py';
    $eval_cmd = escapeshellcmd('python ' . $eval_script);
    $accuracy = exec($eval_cmd);

    echo "<p>Accuracy: $accuracy</p>";

    // Predict labels
    $predicted_labels = array();
    for ($i = 0; $i < count($test_reviews); $i++) {
        $predicted_label = exec('python -c "import joblib; model = joblib.load(\'model.pkl\'); print(model.predict([\'' . addslashes($test_reviews[$i]) . '\'])[0])"');
        $predicted_labels[] = $predicted_label;
    }

    // unlink($train_temp_file); // Hapus berkas sementara setelah digunakan

    // Display the table
    echo "<table>";
    echo "<tr><th>Review</th><th>Actual Label</th><th>Predicted Label</th></tr>";

    for ($i = 0; $i < count($test_reviews); $i++) {
        echo "<tr>";
        echo "<td>" . $test_reviews[$i] . "</td>";
        echo "<td>" . $test_labels[$i] . "</td>";
        echo "<td>" . $predicted_labels[$i] . "</td>";
        echo "</tr>";
    }

    echo "</table>";



    ?>
</body>

</html>