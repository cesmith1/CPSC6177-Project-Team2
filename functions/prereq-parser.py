#TO DO:
#Import PDF -> extract text -> parse courses, then store courses in local JSON

#PART 2:
#Use regular expressions to identify and extract course details.
#Organize the extracted details into a structured format.
#Save the structured data to a JSON file.


# importing required modules
import os
from PyPDF2 import PdfReader
  
# creating a pdf reader object
reader = PdfReader('../PrerequisiteGraph-Software_Systems2019-2020.pdf')
  
# printing number of pages in pdf file
print("Number of pages detected:",len(reader.pages))
  
# getting a specific page from the pdf file
page = reader.pages[0]
  
# extracting text from page
text = page.extract_text()

print("RAW OUTPUT:")
print(text)

#PART 2 -----
#Use regular expressions to identify and extract course details.
#Organize the extracted details into a structured format.
#Save the structured data to a JSON file.

import re
import json

# Sample data from the PDF
data = text

# Adjusted regular expression to match course details
pattern = r"([A-Z]{4} \d{4}[A-Z]?)([A-Za-z\s\-]+)((?:Fa|Sp|Su|--|\?\?)+)"

matches = re.findall(pattern, data)

courses = []

for match in matches:
    course_code = match[0]
    course_name = match[1].strip()
    semesters_offered = re.findall(r"Fa|Sp|Su", match[2])

    course = {
        "Rubric Number": course_code,
        "Course Name": course_name,
        "Semesters Offered": semesters_offered
    }
    courses.append(course)

# Save to JSON file
with open('data/prereqs.json', 'w') as json_file:
    json.dump(courses, json_file, indent=4)


print()
print("Prerequisites parsed & saved to prereqs.json file in the data folder")
