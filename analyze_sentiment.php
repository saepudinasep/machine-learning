<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Ambil teks dari formulir
    $text = $_POST["text"];

    // Lakukan pra-pemrosesan teks (misalnya, menghilangkan tanda baca dan stemming)

    // Lakukan analisis sentimen menggunakan algoritma atau model yang sesuai

    // Fungsi untuk melakukan stemming menggunakan algoritma Porter Stemmer
    function stem($word)
    {
        require_once('porter-stemmer.php'); // Memuat implementasi Porter Stemmer
        $stemmer = new \PorterStemmer();
        return $stemmer->stem($word);
    }
    // Pra-pemrosesan teks
    $text = $_POST["text"];

    // Menghilangkan tanda baca dan karakter non-alfabet
    $text = preg_replace('/[^A-Za-z0-9\s]/', '', $text);

    // Konversi teks menjadi huruf kecil
    $text = strtolower($text);

    // Tokenisasi teks menjadi kata-kata
    $words = explode(' ', $text);

    // Lakukan stemming pada kata-kata (misalnya, menggunakan algoritma Porter Stemmer)
    $stemmed_words = array();
    foreach ($words as $word) {
        // Lakukan stemming pada kata dan tambahkan ke array baru
        $stemmed_word = stem($word); // Ganti dengan fungsi stemming yang sesuai
        $stemmed_words[] = $stemmed_word;
    }

    // Gabungkan kata-kata yang telah di-stemming kembali menjadi teks
    $preprocessed_text = implode(' ', $stemmed_words);



    // Tampilkan hasil analisis sentimen
    echo "<h2>Hasil Analisis Sentimen:</h2>";
    echo "<p>Teks: $text</p>";
    echo "<p>Sentimen: $sentiment</p>";
}
