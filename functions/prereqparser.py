# importing required modules
import re
import json
from PyPDF4 import PdfFileReader

# creating a pdf reader object
def parsePrereqs(inputFilepath, outputFilepath):
    with open(inputFilepath, 'rb') as file:
        reader = PdfFileReader(file)

        # printing number of pages in pdf file
        #print("Number of pages detected:", reader.numPages)

        # getting a specific page from the pdf file
        page = reader.getPage(0)

        # extracting text from page
        text = page.extractText()

    #print("RAW OUTPUT:")
    #print(text)

    # Sample data from the PDF
    data = text

    # Adjusted regular expression to match course details
    pattern = r"([A-Z]{4} \d{4}[A-Z]?)([A-Za-z\s\-]+)((?:Fa|Sp|Su|--|\?\?)+)"

    matches = re.findall(pattern, data)

    courses = []

    for match in matches:
        course_code = match[0]
        course_name = match[1].replace('\n', ' ').strip()  # Replace \n with space
        semesters_offered = re.findall(r"Fa|Sp|Su|--|\?\?", match[1] + match[2])  # Search in both course_name and the matched semester string

        # Remove the semesters, '--', and '??' from the course name
        for semester in semesters_offered:
            course_name = course_name.replace(semester, "").strip()

        course = {
            "Rubric Number": course_code,
            "Course Name": course_name,
            "Semesters Offered": semesters_offered
        }
        courses.append(course)

    # Save the parsed data to a JSON file
    with open(outputFilepath, 'w') as json_file:
        json.dump(courses, json_file, indent=4)

    #print()
    #print("Prerequisites parsed & saved to prereqs.json file in the data folder")
