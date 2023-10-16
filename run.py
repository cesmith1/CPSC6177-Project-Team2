# filename: class_scheduler.py

import os
from functions.schedule_web_scraper import ScheduleWebScraper

def main():
    print("Hello, and welcome to the class scheduler. Please select an option from the list below.")
    print()
    print("a) Parse (Static) Prerequisite file")
    print("b) Parse DegreeWorksPDF")
    print("c) Webscrape & parse Class Schedule")
    
    choice = input("Enter your choice: ").strip().lower()

    if choice == 'a':
        #username = input("Press enter to run parser for prereq. courses : ").strip()
        os.system(f"python3 functions/prereq-parser.py")
    elif choice == 'b':
        print("b selected")
    elif choice == 'c':
        web_scraper = ScheduleWebScraper()
        print(web_scraper.formatted_schedule)
        # os.system(f"python3 functions/schedule_web_scraper.py")        
    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main()