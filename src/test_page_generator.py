import unittest
from page_generator import extract_title

class TestPageGenerator(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello World \n\nThis is a paragraph."
        self.assertEqual(extract_title(md), "Hello World")

    def test_extract_title_no_h1(self):
        md = "## Subheading\n\nNo main heading here!"
        with self.assertRaises(ValueError):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()