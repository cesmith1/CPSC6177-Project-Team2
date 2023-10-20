# Quick class for demoing the prereq DAG
import json
from prereqdag import PrereqDAG
from classschedule import ClassSchedule
from schedule_web_scraper import ScheduleWebScraper

file = open("../data/prereqs.json", "r")
dag = PrereqDAG(json.load(file))
print("PRINTED DAG:\n\n"+str(dag)+"\n\n")
print("TOPOLOGICALLY SORTED:\n\n"+str(dag.topoSort(["MATH 1113","MATH 2125","CPSC 1301K"]))+"\n\n")
print("PREREQ TREE FOR \"CPSC 4176\"\n\n"+str(dag.getPrereqs("CPSC 4176"))+"\n\n")
file.close()

web_scraper = ScheduleWebScraper()
class_schedule_file_path = web_scraper.class_schedule_json_path
file = open(class_schedule_file_path, "r")
schedule = ClassSchedule(json.load(file))
print("PRINTED CLASS SCHEDULE:\n\n"+str(schedule)+"\n\n")
print("ALL REQS FOR FIRST YEAR FALL:\n\n"+str(schedule.getRequirements(1,"Fall"))+"\n\n")
print("WHEN IS CPSC 2108 AVAILABLE?:\n\n"+str(schedule.getAvailability("CPSC 2108"))+"\n\n")
file.close()