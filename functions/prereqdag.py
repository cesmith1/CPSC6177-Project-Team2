# Module containing the data structures for the prereq DAG.

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


    # Rewriten string writer for pretty printing of the dictionary (not topologically sorted)
    def __str__(self):
        returnStr = ""
        for k,v in self.dagDict.items():
            returnStr += (f"{k}:\n\tname={v.name}\n\tsemestersOffered={v.semestersOffered}\n\tchildren={v.children}\n\totherReqs={v.otherReqs})\n")
        return returnStr
