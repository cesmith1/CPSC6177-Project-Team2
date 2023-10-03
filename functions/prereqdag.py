# Module containing the data structures for the prereq DAG. May rename and add other data structures (schedule and degreeworks) later.

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
        
    # Recursive sort method    
    def _recurTopoSort(self, v, visited, sorted, completed):
        visited[v] = True
        for u in self.dagDict[v].children:
            if visited[u] == False:
                self._recurTopoSort(u, visited, sorted, completed)
        # Don't add courses that are already completed
        if v not in completed:
            sorted.insert(0,v)

    # Function to return the list of "Rubric Number" in topologically sorted order.
    # Courses that are already completed will not be added to the result
    # Args: completedRubricNumbers - A list of already completed rubric nums
    def topoSort(self, completedRubricNumbers):
        visited = {}
        for k in self.dagDict:
            visited[k] = False
        sorted = []

        for v in self.dagDict:
            if visited[v] == False:
                self._recurTopoSort(v, visited, sorted, completedRubricNumbers)
        #TODO implement TopoSort
        return sorted

    # Rewriten string writer for pretty printing of the dictionary (not topologically sorted)
    def __str__(self):
        returnStr = ""
        for k,v in self.dagDict.items():
            returnStr += (f"{k}:\n\tname={v.name}\n\tsemestersOffered={v.semestersOffered}\n\tchildren={v.children}\n\totherReqs={v.otherReqs})\n")
        return returnStr
