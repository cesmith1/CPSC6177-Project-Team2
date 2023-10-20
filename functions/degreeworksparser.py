import re
from py_pdf_parser.loaders import load_file

filepath = ("../data/Sample Input3.pdf")

class StillNeededCourse:

    def __init__(self, numCourses, courseList):
        self.numCourses, self.courseList = numCourses, courseList

    def __str__(self):
        return '{' + f"'numCourses':{self.numCourses}, 'courseList':{self.courseList}" + '}'
    
    __repr__ = __str__

def parseDegreeworksFile(filepath):
    choose_from = []
    results = []

    document = load_file(filepath)
    still_needed_elements = document.elements.filter_by_text_contains("Still Needed:")

    for el in still_needed_elements:
        try:
            element = document.elements.to_the_right_of(el).extract_single_element().text()
            # print(element)
            element = " ".join(element.split()) # remove extra spaces between words

            # get startwith text ("1 Class in..." or  "6 Credits in")
            num_class_credit = element.split(" ")[0]  

            if "Choose from" in element:
                num_course = re.search(r'\d+', element).group()
                choose_from.append([int(num_course), []])
                
            elif "( " in element:
                code = re.search(r'[A-Z]{4} \d{4}[A-Z]?', element).group()
                choose_from[len(choose_from) - 1][1].append(code)
                
            elif re.match(r'^\d+ Class', element, re.IGNORECASE):
                class_list = []
                if " or " in element:
                    split_or = element.split(' or ')
                    class_one = re.search(r'[A-Z]{4} \d{4}[A-Z]?', split_or[0]).group()
                    code_prefix = class_one.split(" ")[0]
                    class_list.append(class_one)
                    remaining_courses = []
                    course_num_only_pattern = '\d{4}[A-Z]?'
                    remaining_courses = [ f"{code_prefix} {re.search(course_num_only_pattern, split_or[i]).group()}" if not re.match(r'^[A-Z]{4}', split_or[i]) else split_or[i] for i in range(1, len(split_or)) ]
                    class_list += remaining_courses
                else:
                    class_list.append(re.search(r'[A-Z]{4} \d{4}[A-Z]?', element).group())
                
                results.append(StillNeededCourse(int(num_class_credit), class_list))
            
            elif re.match(r'^\d+ Credit', element, re.IGNORECASE):
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
                        remaining_courses = [ f"{code_prefix} {re.search(course_num_only_pattern, split_or[i]).group()}" if not re.match(r'^[A-Z]{4}', split_or[i]) else split_or[i] for i in range(1, len(split_or)) ]
                        
                        remaining_courses = [ re.search(r'[A-Z]{4} \d{4}', c).group() for c in remaining_courses ]
                        classes += remaining_courses

                else:
                    num_class_credit = int(num_class_credit) // 3 if int(num_class_credit) % 3 == 0 else 1
                    classes = re.findall(r'[A-Z]{4} \d{1}XXX', element)

                results.append(StillNeededCourse(int(num_class_credit), classes))

        except:
            pass
    
    # print(choose_from)
    if choose_from:  # add choose_from list to results
        for c in choose_from:
            results.append(StillNeededCourse(c[0], c[1]))

    return results

    
#print(parseDegreeworksFile(filepath))
