<?php
require '../vendor/autoload.php';

use PhpOffice\PhpSpreadsheet\IOFactory;

if (isset($_FILES['excel_file']) && $_FILES['excel_file']['error'] === UPLOAD_ERR_OK) {
    $file = $_FILES['excel_file']['tmp_name'];

    // Load the Excel file
    $spreadsheet = IOFactory::load($file);
    $sheet = $spreadsheet->getActiveSheet();

    // Convert Excel data to JSON
    $data = array();
    $highestRow = $sheet->getHighestRow();
    $highestColumn = $sheet->getHighestColumn();
    $headerRow = $sheet->getRowIterator(1, 1)->current(); // Get the first row as header

    $headerValues = array();
    foreach ($headerRow->getCellIterator() as $cell) {
        $headerValues[] = $cell->getValue();
    }

    for ($row = 2; $row <= $highestRow; $row++) {
        $rowData = array();
        $colIndex = 0;
        for ($col = 'A'; $col <= $highestColumn; $col++) {
            $rowData[$headerValues[$colIndex]] = $sheet->getCell($col . $row)->getValue();
            $colIndex++;
        }
        $data[] = $rowData;
    }

    $json_data = json_encode($data, JSON_PRETTY_PRINT);

    // Save JSON data to a file
    $json_filename = 'data.json';
    file_put_contents($json_filename, $json_data);
}
?>

<!DOCTYPE html>
<html>

<head>
    <title>Excel to JSON and HTML Table</title>
</head>

<body>
    <h2>Upload Excel File</h2>
    <form action="" method="POST" enctype="multipart/form-data">
        <input type="file" name="excel_file">
        <button type="submit">Upload</button>
    </form>

    <?php
    // Display data in HTML table
    if (isset($json_filename)) {
        $json_content = file_get_contents($json_filename);
        $json_data = json_decode($json_content, true);

        if ($json_data) {
            echo '<h2>Data from Excel</h2>';
            echo '<table border="1">';
            echo '<tr>';
            foreach ($headerValues as $header) {
                echo '<th>' . $header . '</th>';
            }
            echo '</tr>';
            foreach ($json_data as $row) {
                echo '<tr>';
                foreach ($headerValues as $header) {
                    echo '<td>' . $row[$header] . '</td>';
                }
                echo '</tr>';
            }
            echo '</table>';
        }
    }
    ?>
</body>

</html>