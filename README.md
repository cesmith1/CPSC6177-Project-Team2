# CPSC6177-Project-Team2
Welcome to the repo that contains the Python code for the CPSC6177 semester project, the *Smart Class Planner*.

## Purpose

The primary purpose of the *Smart Class Planner* is to provide a student with a recommended CSU class schedule in 
order to complete their degree track. To accomplish this, the application uses a combination of user input
and data files in order to create an accurate estimate of which classes a student should take.

## Application Structure

### Data

All data other than direct user input is stored in the **_data_** subdirectory (**_/_internal/data_** in the compiled binary). 3 primary data sources are used
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

The *Smart Class Planner* application is modularized with all modules being stored in the **_functions_** subdirectory.
The modules utilized by the program are as follows:
1. **schedulewebscraper.py** - Webscraper utility for pulling class schedule data and generating the **_class_schedule.json_**
1. **degreeworksparser.py** - Contains the parser for degreeworks pdf files
2. **prereqparser.py** - A utility for extracting information from prereq pdf (not part of main execution)
3. **prereqdag.py** - A module that contain classes and functions involving the prerequisites graph
4. **classschedule.py** - A module that contain classes and functions involving the class schedule
5. **outputwriter.py** - Contains the XlsxWriter logic for writing the final **_output.xlsx_**

### Tests

To execute test cases, run the following after installing all requirements (see **Compiling** note):

```
> python -m coverage run -m unittest
```

You can then view the code coverage report using the coverage tool:

```
> python -m coverage report
```

## Compiling

> [!IMPORTANT]
> In order to build or execute the application, python 3.11 or later should be installed on the host machine.
> Package manager *pip* is used to manage dependencies. 
> *requirements.txt* in project root directory contains all required packages. 
> Run ```pip install -r requirements.txt``` to install them before running the application. 
> See the **Requirements** and **Resources** sections below.

### Automated Compiling

The **_build.sh_** script included in the repo's root directory will compile the application automatically.

```
> cd CPSC6177-Project-Team2
> ./build.sh
```

Once compilation is complete, the resulting binary and data files will be stored in **_./dist/SmartClassPlanner/_**.

All files in the **_data_** directory will be packaged in the **_./dist/SmartClassPlanner/_included_** directory.
This directory must remain in the same directory as the **_SmartClassPlanner.exe_** executable, as it contains resources
that are required for the executable.

### Manual Compiling

*pyinstall* can be invoked manually to customize the build. This may be useful to produce a portable executable with the **--onefile**
directive or some other custom build options. The build method executed by the script is the following:

```
> pyinstaller run.py --add-data="data:data" --name SmartClassPlanner
```

## Installation

### Automated Installation

