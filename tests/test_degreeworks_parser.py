import unittest
import re
from pdfminer.high_level import extract_text

class TestDegreeWorksParser(unittest.TestCase):

    def setUp(self):
        self.text = extract_text('../SampleInput1.pdf')
        self.pattern = re.compile(r"[A-Z]{4} \d{4}[A-Z]?\s*([A-Za-z\s\-]+)")

    def tearDown(self):
        # Check if the tests passed
        if hasattr(self, '_outcome'):  # Python 3.4+
            result = self._outcome.result
            if result.wasSuccessful():
                print(f"{self._testMethodName} passed successfully!")
        else:  # Python 3.3 and below
            if not self._resultForDoCleanups.failures and not self._resultForDoCleanups.errors:
                print(f"{self._testMethodName} passed successfully!")

    def test_pdf_extraction(self):
        # Test if the extraction returns a string
        self.assertIsInstance(self.text, str)
        # Test if the extracted text is not empty
        self.assertTrue(len(self.text) > 0)

    def test_regex_pattern(self):
        #print(self.text)
        matches = self.pattern.findall(self.text)
        # Test if matches is a list
        self.assertIsInstance(matches, list)
        # Test if there are matches
        self.assertTrue(len(matches) > 0)


    #TESTING EACH COURSE EXTRACTION FROM degreeworks.pdf file
    def test_american_government_extraction(self):
        self.assertIn('American Government', self.text)
        pattern = re.compile(r'1 Class in POLS 1101')
        self.assertIsNotNone(pattern.search(self.text))

    def test_professionalism_in_computing_extraction(self):
        # Check if 'Professionalism in Computing' is present in the extracted text
        self.assertIn('Professionalism in Computing', self.text)
        # Use regex to check for the pattern '1 Class in CPSC 3165*'
        pattern = re.compile(r'1 Class in CPSC 3165\*')
        self.assertIsNotNone(pattern.search(self.text))
        

    def test_baccalaureate_survey_extraction(self):
        # Check if 'Baccalaureate Survey' is present in the extracted text
        self.assertIn('Baccalaureate Survey', self.text)
        # Use regex to check for the pattern '1 Class in CPSC'
        pattern = re.compile(r'1 Class in CPSC')
        self.assertIsNotNone(pattern.search(self.text))

    def test_assembly_language_programming_extraction(self):
        self.assertIn('Assembly Language Programing 1', self.text)
        pattern = re.compile(r'1 Class in CPSC 3121\*')
        self.assertIsNotNone(pattern.search(self.text))

    def test_algorithms_extraction(self):
        self.assertIn('CPSC 4115 Algorithms', self.text)
        pattern = re.compile(r'1 Class in CPSC 5115U\*')
        self.assertIsNotNone(pattern.search(self.text))

    def test_programming_languages_extraction(self):
        self.assertIn('Programming Languages', self.text)
        pattern = re.compile(r'1 Class in CPSC 4135\* or 5135U\*')
        self.assertIsNotNone(pattern.search(self.text))

    def test_theory_of_computation_extraction(self):
        self.assertIn('Theory of Computation', self.text)
        pattern = re.compile(r'1 Class in CPSC 4148\* or 5128U\*')
        self.assertIsNotNone(pattern.search(self.text))

    def test_computer_architecture_extraction(self):
        self.assertIn('Computer Architecture', self.text)
        pattern = re.compile(r'1 Class in CPSC 4155\* or 5155U\*')
        self.assertIsNotNone(pattern.search(self.text))

    def test_computer_networks_extraction(self):
        self.assertIn('Computer Networks', self.text)
        pattern = re.compile(r'1 Class in CPSC 4157\* or 5157U\*')
        self.assertIsNotNone(pattern.search(self.text))

    def test_software_engineering_extraction(self):
        self.assertIn('Software Engineering', self.text)
        pattern = re.compile(r'1 Class in CPSC 4175\*')
        self.assertIsNotNone(pattern.search(self.text))

    def test_senior_software_engineering_project_extraction(self):
        self.assertIn('Senior Software Engineering Project', self.text)
        pattern = re.compile(r'1 Class in CPSC 4176\*')
        self.assertIsNotNone(pattern.search(self.text))

if __name__ == "__main__":
    unittest.main()
