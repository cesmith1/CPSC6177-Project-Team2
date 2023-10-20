# filename: class_scheduler.py

import os
import sys
import subprocess
from pathlib import Path
from json import load
from functions.schedulewebscraper import ScheduleWebScraper
from functions.prereqdag import PrereqDAG
from functions.classschedule import CourseInfo, ClassSchedule
from functions.degreeworksparser import parseDegreeworksFile, StillNeededCourse
from functions.outputwriter import OutputWriter, OutputClass
sys.path.append('tests')

ROOT_DIR = Path(__file__).parent

def main():
    print("Hello, and welcome to the class scheduler.")
    print()
    studentName = input("Enter your full name: ").strip()
    csuId = input("Enter your CSU ID: ").strip()
    startingYear = input("Enter the next academic year (default=2023): ").strip()
    if startingYear == "":
        startingYear = 2023

    else:
        startingYear = int(startingYear)  # Convert the input to an integer
            
    startingSemester = input("Enter the next semester (Fall/Spring, default=Spring): ").strip().lower()
    if startingSemester == "spring" or startingSemester == "":
        startingSemester = "Spring"
    elif startingSemester == "fall":
        startingSemester = "Fall"
    else:
        print("Invalid semester name. Exiting...")
        sys.exit(1)

    while(True):
        print()
        print("Please select an option from the list below.")
        print()
        print("s(crape): Execute class schedule webscraper ")
        print("p(rint): Generate and export recommended class schedule")
        print("t(est): Run test cases")
        print("e(xit): Exit program")
        print()
        
        choice = input("Enter your choice: ").strip().lower()
        print()

        if choice == 's' or choice == 'scrape':
            print('Scraping course schedule from CSU website')
            webScraper = ScheduleWebScraper()
            print(f'Course schedule has been exported to "{webScraper.class_schedule_json_path}"')

        elif choice == 'p' or choice == 'print':
            print("Provide the path to the degreeworks pdf containing the courses you still require for your degree track...")
            print()
            degreeworksFilePath = input("Input file: ").strip()
            stillNeededCourseList = generateStillNeededCourseList(degreeworksFilePath)
            classSchedule = generateClassSchedule()
            prereqs = generatePrereqs()
            recommendedSchedule = getRecommendedSchedule(stillNeededCourseList, classSchedule, prereqs, startingSemester)
            outputWriter = OutputWriter(studentName, csuId, startingYear)
            writeResults(outputWriter, recommendedSchedule)

        elif choice == 't' or choice == 'test':
            subprocess.call("python3 tests/test_all.py", shell=True)

        elif choice == 'e' or choice == 'exit':
            print("Exiting...")
            sys.exit(0)

        else:
            print("Invalid choice. Exiting...")
            sys.exit(1)

def generateStillNeededCourseList(degreeworksFilePath):
    print('Retrieving still needed courses from degreeworks pdf...')
    stillNeededCourseList = parseDegreeworksFile(degreeworksFilePath)
    print('Still needed course list successfully parsed and loaded.')
    return stillNeededCourseList

def generatePrereqs():
    print('Retrieving prerequisites from json file...')
    prereqsFile = open(ROOT_DIR / 'data/prereqs.json')
    prereqsJson = load(prereqsFile)
    prereqsFile.close()
    prereqs = PrereqDAG(prereqsJson)
    print('Prerequisites successfully parsed and loaded.')
    return prereqs

def generateClassSchedule():
    print('Retrieving class schedule from json file...')
    prereqsFile = open(ROOT_DIR / 'data/class_schedule.json')
    prereqsJson = load(prereqsFile)
    prereqsFile.close()
    classSchedule = ClassSchedule(prereqsJson)
    print('Class schedule successfully parsed and loaded.')
    return classSchedule

def getRecommendedSchedule(stillNeededCourseList, classSchedule, prereqs, startingSemester):
    print('Preparing recommended class schedule...')
    recommendedSchedule = []
    for _ in range(len(classSchedule.yearList)):
        recommendedSchedule.append({'Fall':[], 'Spring':[]})
    for stillNeededCourse in stillNeededCourseList:
        foundOne = False
        for potentialCourseCode in stillNeededCourse.courseList:
            availableCourses = classSchedule.getAvailability(potentialCourseCode)
            removeUnavailableCourses(availableCourses, startingSemester)
            if len(availableCourses) > 0:
                selectedCourse = availableCourses[0]
                prereqCourseInfo = prereqs.getClass(selectedCourse.code)
                outputClass = OutputClass(selectedCourse.code, selectedCourse.name, prereqCourseInfo.semestersOffered, selectedCourse.credit, prereqCourseInfo.otherReqs)
                recommendedSchedule[selectedCourse.year][selectedCourse.semester].append(outputClass)
                foundOne = True
                break
        if not foundOne:
            print(f"Warning! Couldn't find any course in the class schedule for a requirement: {stillNeededCourse.courseList}")
    print('Recommended class schedule generated.')
    return recommendedSchedule

# Print results to file
def writeResults(outputWriter, recommendedSchedule):
    print('Writing recommended class schedule to "./output.xlsx"...')
    for yearIndex in range(len(recommendedSchedule)):
        for semester in recommendedSchedule[yearIndex]:
            outputWriter.addSemesterToWriter(yearIndex, semester, recommendedSchedule[yearIndex][semester])
    outputWriter.write()
    print('Recommended class schedule was successfully written to "./output.xlsx".')
    print('The application can now be terminated or run again to generate another class schedule.')
    outputWriter.close()

# Remove any courses from the running that are in first year Spring if the starting semester is fall
def removeUnavailableCourses(availableCourses, startingSemester):
    if startingSemester == 'Spring':
        return
    for index in range(len(availableCourses)):
        if availableCourses[index].year == 0 and availableCourses[index].semester == 'Spring':
            del availableCourses[index]

if __name__ == "__main__":
    main()
