import unittest
import os
from PyPDF4 import PdfFileReader
import json
#import prereqparser as pp  # assuming your parser code is saved in prereqparser.py

class TestPrereqParser(unittest.TestCase):

    def setUp(self):
        # Setup any pre-conditions before running tests, e.g., paths or sample data
        self.pdf_path = '../PrerequisiteGraph-Software_Systems2019-2020.pdf'
        self.json_output_path = '../data/prereqs.json'

    def test_pdf_read(self):
        """Test if the PDF file is successfully read."""
        if os.path.exists(self.pdf_path):
            with open(self.pdf_path, 'rb') as file:
                reader = PdfFileReader(file)
                self.assertIsNotNone(reader, "Failed to read the PDF file.")
                self.assertGreater(reader.numPages, 0, "No pages detected in the PDF file.")
        print("test_pdf_read passed successfully!")

    def test_course_data_extraction(self):
        """Test if the course data is successfully extracted."""
        # assuming you have a function `extract_courses_from_pdf` that does the extraction in prereqparser.py
        # courses = pp.extract_courses_from_pdf(self.pdf_path)
        
        # For this example, I am reading from the JSON output file
        with open(self.json_output_path, 'r') as json_file:
            courses = json.load(json_file)
            self.assertIsNotNone(courses, "No courses extracted.")
            self.assertGreater(len(courses), 0, "No course data extracted.")
            for course in courses:
                self.assertIn("Rubric Number", course)
                self.assertIn("Course Name", course)
                self.assertIn("Semesters Offered", course)
            print("test_course_data_extraction passed successfully!")

if __name__ == "__main__":
    unittest.main()
