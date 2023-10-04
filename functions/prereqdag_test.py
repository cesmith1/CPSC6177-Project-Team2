# Quick class for demoing the prereq DAG
import json
from prereqdag import PrereqDAG

file = open("../data/prereqs.json", "r")
dag = PrereqDAG(json.load(file))
print(dag.getPrereqs("CPSC 4176"))
print(dag.topoSort([]))