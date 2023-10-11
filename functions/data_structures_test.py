# Quick class for demoing the prereq DAG
import json
from prereqdag import PrereqDAG
from classschedule import ClassSchedule

file = open("../data/prereqs.json", "r")
dag = PrereqDAG(json.load(file))
print(dag.getPrereqs("CPSC 4176"))
print(dag.topoSort([]))
print(dag)
file.close()

file = open("../data/class_schedule.json", "r")
schedule = ClassSchedule(json.load(file))
print(schedule.getRequirements(1,"Fall"))
print(schedule)
file.close()