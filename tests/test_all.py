import unittest
import sys
import subprocess
# Add the directory containing the classschedule module to the Python path
sys.path.append('../functions')


class TestAllTests(unittest.TestCase):

    def allTests():
        print("")
        print("")
        print("Testing classschedule.py: ")
        subprocess.call("test_classschedule.py", shell=True)
        print("")

        print("Testing degreeworks_parser.py: ")
        subprocess.call("test_degreeworks_parser.py", shell=True)
        print("")

        print("Testing prereq-parser.py: ")
        subprocess.call("test_prereq_parser.py", shell=True)
        print("")

        print("Testing prereqdag.py: ")
        subprocess.call("test_prereqdag.py", shell=True)
        print("")

        print("Testing schedule_web_scraper.py: ")
        subprocess.call("test_schedule_web_scraper.py", shell=True)
        print("")

        print("Testing outputwriter.py: ")
        subprocess.call("test_outputwriter.py", shell=True)
        print("")

if __name__ == "__main__":
    # Run the tests
    TestAllTests.allTests()
