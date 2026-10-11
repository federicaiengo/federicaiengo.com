"""Citation URL validation regression fixtures. Offline only."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from source_url_validation import valid_source_url


class SourceUrlTests(unittest.TestCase):
    def test_real_public_citation(self):
        for url in ("https://notion.com/help", "http://example.org/a?b=1",
                    "https://docs.python.org:443/3/"):
            self.assertTrue(valid_source_url(url), url)

    def test_unsafe_authority(self):
        for url in ("http://localhost:8000", "https://127.0.0.1/api",
                    "https://10.0.0.3", "http://internal/",
                    "https://user@example.org", "https://:secret@example.org"):
            self.assertFalse(valid_source_url(url), url)

    def test_malformed_url(self):
        for url in ("https://example.org:99999", "ftp://example.org",
                    "https://example.org:/", "https://example.org/hello world",
                    "https://exam\nple.org", " https://example.org"):
            self.assertFalse(valid_source_url(url), url)

    def test_wrong_types(self):
        for url in ("", None, [], 10):
            self.assertFalse(valid_source_url(url))


if __name__ == "__main__":
    unittest.main()
