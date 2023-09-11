# filename: class_scheduler.py

import os

def main():
    print("Hello, and welcome to the class scheduler. Please select an option from the list below.")
    print()
    print("a) Parse (Static) Prerequisite file")
    print("b) Parse DegreeWorksPDF")
    print("c) Webscrape & parse Class Schedule")
    
    choice = input("Enter your choice: ").strip().lower()

    if choice == 'a':
        username = input("Press enter to run parser for prereq. courses : ").strip()
        os.system(f"python3 functions/prereq-parser.py")
    elif choice == 'b':
        print("b selected")
    elif choice == 'c':
        os.system(f"python3 functions/get_class_schedule.py")        
    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main()
