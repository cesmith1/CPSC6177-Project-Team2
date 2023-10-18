import unittest
import sys
# Add the directory containing the classschedule module to the Python path
sys.path.append('../functions')
from unittest.mock import patch, Mock
from get_class_schedule import fetch_page_content, extract_schedule, get_area_courses, format_schedule, save_schedule_to_json


class TestWebScrapingFunctions(unittest.TestCase):

    def tearDown(self):
        # Check if the test passed
        if hasattr(self, '_outcome'):  # Python 3.4+
            result = self._outcome.result
            if result.wasSuccessful():
                print(f"{self._testMethodName} passed successfully!")
        else:  # Python 3.3 and below
            if not self._resultForDoCleanups.failures and not self._resultForDoCleanups.errors:
                print(f"{self._testMethodName} passed successfully!")

    @patch('get_class_schedule.requests.get')
    def test_fetch_page_content(self, mock_get):
        test_url = "https://catalog.columbusstate.edu/academic-units/business/computer-science/computer-science-bs-software-systems-track/#programmaptextcontainer"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = "<html><body>Test Content</body></html>".encode()
        mock_get.return_value = mock_response
        
        content = fetch_page_content(test_url)
        self.assertEqual(content, mock_response.content)

    def test_extract_schedule(self):
        URL = "https://catalog.columbusstate.edu/academic-units/business/computer-science/computer-science-bs-software-systems-track/#programmaptextcontainer"
        content = fetch_page_content(URL)
        mock_content = content  # Add a mock HTML content here
        result = extract_schedule(mock_content)
        # Assert based on expected structure and content
        self.assertIn("First Year", result)
        self.assertIn("Fall", result["First Year"])
        self.assertIn("courseCode", result["First Year"]["Fall"][0])




    @patch('get_class_schedule.fetch_page_content')
    def test_get_area_courses(self, mock_fetch_page_content):
        URL = "https://catalog.columbusstate.edu/academic-units/business/computer-science/computer-science-bs-software-systems-track/#programmaptextcontainer"
        content = fetch_page_content(URL)
        # Define your mock content
        mock_content = content # Add a mock HTML content here

        # Mock the fetch_page_content function to return the mock_content
        mock_fetch_page_content.return_value = mock_content

        area_req_url = 'https://catalog.columbusstate.edu/academic-units/business/computer-science/computer-science-bs-software-systems-track/#programofstudytextcontainer'
        container_id = area_req_url[area_req_url.index("#") :]

        result = get_area_courses(area_req_url, container_id)

        
        #print("TEST AREA COURSES RESULTS:")
        #print(result)

        #Assert based on expected structure and content
        self.assertIn("Area A Essential Skills", result)
        self.assertIn("Area B Institutional Options  1", result)
        self.assertIn("Area C Humanities/Fine Arts/Ethics", result)
        self.assertIn("Area D Science/Math/Technology 1", result)
        self.assertIn("Area E Social Sciences ", result)
        self.assertIn("Area F Courses Related to Major", result)
        self.assertIn("Area G Program Requirements ", result)
        self.assertIn("Area H Track Requirements", result)
        self.assertIn("Area I General Electives ", result)

        # You can also check for specific sub-sections or courses within each area
        self.assertIn("Select the following course (the extra credit of MATH applies to Area I):", result["Area A Essential Skills"])
        self.assertIn("B1: Select 3 hours of following courses:", result["Area B Institutional Options  1"])
        self.assertIn("Select one of the following humanities courses:", result["Area C Humanities/Fine Arts/Ethics"])
        self.assertIn("D1: Select two of the following lab science courses:", result["Area D Science/Math/Technology 1"])
        self.assertIn("Select one of the following behavioral science courses:", result["Area E Social Sciences "])
        self.assertIn("Minimum grade of C is required in each course", result["Area F Courses Related to Major"])
        self.assertIn("Minimum grade of C is required  in each CPSC course", result["Area G Program Requirements "])
        self.assertIn("Minimum grade of C is required in each course", result["Area H Track Requirements"])

        # You can also check for specific courses within sub-sections
        self.assertIn({"courseCode": "MATH 1113", "courseName": "Pre-Calculus"}, result["Area A Essential Skills"]["Select the following course (the extra credit of MATH applies to Area I):"])
        self.assertIn({"courseCode": "COMM 1110", "courseName": "Public Speaking"}, result["Area B Institutional Options  1"]["B1: Select 3 hours of following courses:"])
        self.assertIn({"courseCode": "ENGL 2111", "courseName": "World Literature I"}, result["Area C Humanities/Fine Arts/Ethics"]["Select one of the following humanities courses:"])
        # ... and so on for other courses and sections as needed



    def test_format_schedule(self):
        mock_schedule = {
            "First Year": {
                "Fall": [{"courseCode": "TEST101", "courseName": "Test Course", "courseCredit": "3"}],
                "Spring": []
            },
            "Second Year": {
                "Fall": [],
                "Spring": []
            },
            "Third Year": {
                "Fall": [],
                "Spring": []
            },
            "Fourth Year": {
                "Fall": [],
                "Spring": []
            }
        }
        result = format_schedule(mock_schedule)
        # Assert based on expected structure and content
        self.assertIn("First Year", result)
        self.assertIn("Fall", result["First Year"])
        self.assertIn("courses", result["First Year"]["Fall"][0])
        self.assertIn("code", result["First Year"]["Fall"][0]["courses"][0])

    @patch('get_class_schedule.open', new_callable=unittest.mock.mock_open)
    @patch('get_class_schedule.json.dumps')



    def test_save_schedule_to_json(self, mock_dumps, mock_open):
        mock_schedule = {
            "First Year": {"Fall": [{"courseCode": "TEST101", "courseName": "Test Course", "courseCredit": "3"}]}
        }
        mock_filename = "test_file.json"
        save_schedule_to_json(mock_schedule, mock_filename)
        mock_open.assert_called_once_with(mock_filename, 'w')
        mock_dumps.assert_called_once_with(mock_schedule, indent=4)

if __name__ == "__main__":
    unittest.main()
