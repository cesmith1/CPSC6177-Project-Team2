import unittest
import sys
import os
# Add the directory containing the classschedule module to the Python path
sys.path.insert(0, os.path.abspath('..'))
from functions.prereqdag import PrereqDAG, DAGClass

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

    def test_init(self):
        dag = PrereqDAG(self.jsonArray)
        self.assertIsInstance(dag.dagDict["CPSC 2100"], DAGClass)
        self.assertEqual(dag.dagDict["CPSC 2100"].name, "Intro to Programming")

    def test_topoSort(self):
        dag = PrereqDAG(self.jsonArray)
        sorted_result = dag.topoSort(["CPSC 2108", "CPSC 2100"])
        self.assertEqual(sorted_result, ["CPSC 2100", "CPSC 2108"])

    def test_getPrereqs(self):
        dag = PrereqDAG(self.jsonArray)
        prereqs = dag.getPrereqs("CPSC 2108")
        self.assertEqual(prereqs, ["CPSC 2100"])

    def test_str(self):
        dag = PrereqDAG(self.jsonArray)
        result_str = str(dag)
        expected_str = ("CPSC 2100:\n\tname=Intro to Programming\n\tsemestersOffered=['Fall', 'Spring']\n\tchildren=['CPSC 2108']\n\totherReqs=[])\n"
                        "CPSC 2108:\n\tname=Data Structures\n\tsemestersOffered=['Fall', 'Spring']\n\tchildren=[]\n\totherReqs=['CPSC 2100'])\n")
        self.assertEqual(result_str, expected_str)

if __name__ == '__main__':
    unittest.main()
