import unittest
import sys
import os
# Add the directory containing the classschedule module to the Python path
sys.path.append('../functions')
import tests


class TestAllTests(unittest.TestCase):

    def allTests():
        print("")
        print("")
        print("Testing classschedule.py: ")
        os.system(f"python3 test_classschedule.py")
        print("")

        print("Testing degreeworks_parser.py: ")
        os.system(f"python3 test_degreeworksparser.py")
        print("")

        print("Testing prereq_parser.py: ")
        os.system(f"python3 test_prereqparser.py")
        print("")

        print("Testing prereqdag.py: ")
        os.system(f"python3 test_prereqdag.py")
        print("")

        print("Testing schedule_web_scraper.py: ")
        os.system(f"python3 test_schedulewebscraper.py")
        print("")

if __name__ == "__main__":
    # Run the tests
    TestAllTests.allTests()
