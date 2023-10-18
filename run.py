# filename: class_scheduler.py

import os
import sys
sys.path.append('functions')
#from prereq-parser import print_prereq-parser_output
#from degreeworks_parser import print_degreeworks_parser_output
from functions.schedule_web_scraper import ScheduleWebScraper

def main():
    print("Hello, and welcome to the class scheduler. Please select an option from the list below.")
    print()
    print("a) Parse (Static) Prerequisite file")
    print("b) Parse DegreeWorksPDF")
    print("c) Webscrape & parse Class Schedule")
    print("d) Run test case")
    
    choice = input("Enter your choice: ").strip().lower()

    if choice == 'a':
        #username = input("Press enter to run parser for prereq. courses : ").strip()
        os.chdir("functions")
        os.system(f"python3 prereq-parser.py")
        #print_prereq-parser_output()

    elif choice == 'b':
        os.chdir("functions")
        os.system(f"python3 degreeworks_parser.py")
        #print_degreeworks_parser_output()

    elif choice == 'c':
        web_scraper = ScheduleWebScraper()
        print(web_scraper.formatted_schedule)
        os.chdir("functions")
        os.system(f"python3 schedule_web_scraper.py")    

    elif choice == 'd':
        os.chdir("tests")
        os.system(f"python3 test_all.py")

    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main()
