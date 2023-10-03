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
            self.dagDict[node["Rubric Number"]] = DAGClass(node["Course Name"], node["Semesters Offered"], node["Children"], node["Other Reqs"])
        
    # Function to return the list of "Rubric Number" in topologically sorted order
    def topoSort(self, completedRubricNumbers):
        sorted = []
        #TODO implement TopoSort
        return sorted

    # Rewriten string writer for pretty printing of the dictionary (not topologically sorted)
    def __str__(self):
        returnStr = ""
        for k,v in self.dagDict.items():
            returnStr += (f"{k}:\n\tname={v.name}\n\tsemestersOffered={v.semestersOffered}\n\tchildren={v.children}\n\totherReqs={v.otherReqs})\n")
        return returnStr
