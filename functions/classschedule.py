# Module containing the data structures for the class schedule.

class Year:
    def __init__(self, year):
        self.semesters = {}
        for semester, classes in year.items():
            self.semesters[semester] = []
            for clazz in classes:
                self.semesters[semester].append(clazz['courseCode']);

class ClassSchedule:
    def __init__(self, jsonArray):
        self.yearList = []
        for _,year in jsonArray.items():
            self.yearList.append(Year(year))

    # Function to get all classes for a given year and semester
    # args: year - the students year (zero based 0 = first year), semester - either "Fall" or "Spring"
    def getClasses(self, year, semester):
        if semester.lower() == "fall":
            return self.yearList[year].semesters["Fall"]
        elif semester.lower() == "spring":
            return self.yearList[year].semesters["Spring"]
    
    def __str__(self):
        i = 0
        returnStr = ""
        for year in self.yearList:
            returnStr += f"Year {i+1}:\n"
            for semester, classes in year.semesters.items():
                returnStr += f"\t{semester}:{classes}\n"
            i += 1
        return returnStr