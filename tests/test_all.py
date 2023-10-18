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
        os.system(f"python3 test_degreeworks_parser.py")
        print("")

        print("Testing prereq-parser.py: ")
        os.system(f"python3 test_prereq_parser.py")
        print("")

        print("Testing prereqdag.py: ")
        os.system(f"python3 test_prereqdag.py")
        print("")

        print("Testing schedule_web_scraper.py: ")
        os.system(f"python3 test_schedule_web_scraper.py")
        print("")

if __name__ == "__main__":
    # Run the tests
    TestAllTests.allTests()
