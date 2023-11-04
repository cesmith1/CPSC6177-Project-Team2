import unittest
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from PyPDF4 import PdfFileReader
from functions.prereqparser import parsePrereqs
import json
#import prereqparser as pp  # assuming your parser code is saved in prereqparser.py

class TestPrereqParser(unittest.TestCase):

    def setUp(self):
        # Setup any pre-conditions before running tests, e.g., paths or sample data
        self.pdf_path = './data/PrerequisiteGraph-Software_Systems2019-2020.pdf'
        self.json_output_path = './tests/prereqs_temp.json'

    def tearDown(self):
                # Check if the tests passed
        if hasattr(self, '_outcome'):  # Python 3.4+
            result = self._outcome.result
            if result.wasSuccessful():
                print(f"{self._testMethodName} passed successfully!")
        else:  # Python 3.3 and below
            if not self._resultForDoCleanups.failures and not self._resultForDoCleanups.errors:
                print(f"{self._testMethodName} passed successfully!")
        try:
            os.remove(self.json_output_path)
        except OSError:
            pass

    def test_pdf_read(self):
        """Test if the PDF file is successfully read."""
        if os.path.exists(self.pdf_path):
            with open(self.pdf_path, 'rb') as file:
                reader = PdfFileReader(file)
                self.assertIsNotNone(reader, "Failed to read the PDF file.")
                self.assertGreater(reader.numPages, 0, "No pages detected in the PDF file.")
            print("test_pdf_read passed successfully!")

    def test_parsePrereqs(self):
        parsePrereqs(self.pdf_path, self.json_output_path)
        self.assertTrue(os.path.exists(self.json_output_path))
        os.remove(self.json_output_path)

if __name__ == "__main__":
    unittest.main()
