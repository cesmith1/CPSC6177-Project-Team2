import unittest
import sys
# Add the directory containing the classschedule module to the Python path
sys.path.append('../functions')
from classschedule import Course, Requirement, Year, ClassSchedule


class TestSchedulingSystem(unittest.TestCase):

    def setUp(self):
        # Sample data to be used for testing
        self.sample_data = {
            "Year1": {
                "Fall": [
                    {
                        "courses": [{"code": "CPSC 1010", "name": "Introduction to Programming"}],
                        "courseCredit": 3
                    },
                    {
                        "courses": [{"code": "MATH 1010", "name": "Calculus I"}],
                        "courseCredit": 3
                    }
                ],
                "Spring": [
                    {
                        "courses": [{"code": "CPSC 1020", "name": "Advanced Programming"}],
                        "courseCredit": 3
                    }
                ]
            }
        }
        # Create a ClassSchedule instance to be used in the tests
        self.schedule = ClassSchedule(self.sample_data)

    def tearDown(self):
        # Check if the test passed
        if hasattr(self, '_outcome'):  # Python 3.4+
            result = self._outcome.result
            if result.wasSuccessful():
                print(f"{self._testMethodName} passed successfully!")
        else:  # Python 3.3 and below
            if not self._resultForDoCleanups.failures and not self._resultForDoCleanups.errors:
                print(f"{self._testMethodName} passed successfully!")

    def test_course_creation(self):
        # Test data for creating a Course instance
        course_data = {"code": "CPSC 1010", "name": "Introduction to Programming"}
        course = Course(course_data)
        # Check if the course code is set correctly
        self.assertEqual(course.code, "CPSC 1010")
        # Check if the course name is set correctly
        self.assertEqual(course.name, "Introduction to Programming")

    def test_requirement_creation(self):
        # Test data for creating a Requirement instance
        req_data = {
            "courses": [{"code": "CPSC 1010", "name": "Introduction to Programming"}],
            "courseCredit": 3
        }
        req = Requirement(req_data)
        # Check if the courses list is set correctly
        self.assertEqual(len(req.courses), 1)
        # Check if the course credit is set correctly
        self.assertEqual(req.courseCredit, 3)

    def test_year_creation(self):
        # Create a Year instance using the sample data
        year = Year(self.sample_data["Year1"])
        # Check if "Fall" is a valid semester in the created year
        self.assertIn("Fall", year.semesters)
        # Check if "Spring" is a valid semester in the created year
        self.assertIn("Spring", year.semesters)

    def test_schedule_requirements(self):
        # Retrieve the requirements for the fall semester of the first year
        requirements_fall = self.schedule.getRequirements(0, "fall")
        # Check if there are two requirements in the fall semester
        self.assertEqual(len(requirements_fall), 2)

        # Retrieve the requirements for the spring semester of the first year
        requirements_spring = self.schedule.getRequirements(0, "spring")
        # Check if there is one requirement in the spring semester
        self.assertEqual(len(requirements_spring), 1)

    def test_course_availability(self):
        # Retrieve the availability of the course "CPSC 1010"
        availability = self.schedule.getAvailability("CPSC 1010")
        
        # Initialize a flag to False
        found = False
        
        # Check if "CPSC 1010" is available in the first year and fall semester
        for course_info in availability:
            if course_info.year == 0 and course_info.semester == "Fall":
                found = True
        
        # Assert that the course was found
        self.assertTrue(found, "'CPSC 1010' was not found in Year 0, Fall semester.")


if __name__ == "__main__":
    # Run the tests
    unittest.main()

""" Each function in the TestSchedulingSystem class is a 
test case that checks a specific functionality or behavior 
of the classes from your classschedule module. The setUp method is a 
special method that is run before each test case to set up any objects or 
data that will be used in the test. The unittest.main() function is used to 
run the tests when the script is run. """