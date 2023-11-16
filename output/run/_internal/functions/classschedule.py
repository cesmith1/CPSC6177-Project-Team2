# This module contains the data structures for representing a class schedule.

# CourseInfo class represents the details of a course, including its year, semester, code, name, and credit.
class CourseInfo:
    def __init__(self, year, semester, code, name, credit):
        # The year the course is offered.
        self.year = year
        # The semester (e.g., "Fall", "Spring") the course is offered.
        self.semester = semester
        # The code identifier for the course (e.g., "CPSC 2108").
        self.code = code
        # The human-readable name of the course.
        self.name = name
        # The credit value for the course.
        self.credit = credit

    # String representation of the CourseInfo object.
    def __str__(self):
        return '{' + f'"year":{self.year}, "semester":"{self.semester}", "code":"{self.code}", "name":"{self.name}", "credit":{self.credit}' + '}'

    __repr__ = __str__


# Course class represents a simplified version of a course with just the code and name.
class Course:
    def __init__(self, course):
        self.code = course['code']
        self.name = course['name']


# Requirement class represents a set of courses and their total credit requirement.
class Requirement:
    def __init__(self, req):
        # List of courses under this requirement.
        self.courses = []
        for course in req['courses']:
            self.courses.append(Course(course))
        # Total credits for this requirement.
        self.courseCredit = req['courseCredit']

    # String representation of the Requirement object.
    def __str__(self):
        returnStr = "\nCourses:\n"
        for course in self.courses:
            returnStr += f"\t{course.code} ({course.name})\n"
        returnStr += f"Credit:{self.courseCredit}\n"
        return returnStr

    __repr__ = __str__


# Year class represents the academic year with the courses and requirements for each semester.
class Year:
    def __init__(self, year):
        # Dictionary storing the semesters (e.g., "Fall", "Spring") and their respective requirements.
        self.semesters = {}
        for semester, requirements in year.items():
            self.semesters[semester] = []
            for req in requirements:
                self.semesters[semester].append(Requirement(req))


# ClassSchedule class represents the entire academic schedule for a student.
class ClassSchedule:
    def __init__(self, jsonArray):
        # List of Year objects representing each academic year in the schedule.
        self.yearList = []
        for year in jsonArray.values():
            self.yearList.append(Year(year))

    # Returns the course requirements for a given year and semester.
    def getRequirements(self, year, semester):
        if semester.lower() == "fall":
            return self.yearList[year].semesters["Fall"]
        elif semester.lower() == "spring":
            return self.yearList[year].semesters["Spring"]

    # Returns a list of CourseInfo objects representing the availability of a course given its course code.
    def getAvailability(self, courseCode):
        available = []
        yearIndex = 0
        for year in self.yearList:
            for semester, reqs in year.semesters.items():
                for req in reqs:
                    for course in req.courses:
                        if courseCode.casefold() in course.code.casefold():
                            available.append(
                                CourseInfo(yearIndex, semester, course.code, course.name, req.courseCredit))
            yearIndex += 1
        return available

    # String representation of the entire ClassSchedule.
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
