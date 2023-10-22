# Quick class for demoing the prereq DAG

# Import required libraries
import json
from prereqdag import PrereqDAG
from classschedule import ClassSchedule
from schedule_web_scraper import ScheduleWebScraper

# Open and load the JSON file containing prerequisite information into a PrereqDAG object
file = open("../data/prereqs.json", "r")
dag = PrereqDAG(json.load(file))

# Print the original DAG
print("PRINTED DAG:\n\n" + str(dag) + "\n\n")

# Get the topologically sorted DAG for specified courses and print it
print("TOPOLOGICALLY SORTED:\n\n" + str(dag.topoSort(["MATH 1113", "MATH 2125", "CPSC 1301K"])) + "\n\n")

# Get the prerequisite tree for a specific course ("CPSC 4176") and print it
print("PREREQ TREE FOR \"CPSC 4176\"\n\n" + str(dag.getPrereqs("CPSC 4176")) + "\n\n")

# Close the JSON file
file.close()

# Initialize a ScheduleWebScraper object to fetch class schedule data
web_scraper = ScheduleWebScraper()
class_schedule_file_path = web_scraper.class_schedule_json_path

# Open and load the JSON file containing the formatted class schedule into a ClassSchedule object
file = open(class_schedule_file_path, "r")
schedule = ClassSchedule(json.load(file))

# Print the formatted class schedule
print("PRINTED CLASS SCHEDULE:\n\n" + str(schedule) + "\n\n")

# Get all requirements for the first year in the fall semester and print them
print("ALL REQS FOR FIRST YEAR FALL:\n\n" + str(schedule.getRequirements(1, "Fall")) + "\n\n")

# Check when the course "CPSC 2108" is available and print the result
print("WHEN IS CPSC 2108 AVAILABLE?:\n\n" + str(schedule.getAvailability("CPSC 2108")) + "\n\n")

# Close the JSON file
file.close()
