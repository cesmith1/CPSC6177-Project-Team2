# Module containing the data structures for the class schedule.

# class for storing each class found in the get metho
class CourseInfo:
    def __init__(self, year, semester, code, name, credit):
        self.year = year
        self.semester = semester
        self.code = code
        self.name = name
        self.credit = credit
    
    def __str__(self):
        return '{' + f'"year":{self.year}, "semester":"{self.semester}", "code":"{self.code}", "name":"{self.name}", "credit":{self.credit}' + '}'

    __repr__ = __str__

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

    # Function to get the year and semester a course is in given its course code
    # args: course code (eg. "CPSC 2108")
    def getAvailability(self, courseCode):
        available = []
        yearIndex = 0
        for year in self.yearList:
            for semester, reqs in  year.semesters.items():
                for req in reqs:
                    for course in req.courses:
                        if courseCode.casefold() in course.code.casefold():
                            available.append(CourseInfo(yearIndex, semester, course.code, course.name, req.courseCredit))
            yearIndex += 1
        return available
    
    def __str__(self):
        i = 0
        returnStr = ""
        for year in self.yearList:
            returnStr += f"Year[{i}]:\n"
            for semester, reqs in year.semesters.items():
                returnStr += f"\t{semester}:\n"
                for req in reqs:
                    returnStr += "\t\tCourses:\n"
                    for course in req.courses:
                        returnStr += f"\t\t\t{course.code} ({course.name})\n"
                    returnStr += f"\t\tCredit:{req.courseCredit}\n"
            i += 1
        return returnStr
