# Module containing the data structures for the class schedule.
class Course:
    def __init__(self, course):
        self.code = course['code']
        self.name = course['name']
    
class Requirement:
    def __init__(self, req):
        self.courses = []
        for course in req['courses']:
            self.courses.append(Course(course))
        self.courseCredit = req['courseCredit']
    
    def __str__(self):
        returnStr = "\nCourses:\n"
        for course in self.courses:
            returnStr += f"\t{course.code} ({course.name})\n"
        returnStr += f"Credit:{self.courseCredit}\n"
        return returnStr    
    
    __repr__ = __str__

class Year:
    def __init__(self, year):
        self.semesters = {}
        for semester, requirements in year.items():
            self.semesters[semester] = []
            for req in requirements:
                self.semesters[semester].append(Requirement(req))

class ClassSchedule:
    def __init__(self, jsonArray):
        self.yearList = []
        for year in jsonArray.values():
            self.yearList.append(Year(year))

    # Function to get all classes for a given year and semester
    # args: year - the students year (zero based 0 = first year), semester - either "Fall" or "Spring"
    def getRequirements(self, year, semester):
        if semester.lower() == "fall":
            return self.yearList[year].semesters["Fall"]
        elif semester.lower() == "spring":
            return self.yearList[year].semesters["Spring"]
    
    def __str__(self):
        i = 0
        returnStr = ""
        for year in self.yearList:
            returnStr += f"Year {i+1}:\n"
            for semester, reqs in year.semesters.items():
                returnStr += f"\t{semester}:\n"
                for req in reqs:
                    returnStr += "\t\tCourses:\n"
                    for course in req.courses:
                        returnStr += f"\t\t\t{course.code} ({course.name})\n"
                    returnStr += f"\t\tCredit:{req.courseCredit}\n"
            i += 1
        return returnStr