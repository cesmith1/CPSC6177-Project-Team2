# importing required modules
import os
import re
import json
from PyPDF4 import PdfFileReader

# creating a pdf reader object
os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open('../PrerequisiteGraph-Software_Systems2019-2020.pdf', 'rb') as file:
    reader = PdfFileReader(file)

    # printing number of pages in pdf file
    print("Number of pages detected:", reader.numPages)

    # getting a specific page from the pdf file
    page = reader.getPage(0)

    # extracting text from page
    text = page.extractText()


print("RAW OUTPUT:")
print(text)

#PART 2 -----
#Use regular expressions to identify and extract course details.
#Organize the extracted details into a structured format.
#Save the structured data to a JSON file.

# Sample data from the PDF
data = text

# Adjusted regular expression to match course details
pattern = r"([A-Z]{4} \d{4}[A-Z]?)([A-Za-z\s\-]+)((?:Fa|Sp|Su|--|\?\?)+)"

matches = re.findall(pattern, data)

courses = []

for match in matches:
    course_code = match[0]
    course_name = match[1].strip()
    semesters_offered = re.findall(r"Fa|Sp|Su", match[1] + match[2])  # Search in both course_name and the matched semester string

    # Remove the semesters from the course name
    for semester in semesters_offered:
        course_name = course_name.replace(semester, "").strip()

    course = {
        "Rubric Number": course_code,
        "Course Name": course_name,
        "Semesters Offered": semesters_offered
    }
    courses.append(course)

# Save to JSON file
with open('../data/prereqs.json', 'w') as json_file:
    json.dump(courses, json_file, indent=4)

print()
print("Prerequisites parsed & saved to prereqs.json file in the data folder")