The latest release build can be found in the [releases](https://github.com/cesmith1/CPSC6177-Project-Team2/releases) section
in this repo. The release can be downloaded in both a binary zip format and a windows installer packages through 
[Advanced Installer](https://www.advancedinstaller.com/).

To use the installer, download and run the **_SmartClassPlanner-Setup-x86.msi_** installer from releases. Follow the prompts to
install. Use all default options. Select "Install" when prompted.

![image](https://github.com/cesmith1/CPSC6177-Project-Team2/assets/144077890/a2d21519-fd4b-4979-bf7f-2efe5f882c53)

The automated installer places the executable and its data files inside **_%APPDATA%/SmartClassPlanner/_**

Once installation is complete, the *SmartClassPlanner* will be added to the active user's Path variable. The program can be
executed by opening a *Command Prompt* or *PowerShell* and executing the following command:

```
> SmartClassPlanner
> Hello, and welcome to the Smart Class Planner.
> ...
```

### Manual Installation

To use the binary zip, unzip the contents of the **_SmartClassPlanner.zip_** archive and execute the program by navigating 
into the **_SmartClassPlanner_** directory and launching the **_SmartClassPlanner.exe_** executable from a *Command Prompt* or *PowerShell*. 

```
> tar -xf SmartClassPlanner.zip
> cd SmartClassPlanner
> SmartClassPlanner
Hello, and welcome to the Smart Class Planner.
...
```

Optionally, the **_SmartClassPlanner_** directory can be added to the Path variable to make the program accessable
from *Command Prompt* or *PowerShell* globally.

If you have built the application from its source code, you can also execute the program from **_./dist/SmartClassPlanner/SmartClassPlanner.exe_**

## Execution

### Running the Application

> [!IMPORTANT]
> Follow the  **Installation** section above first to setup the SmartClassPlanner.
> The following guide assumes that you have either followed the **Automated Installation**, added the application to your Path,
> or are executing the program from its parent directory.

After installation, execute the application from *Command Prompt* or *PowerShell*

```
> SmartClassPlanner
```

### Program Usage

#### Main Menu

On execution, the user will be prompted to enter some details, including their full name and CSU number, the next 
academic year, and the upcoming semester.

```
Hello, and welcome to the Smart Class Planner.

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
e(xit): Exit program
```

Selection can be done with a single letter or the entire option name (i.e. `s` or `scrape` will select the first option).
The options are further explained below:
- **scrape** - Executes the class schedule webscraper and writes the result to **__internal/data/class_schedule.json_**
- **print** - Pulls all data from **_data_** subdirectory and generates a class schedule, exporting it to **_./output.xlsx_**
- **exit** - Terminates the program

Any unexpected input will result in the program gracefully exiting. Once an operation has completed, the user will be
directed back to the main menu.

#### CSU Class Schedule Webscraper

If **s(crap)** is selected, the class schedule webscraper will execute and store the resulting class schedule in 
**__internal/data/class_schedule.json_**.

```
Scraping course schedule from CSU website
Course schedule has been exported to "C:\Users\{currentUser}\AppData\Roaming\SmartClassPlanner\_internal\data\class_schedule.json"
```

#### Generate Class Schedule

If **print** is selected, the user will be prompted to provide their degreeworks pdf file:
```
Provide the path to the degreeworks pdf containing the courses you still require for your degree track...

Input file: ./Sample Input2.pdf
```
> [!NOTE]
> The sample above assumes the degreeworks file is located in the directory you are executing the application from.
> This may be a good practice, as will make entering the input file path simpler. This will also result in the **_./output.xlsx_** file 
> being stored in the same directory, allowing easy access after the **print** operation is complete.

> [!NOTE]
> Keep in mind that if **_class_schedule.json_** is deleted or removed from the **__internal/data_** subdirectory,
> an error will occur when attempting to execute the **print** function. The webscraper will need to be 
> executed again before attempting to print a schedule. 

After executing **print**, the resulting schedule (**_output.xlsx_**) should be available in the same directory the
program was executed from.

```
Writing recommended class schedule to "./output.xlsx"...
Recommended class schedule was successfully written to "./output.xlsx".
The application can now be terminated or run again to generate another class schedule.
```

#### View Prerequisite Violations

If prerequisite issues are found in the generated class schedule, they will be printed to the console.

```
WARNING! Prerequisite violations found in recommended schedule!
******** 'MATH 5125U' should be taken before courses: ['CPSC 2108']
Prerequisite violations will be written to "./output.xlsx" under the "Prerequisite Violation Warnings" section.
```

Once a schedule is generated, these prereq vilations can be viewed under the mentioned "Prerequisite Violation Warnings" section
in the resulting output file.

![image](https://github.com/cesmith1/CPSC6177-Project-Team2/assets/144077890/5a940762-2340-43f6-96ad-e9acc6b33321)

### Running the Application as a Python Script

> [!WARNING]
> This application was designed to be built and executed as an executable.
> For the best experience, it is recommended to follow the **Installation** section above to set up the 
> SmartClassPlanner as an executable. Only use this option for debugging or testing. 
> You will still need to run ```pip install -r requirements.txt``` to install all dependencies before 
> running the application. See the **Requirements** and **Resources** sections below.

To start the class scheduler application, the **_run.py_** script in the root directory should be executed.

```
> cd CPSC6177-Project-Team2
> python run.py
Hello, and welcome to the Smart Class Planner.
...
```

## Requirements

- An personal computer or vritual machine with an OS capable of running Python 3
- A Windows 10 or 11 operating system is required for the provided installer to function
- Build compatibility with other operating systems may vary. See **Manual Installation** section above.
- Python 3.11.5 installed and optionally added to the system PATH for easy execution
- Git installed on your local machine to do your commits and pushes from local

## Resources
- [Python 3.11.5](https://www.python.org/downloads/release/python-3115/)
- [Git CLI](https://git-scm.com/downloads) (feel free to install a GUI as well if you need/want it)
- [Advanced Installer](https://www.advancedinstaller.com/) - Used to create installer for the binary
