import re
from py_pdf_parser.loaders import load_file

# Define the file path for the PDF to be parsed
filepath = ("../data/Sample Input3.pdf")

# Define a class for representing still needed courses
class StillNeededCourse:

    def __init__(self, numCourses, courseList):
        self.numCourses, self.courseList = numCourses, courseList

    def __str__(self):
        return '{' + f"'numCourses':{self.numCourses}, 'courseList':{self.courseList}" + '}'

    __repr__ = __str__

# Function to parse the DegreeWorks PDF file
def parseDegreeworksFile(filepath):
    choose_from = []  # List to store "Choose from" courses
    results = []      # List to store parsed course information

    # Load the PDF document
    document = load_file(filepath)

    # Find elements in the document containing the text "Still Needed:"
    still_needed_elements = document.elements.filter_by_text_contains("Still Needed:")

    for el in still_needed_elements:
        try:
            # Extract and clean the text from the element
            element = document.elements.to_the_right_of(el).extract_single_element().text()
            element = " ".join(element.split())  # Remove extra spaces between words

            # Get the text at the beginning ("1 Class in..." or "6 Credits in")
            num_class_credit = element.split(" ")[0]

            if "Choose from" in element:
                # If it's a "Choose from" section, extract the number of courses and initialize an empty list
                num_course = re.search(r'\d+', element).group()
                choose_from.append([int(num_course), []])

            elif "( " in element:
                # If it's a course code, add it to the last "Choose from" section
                code = re.search(r'[A-Z]{4} \d{4}[A-Z]?', element).group()
                choose_from[len(choose_from) - 1][1].append(code)

            elif re.match(r'^\d+ Class', element, re.IGNORECASE):
                # If it's a "Class" requirement, parse the course list
                class_list = []

                if " or " in element:
                    # If there are multiple options, split and extract them
                    split_or = element.split(' or ')
                    class_one = re.search(r'[A-Z]{4} \d{4}[A-Z]?', split_or[0]).group()
                    code_prefix = class_one.split(" ")[0]
                    class_list.append(class_one)
                    remaining_courses = []
                    course_num_only_pattern = '\d{4}[A-Z]?'
                    remaining_courses = [f"{code_prefix} {re.search(course_num_only_pattern, split_or[i]).group()}" if not re.match(r'^[A-Z]{4}', split_or[i]) else split_or[i] for i in range(1, len(split_or))]
                    class_list += remaining_courses
                else:
                    class_list.append(re.search(r'[A-Z]{4} \d{4}[A-Z]?', element).group())

                results.append(StillNeededCourse(int(num_class_credit), class_list))

            elif re.match(r'^\d+ Credit', element, re.IGNORECASE):
                # If it's a "Credit" requirement, parse the course list
                classes = []

                if re.compile(r' \d@').search(element):
                    element = element.replace("@", "XXX")

                if int(num_class_credit) < 3:
                    if " or " in element:
                        split_or = element.split(' or ')
                        class_one = re.search(r'[A-Z]{4} \d{4}[A-Z]?', split_or[0]).group()
                        code_prefix = class_one.split(" ")[0]
                        classes.append(class_one)
                        remaining_courses = []
                        course_num_only_pattern = '\d{4}[A-Z]?'
                        remaining_courses = [f"{code_prefix} {re.search(course_num_only_pattern, split_or[i]).group()}" if not re.match(r'^[A-Z]{4}', split_or[i]) else split_or[i] for i in range(1, len(split_or))]

                        remaining_courses = [re.search(r'[A-Z]{4} \d{4}', c).group() for c in remaining_courses]
                        classes += remaining_courses
                else:
                    num_class_credit = int(num_class_credit) // 3 if int(num_class_credit) % 3 == 0 else 1
                    classes = re.findall(r'[A-Z]{4} \d{1}XXX', element)
                results.append(StillNeededCourse(int(num_class_credit), classes))

        except:
            pass

    # Add the "Choose from" courses to the results
    if choose_from:
        for c in choose_from:
            results.append(StillNeededCourse(c[0], c[1]))

    return results

# Uncomment the following line to test the parsing function
# print(parseDegreeworksFile(filepath))
