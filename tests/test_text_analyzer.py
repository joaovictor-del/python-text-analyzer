import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from text_analyzer import analyze_text, format_report, read_input


class TextAnalyzerTests(unittest.TestCase):
    def test_analyze_counts_words_and_unicode(self):
        report = analyze_text("Olá, mundo! Olá.")
        self.assertEqual(report.words, 3)
        self.assertEqual(report.sentences, 2)
        self.assertEqual(report.top_words, (("olá", 2), ("mundo", 1)))

    def test_word_ranking_is_stable_when_counts_tie(self):
        report = analyze_text("banana maçã uva", top=2)
        self.assertEqual(report.top_words, (("banana", 1), ("maçã", 1)))

    def test_character_counts_distinguish_whitespace(self):
        report = analyze_text("a b\n")
        self.assertEqual(report.characters, 4)
        self.assertEqual(report.characters_without_spaces, 2)

    def test_reading_time_rounds_up_to_a_minute(self):
        report = analyze_text("palavra " * 201)
        self.assertEqual(report.reading_minutes, 2)
        self.assertEqual(analyze_text("").reading_minutes, 0)

    def test_empty_text_report_is_readable(self):
        self.assertIn("(nenhuma palavra encontrada)", format_report(analyze_text("")))

    def test_top_must_be_positive(self):
        with self.assertRaisesRegex(ValueError, "pelo menos 1"):
            analyze_text("texto", top=0)

    def test_read_input_from_file_and_stdin(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "text.txt"
            path.write_text("Olá", encoding="utf-8")
            self.assertEqual(read_input(path), "Olá")

        with patch("text_analyzer.sys.stdin") as stdin:
            stdin.read.return_value = "Entrada"
            self.assertEqual(read_input(None), "Entrada")


if __name__ == "__main__":
    unittest.main()
