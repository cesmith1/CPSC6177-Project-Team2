# Module containing the data structures for the prereq DAG.

# Class to store an error in the case that a preq rule is violated
class PrereqViolation:
    def __init__(self, prereqs, causeCourse):
        self.prereqs, self.causeCourse = prereqs, causeCourse

    def getMessage(self):
        return f"'{self.causeCourse}' should be taken before courses: {self.prereqs}"

    __str__ = getMessage
    __repr__ = getMessage

# Class for each node in the dictionary "Rubric Number":{class object}
class DAGClass:
    def __init__(self, name, semestersOffered, children, otherReqs):
        self.name, self.semestersOffered, self.children, self.otherReqs = name, semestersOffered, children, otherReqs

# Primary class for storing the prereqs. This should be the primary class imported from this module.
class PrereqDAG:
    # Initialize the dictionary of classes from the json file
    def __init__(self, jsonArray):
        self.dagDict = {}
        for node in jsonArray:
            # Adding an additional number at the end of duplicate rubric nums (starting with 1)
            key = node["Rubric Number"]
            n = 0
            while key in self.dagDict:
                n += 1
                key += " " + str(n)
            self.dagDict[key] = DAGClass(node["Course Name"], node["Semesters Offered"], node["Children"], node["Other Reqs"])
        
    # Private helper function - recursive topological sort of stored prereqs DAG.   
    def _recurTopoSort(self, v, visited, sorted, incomplete):
        visited[v] = True
        for u in self.dagDict[v].children:
            if visited[u] == False:
                self._recurTopoSort(u, visited, sorted, incomplete)
        # Only add courses that are explicitely incomplete
        if v in incomplete:
            sorted.insert(0,v)

    # Returns the list of "Rubric Number" in topologically sorted order.
    # Courses that are already completed will not be added to the result
    # Args: incompleteRubricNumbers - A list of course rubric nums not yet completed.
    def topoSort(self, incompleteRubricNumbers):

        visited = {}
        for k in self.dagDict:
            visited[k] = False
        sorted = []

        for v in self.dagDict:
            if visited[v] == False:
                self._recurTopoSort(v, visited, sorted, incompleteRubricNumbers)
        return sorted
    
    # Identify and return any prereq violations in a schedule
    def getPrereqViolations(self, recommendedSchedule):
        # Store return value here, list of prereq violations (Will be empty if none are found)
        prereqViolations = []
        # List to store all courses taken in each semester as we go along
        completedCourses = []
        for year in recommendedSchedule:
            for courses in year.values():
                # Add all courses taken this semester to completed courses
                for course in courses:
                    completedCourses.append(course.code)
                # Iterate over courses added this semester
                for course in courses:
                    # List to store each missing prereq for a given course
                    shouldBePrereqs = []
                    # Iterate over all courses taken (including this semster)
                    for completedCourse in completedCourses:
                        # Get all prereqs for the completed course
                        prereqCodes = self.getPrereqs(completedCourse)
                        # Add completed course to missing prereqs list if the course taken this semester is a prereq for a completed course
                        if course.code in prereqCodes:
                            shouldBePrereqs.append(completedCourse)
                    # Store missing prereqs for the course if they were found
                    if shouldBePrereqs:
                        prereqViolations.append(PrereqViolation(shouldBePrereqs, course.code))
        return prereqViolations
    
    # Private helper function - recursive search for prereqs of a given class.
    # Results are stored in prereqs variable as a list of rubric numbers.   
    def _recurGetPrereqs(self, rubricNum, prereqs):
        for parentNum, parentData in self.dagDict.items():
            if rubricNum in parentData.children:
                self._recurGetPrereqs(parentNum, prereqs)
                if parentNum not in prereqs:
                    prereqs.append(parentNum)
    
    # Get a list of all prereqs for a given class
    # Args: rubricNum - The rubric number (eg. CPSC 2108) to get the prereqs for
    def getPrereqs(self, rubricNum):
        prereqs = []
        self._recurGetPrereqs(rubricNum, prereqs)
        return self.topoSort(prereqs)
    
    def getClass(self, classCode):
        if classCode in self.dagDict:
            return self.dagDict[classCode]
        return DAGClass('', [], [], [])

    # Rewriten string writer for pretty printing of the dictionary (not topologically sorted)
    def __str__(self):
        returnStr = ""
        for k,v in self.dagDict.items():
            returnStr += (f"{k}:\n\tname={v.name}\n\tsemestersOffered={v.semestersOffered}\n\tchildren={v.children}\n\totherReqs={v.otherReqs})\n")
        return returnStr
