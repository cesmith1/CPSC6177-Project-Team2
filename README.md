# CPSC6177-Project-Team2
Welcome to the repo that contains the Python code for the CPSC6177 semester project, the class scheduler.

## Purpose

The primary purpose of the class scheduler is to provide a student with a recommended CSU class schedule in 
order to complete their degree track. To accomplish this, the application uses a combination of user input
and data files in order to create an accurate estimate of which classes a student should take.

## Application Structure

### Data

All data other than direct user input is stored in the **_data_** subdirectory. 3 primary data sources are used
in execution.

1. **class_schedule.json** - A json representation of the class schedule as found on the [CSU website](https://catalog.columbusstate.edu/academic-units/business/computer-science/computer-science-bs-software-systems-track/).
2. **prereqs.json** - A json representation of the prerequites graph found in **_PrerequisiteGraph-Software_Systems2019-2020.pdf_**
3. **Sample Input1-3** - Degreeworks pdf files that contain the list of courses a student still requires

The degreeworks files may be in another directory and are directly provided by the user during execution,
but both json files are required to be in the **_data_** subdirectory for proper execution. The **_prereqs.json_**
file is static with no changes being made via any parser or webscraper. 
An existing **class_schedule.json** already exists in the repository, but the most up-to-date schedule can be pulled
using a webscraper built in to the application (see **Execution** section below).

### Functions

The class schedule application is modularized with all modules being stored in the **_functions_** subdirectory.
The modules utilized by the program are as follows:
1. **schedulewebscraper.py** - Webscraper utility for pulling class schedule data and generating the **_class_schedule.json_**
1. **degreeworksparser.py** - Contains the parser for degreeworks pdf files
2. **prereqparser.py** - A utility for extracting information from prereq pdf (not part of main execution)
3. **prereqdag.py** - A module that contain classes and functions involving the prerequisites graph
4. **classschedule.py** - A module that contain classes and functions involving the class schedule
5. **outputwriter.py** - Contains the XlsxWriter logic for writing the final **_output.xlsx_**

### Tests

The **_tests_** subdirectory contains all unit tests for the application. They can all be executed during the main
application's execution or by executing **_test_all.py**

## Execution

### Running the application

To start the class scheduler application, the **_run.py_** script in the root directory should be executed.
> [!IMPORTANT]
> In order to execute the application, python 3.11 or later should be installed on the host machine.
> See the **Requirements** and **Resources** sections below.

```
> cd CPSC6177-Project-Team2
> python run.py
```

### Program Usage

On execution, the user will be prompted to enter some details, including their full name and CSU number, the next 
academic year, and the upcoming semester.

```
Hello, and welcome to the class scheduler.

Enter your full name: John Doe
Enter your CSU ID: 123456789
Enter the next academic year (default=2023): 2023
Enter the next semester (Fall/Spring, default=Spring): Spring
```

After entering these details, the user will then be shown the main program menu

```
Please select an option from the list below.

s(crape): Execute class schedule webscraper
p(rint): Generate and export recommended class schedule
t(est): Run test cases
e(xit): Exit program
```

Selection can be done with a single letter or the entire option name (i.e. `s` or `scrap` will select the first option).
The options are further explained below:
- **scrape** - Executes the class schedule webscraper and writes the result to **_./data/class_schedule.json_**
- **print** - Pulls all data from **_data_** subdirectory and generates a class schedule, exporting it to **_./output.xlsx_**
- **test** - Executes all unit tests and prints the results to the console
- **exit** - Terminates the program

Any unexpected input will result in the program gracefully exiting. Once an operation has completed, the user will be
directed back to the main menu.

If **print** is selected, the user will be prompted to provide their degreeworks pdf file:
```
Provide the path to the degreeworks pdf containing the courses you still require for your degree track...

Input file: ./data/Sample Input2.pdf
```

> [!NOTE]
> Keep in mind that if **_class_schedule.json_** is deleted or removed from the **_data_** subdirectory,
> an error will occur when attempting to execute the **print** function. The webscraper will need to be 
> executed again before attempting to print a schedule. 

After executing **print**, the resulting schedule should be available in the same directory **_run.py_**
was executed from.

```
Writing recommended class schedule to "./output.xlsx"...
Recommended class schedule was successfully written to "./output.xlsx".
The application can now be terminated or run again to generate another class schedule.
```

## Requirements

- An personal computer or vritual machine with an OS capable of running Python 3
- Python 3.11.5 installed and optionally added to the system PATH for easy execution
- Git installed on your local machine to do your commits and pushes from local

## App Execution

In order to execute the program, make do 

## Resources
- [Python 3.11.5](https://www.python.org/downloads/release/python-3115/)
- [Git CLI](https://git-scm.com/downloads) (feel free to install a GUI as well if you need/want it)
