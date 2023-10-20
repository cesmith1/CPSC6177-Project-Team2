import unittest
import sys
import subprocess
import os
# Add the directory containing the classschedule module to the Python path
sys.path.append('../tests')


class TestAllTests(unittest.TestCase):

    def allTests():
        os.chdir("tests")

        print("")
        print("")
        print("Testing classschedule.py: ")
        subprocess.call("python3 test_classschedule.py", shell=True)
        print("")

        print("Testing degreeworksparser.py: ")
        subprocess.call("python3 test_degreeworks_parser.py", shell=True)
        print("")

        print("Testing prereqparser.py: ")
        subprocess.call("python3 test_prereq_parser.py", shell=True)
        print("")

        print("Testing prereqdag.py: ")
        subprocess.call("python3 test_prereqdag.py", shell=True)
        print("")

        print("Testing schedulewebscraper.py: ")
        subprocess.call("python3 test_schedule_web_scraper.py", shell=True)
        print("")

        print("Testing outputwriter.py: ")
        subprocess.call("python3 test_outputwriter.py", shell=True)
        print("")

if __name__ == "__main__":
    # Run the tests
    TestAllTests.allTests()
