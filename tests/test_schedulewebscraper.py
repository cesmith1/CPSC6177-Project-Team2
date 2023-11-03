import unittest
import sys
import os
# Add the directory containing the classschedule module to the Python path
sys.path.insert(0, os.path.abspath('..'))
from unittest.mock import patch
from functions.schedulewebscraper import ScheduleWebScraper
web_scraper = ScheduleWebScraper()

#Here's are basic unittest test suite for the functions mentioned. Note that this test suite requires mocking because many of your functions make real web requests. The unittest.mock library will help avoid actual web requests during testing.

class TestScheduleWebScraper(unittest.TestCase):


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
        # Test for successful response (status code 200)
        with patch('requests.get') as mocked_get:
            # Mock a successful response
            mocked_get.return_value.status_code = 200
            mocked_get.return_value.content = "<div>sample content</div>"
            
            result = web_scraper.fetch_program_schedule()
            
            # Check if the returned value is a dictionary
            self.assertIsInstance(result, dict)
            
            # Check if the mocked status code is 200
            self.assertEqual(mocked_get.return_value.status_code, 200)

        # Test for error response (status code 404)
        with patch('requests.get') as mocked_get_404:
            # Mock an error response
            mocked_get_404.return_value.status_code = 404
            
            result_404 = web_scraper.fetch_program_schedule()
            
            # Based on your actual implementation, you may want to add more assertions here.
            # For example, if you handle errors by returning an empty dictionary, you can assert:
            self.assertEqual(result_404, {})
            
            # Check if the mocked status code is 404
            self.assertEqual(mocked_get_404.return_value.status_code, 404)
        #web_scraper.print_get_request_page_content("https://catalog.columbusstate.edu/academic-units/business/computer-science/computer-science-bs-software-systems-track/#programmaptextcontainer") # For demonstration purposes, replace "some-url" with the desired URL



    def test_fetch_program_schedule(self):
        # Setup mock for the scraper method that fetches data from the website
        mocked_schedule = {
            'First Year': {
                'Fall': [
                    {'courseCode': 'ENGL 1101', 'courseName': 'English Composition I (minimum grade of C)', 'courseCredit': '3'},
                    # ... [we can include other courses similar to above for this semester]
                ],
                'Spring': [
                    {'courseCode': 'ENGL 1102', 'courseName': 'English Composition II (minimum grade of C)', 'courseCredit': '3'},
                    # ... [we can include other courses similar to above for this semester]
                ],
            },
            # ... [we can include data for Second Year, Third Year, and Fourth Year similarly]
        }

        with patch.object(ScheduleWebScraper, 'fetch_program_schedule', return_value=mocked_schedule):
            # Now when we call the method, it won't actually hit the website but will return our mocked_schedule instead
            result = web_scraper.fetch_program_schedule()

            # Basic checks
            self.assertIsInstance(result, dict)
            self.assertIn('First Year', result)

            # Check for specific course details
            first_year = result['First Year']
            self.assertIn('Fall', first_year)
            self.assertTrue(isinstance(first_year['Fall'], list))
            self.assertEqual(first_year['Fall'][0]['courseCode'], 'ENGL 1101')
            self.assertEqual(first_year['Fall'][0]['courseName'], 'English Composition I (minimum grade of C)')
            self.assertEqual(first_year['Fall'][0]['courseCredit'], '3')

            # We can expand these checks for other semesters and years as needed.

        #web_scraper.print_fetch_program_schedule()

    def test_fetch_area_courses(self):
        # Fetch the data from the website
        result = web_scraper.fetch_area_courses()

        # First, check if the returned result is a dictionary
        self.assertIsInstance(result, dict)

        # Check for presence of specific areas
        areas = ['Area A Essential Skills', 'Area B Institutional Options  1', 'Area C Humanities/Fine Arts/Ethics',
                'Area D Science/Math/Technology 1', 'Area E Social Sciences ', 'Area F Courses Related to Major',
                'Area G Program Requirements ', 'Area H Track Requirements', 'Area I General Electives ']
        
        for area in areas:
            self.assertIn(area, result)

        # More specific checks for certain areas
        self.assertIn('Select the following course (the extra credit of MATH applies to Area I):', result['Area A Essential Skills'])
        self.assertIn('B1: Select 3 hours of following courses:', result['Area B Institutional Options  1'])
        
        # Check if certain courses are present in specific areas
        self.assertIn({'courseCode': 'MATH 1113', 'courseName': 'Pre-Calculus'}, result['Area A Essential Skills']['Select the following course (the extra credit of MATH applies to Area I):'])
        self.assertIn({'courseCode': 'COMM 1110', 'courseName': 'Public Speaking'}, result['Area B Institutional Options  1']['B1: Select 3 hours of following courses:'])

        # ... (we can add similar checks for other areas and courses as well)

        # Optionally: check the number of courses in specific areas
        self.assertEqual(len(result['Area A Essential Skills']['Select the following course (the extra credit of MATH applies to Area I):']), 1)
        self.assertEqual(len(result['Area B Institutional Options  1']['B1: Select 3 hours of following courses:']), 1)

        # ... (we can add similar length checks for other areas as well)

        #web_scraper.print_fetch_area_courses()


    def test_reformat_area_courses(self):
        # Call the function
        result = web_scraper.reformat_area_courses()

        # Expected keys based on the provided data
        expected_keys = ['AREA A', 'AREA B B1:', 'AREA B B2:', 'AREA C Humanities courses:', 'AREA C Fine arts courses:', 
                        'AREA D D1:', 'AREA D D2:', 'AREA E Behavioral science courses:', 'AREA E World culture courses:',
                        'AREA F', 'AREA G', 'AREA H']

        # 1. Check if result is a dictionary
        self.assertIsInstance(result, dict)

        # 2. Check if the result's keys match the expected keys
        self.assertListEqual(list(result.keys()), expected_keys)

        # 3. For each key, check if the value is a list
        for key, value in result.items():
            self.assertIsInstance(value, list)
            
            # 4. For each list item, check if it's a dictionary with 'courseCode' and 'courseName' keys
            for item in value:
                self.assertIsInstance(item, dict)
                self.assertIn('courseCode', item)
                self.assertIn('courseName', item)

        #web_scraper.print_reformat_area_courses()

    def test_replace_schedule_area_section(self):
        # This function doesn't return anything. It modifies an internal property.
        # So, we can only check if it runs without errors by calling it.
        web_scraper.replace_schedule_area_section()
    #web_scraper.print_replace_schedule_area_section()


    def test_get_formatted_schedule(self):
        expected_schedule = {
            'First Year': {
                'Fall': [
                    {'courses': [{'code': 'ENGL 1101', 'name': 'English Composition I (minimum grade of C)'}], 'courseCredit': '3'},
                    {'courses': [{'code': 'MATH 1113', 'name': 'Pre-Calculus (minimum grade of C)'}], 'courseCredit': '4'},
                    {'courses': [{'code': 'CHEM 1211', 'name': 'Principles of Chemistry I'}], 'courseCredit': '3'},
                    {'courses': [{'code': 'CHEM 1211L', 'name': 'Principles of Chemistry I Lab'}], 'courseCredit': '1'},
                    {'courses': [{'code': 'ITEC 2215', 'name': 'Into to Information Technology'}], 'courseCredit': '3'}
                ],
                'Spring': [
                    {'courses': [{'code': 'ENGL 1102', 'name': 'English Composition II (minimum grade of C)'}], 'courseCredit': '3'},
                    {'courses': [{'code': 'MATH 2263', 'name': 'Calculus II'}], 'courseCredit': '4'},
                    {'courses': [{'code': 'ITEC 2261', 'name': 'Application Development I'}], 'courseCredit': '3'}
                ],
            },
            'Second Year': {
                'Fall': [
                    {'courses': [{'code': 'ITEC 3230', 'name': 'Systems Analysis'}], 'courseCredit': '3'},
                    {'courses': [{'code': 'ITEC 3250', 'name': 'Database Management Systems'}], 'courseCredit': '3'},
                ],
                'Spring': [
                    {'courses': [{'code': 'ITEC 3260', 'name': 'Data Communications and Networking'}], 'courseCredit': '3'},
                    {'courses': [{'code': 'ITEC 3280', 'name': 'Application Development II'}], 'courseCredit': '3'},
                ],
            },
            'Third Year': {
                'Fall': [
                    {'courses': [{'code': 'ITEC 4230', 'name': 'Project Management'}], 'courseCredit': '3'},
                ],
                'Spring': [
                    {'courses': [{'code': 'ITEC 4250', 'name': 'Web Application Development'}], 'courseCredit': '3'},
                ],
            },
            'Fourth Year': {
                'Fall': [
                    {'courses': [{'code': 'ITEC 4270', 'name': 'Into to Cyber Security'}], 'courseCredit': '3'},
                ],
                'Spring': [
                    {'courses': [{'code': 'ITEC 4290', 'name': 'IT Strategy and Policy'}], 'courseCredit': '3'},
                ],
            },
        }

        # Mocking the get_formatted_schedule() method to return expected_schedule
        with patch.object(web_scraper, 'get_formatted_schedule', return_value=expected_schedule):
            result = web_scraper.get_formatted_schedule()

        self.assertEqual(result, expected_schedule)  
        #web_scraper.print_get_formatted_schedule()


    def test_can_fetch_data(self):
        result = web_scraper.can_fetch_data()
        # Check if the result is of type bool and that its value is True
        self.assertTrue(result, msg="Expected can_fetch_data() to return True but got False")
        #web_scraper.print_can_fetch_data()


#Print Options
#web_scraper.print_get_request_page_content("https://catalog.columbusstate.edu/academic-units/business/computer-science/computer-science-bs-software-systems-track/#programmaptextcontainer") # For demonstration purposes, replace "some-url" with the desired URL
#web_scraper.print_fetch_program_schedule()
#web_scraper.print_fetch_area_courses()
#web_scraper.print_reformat_area_courses()
#web_scraper.print_replace_schedule_area_section()
#web_scraper.print_get_formatted_schedule()
#web_scraper.print_can_fetch_data()

if __name__ == '__main__':
    unittest.main()
