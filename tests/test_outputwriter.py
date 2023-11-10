import unittest
import sys
import os
# Add the directory containing the classschedule module to the Python path
sys.path.insert(0, os.path.abspath('..'))
from functions.outputwriter import OutputWriter, OutputClass  # Import necessary classes from your module
from functions.prereqdag import PrereqViolation
import xlsxwriter

class TestOutputWriter(unittest.TestCase):

    # Helper function to delete the generated file after each test
    def tearDown(self):
        try:
            os.remove('./output.xlsx')
        except OSError:
            pass

    def test_initialization(self):
        writer = OutputWriter('John Doe', 123456789, 2021)
        self.assertEqual(writer.name, 'John Doe')
        self.assertEqual(writer.csuId, 123456789)
        self.assertEqual(writer.startingYear, 2021)
        self.assertIsInstance(writer.workbook, xlsxwriter.Workbook)
        print("test_initialization passed successfully!")

    def test_add_semester(self):
        writer = OutputWriter('John Doe', 123456789, 2021)
        writer.addSemesterToWriter(0, 'Fall', [OutputClass('MATH 101', 'Math 101', ['Fa', 'Sp'], 3, 'Basic Math')])
        writer.addSemesterToWriter(0, 'Spring', [OutputClass('MATH 102', 'Math 102', ['Fa', 'Sp'], 3, 'Intermediate Math')])
        self.assertIn('Fall', writer.years[0])
        self.assertIn('Spring', writer.years[0])
        print("test_add_semester passed successfully!")

    def test_write_and_close(self):
        writer = OutputWriter('John Doe', 123456789, 2021)
        writer.addSemesterToWriter(0, 'Fall', [OutputClass('MATH 102', 'Math 102', ['Fa', 'Sp'], 3, 'Intermediate Math')])
        writer.addSemesterToWriter(0, 'Spring', [OutputClass('MATH 101', 'Math 101', ['Fa', 'Sp'], 3, 'Basic Math')])
        writer.addPrereqViolations([PrereqViolation('MATH 101', ['MATH 102'])])
        writer.write()
        writer.close()
        print("test_write_and_close passed successfully!")

        # Check if the file exists
        self.assertTrue(os.path.exists('./output.xlsx'))

if __name__ == '__main__':
    unittest.main()
