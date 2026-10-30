import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "File-Organizer"))
sys.path.insert(0, str(ROOT / "Log-Analyzer"))

from file_organizer import category_for, organize_directory
from log_analyzer import analyze_log, write_reports

class FileOrganizerTests(unittest.TestCase):
    def test_categories(self):
        self.assertEqual(category_for(Path("picture.PNG")), "Images")
        self.assertEqual(category_for(Path("notes.pdf")), "Documents")
        self.assertEqual(category_for(Path("mystery.xyz")), "Others")

    def test_dry_run_does_not_move_files(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            sample = folder / "hello.txt"
            sample.write_text("hello", encoding="utf-8")
            moves = organize_directory(folder, dry_run=True)
            self.assertEqual(len(moves), 1)
            self.assertTrue(sample.exists())

class LogAnalyzerTests(unittest.TestCase):
    def test_counts_and_malformed(self):
        with tempfile.TemporaryDirectory() as temp:
            log = Path(temp) / "sample.log"
            log.write_text(
                "2026-10-30 09:00:00 INFO started\n"
                "2026-10-30 09:01:00 ERROR failed\n"
                "not a valid log line\n", encoding="utf-8"
            )
            result = analyze_log(log)
            self.assertEqual(result["total_entries"], 2)
            self.assertEqual(result["counts"]["ERROR"], 1)
            self.assertEqual(len(result["malformed_lines"]), 1)

    def test_reports_created(self):
        with tempfile.TemporaryDirectory() as temp:
            log = Path(temp) / "sample.log"
            log.write_text("2026-10-30 09:00:00 INFO started\n", encoding="utf-8")
            result = analyze_log(log)
            txt, js = write_reports(result, Path(temp) / "reports")
            self.assertTrue(txt.exists())
            self.assertTrue(js.exists())

if __name__ == "__main__":
    unittest.main()
