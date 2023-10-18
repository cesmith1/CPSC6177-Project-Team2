import unittest
import sys
# Add the directory containing the classschedule module to the Python path
sys.path.append('../functions')
from unittest.mock import patch
from schedule_web_scraper import ScheduleWebScraper

#Here's are basic unittest test suite for the functions mentioned. Note that this test suite requires mocking because many of your functions make real web requests. The unittest.mock library will help avoid actual web requests during testing.

class TestPrereqDAG(unittest.TestCase):

    def setUp(self):
        # Sample JSON array for testing
        self.jsonArray = [
            {
                "Rubric Number": "CPSC 2100",
                "Course Name": "Intro to Programming",
                "Semesters Offered": ["Fall", "Spring"],
                "Children": ["CPSC 2108"],
                "Other Reqs": []
            },
            {
                "Rubric Number": "CPSC 2108",
                "Course Name": "Data Structures",
                "Semesters Offered": ["Fall", "Spring"],
                "Children": [],
                "Other Reqs": ["CPSC 2100"]
            }
        ]

    def tearDown(self):
        # Check if the tests passed
        if hasattr(self, '_outcome'):  # Python 3.4+
            result = self._outcome.result
            if result.wasSuccessful():
                print(f"{self._testMethodName} passed successfully!")
        else:  # Python 3.3 and below
            if not self._resultForDoCleanups.failures and not self._resultForDoCleanups.errors:
                print(f"{self._testMethodName} passed successfully!")



    def test_get_request_page_content(self):
        scraper = ScheduleWebScraper()

        # Test for successful response (status code 200)
        with patch('requests.get') as mocked_get:
            # Mock a successful response
            mocked_get.return_value.status_code = 200
            mocked_get.return_value.content = "<div>sample content</div>"
            
            result = scraper.fetch_program_schedule()
            
            # Check if the returned value is a dictionary
            self.assertIsInstance(result, dict)
            
            # Check if the mocked status code is 200
            self.assertEqual(mocked_get.return_value.status_code, 200)

        # Test for error response (status code 404)
        with patch('requests.get') as mocked_get_404:
            # Mock an error response
            mocked_get_404.return_value.status_code = 404
            
            result_404 = scraper.fetch_program_schedule()
            
            # Based on your actual implementation, you may want to add more assertions here.
            # For example, if you handle errors by returning an empty dictionary, you can assert:
            self.assertEqual(result_404, {})
            
            # Check if the mocked status code is 404
            self.assertEqual(mocked_get_404.return_value.status_code, 404)
    



    def test_fetch_program_schedule(self):
        scraper = ScheduleWebScraper()
        # Given the structure of the code, this function requires a live website.
        # For unit testing, we should mock the behavior of the required website.
        # However, for simplicity, this test only checks if the return is a dictionary.
        result = scraper.fetch_program_schedule()
        self.assertIsInstance(result, dict)

    def test_fetch_area_courses(self):
        scraper = ScheduleWebScraper()
        # Similar to `test_fetch_program_schedule`, this function requires a live website.
        # This test only checks if the return is a dictionary.
        result = scraper.fetch_area_courses()
        self.assertIsInstance(result, dict)

    def test_reformat_area_courses(self):
        scraper = ScheduleWebScraper()
        result = scraper.reformat_area_courses()
        self.assertIsInstance(result, dict)

    def test_replace_schedule_area_section(self):
        scraper = ScheduleWebScraper()
        # This function doesn't return anything. It modifies an internal property.
        # So, we can only check if it runs without errors by calling it.
        scraper.replace_schedule_area_section()

    def test_get_formatted_schedule(self):
        scraper = ScheduleWebScraper()
        result = scraper.get_formatted_schedule()
        self.assertIsInstance(result, dict)

    def test_can_fetch_data(self):
        scraper = ScheduleWebScraper()
        result = scraper.can_fetch_data()
        self.assertIsInstance(result, bool)

if __name__ == '__main__':
    unittest.main()
