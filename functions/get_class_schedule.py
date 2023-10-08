import requests
from bs4 import BeautifulSoup as bs
import unicodedata
import json
import os

URL = "https://catalog.columbusstate.edu/academic-units/business/computer-science/computer-science-bs-software-systems-track/#programmaptextcontainer"
page = requests.get(URL)

schedule = {}

if page.status_code == 200:
    soup = bs(page.content, "html.parser")

    table = soup.css.iselect('#programmaptextcontainer tr')

    for tr in table:
        
        if len(tr['class']) == 1:
            rowClass = tr['class'][0]
            if rowClass == 'plangridyear':
                schedule[tr.text] = {}
            elif rowClass == 'plangridterm':
                year = tr.find_previous_sibling(class_='plangridyear').text
                schedule[year][tr.th.text] = []
            else:
                course_code = unicodedata.normalize('NFKD', tr.td.text).upper()
                course_name = unicodedata.normalize('NFKD', tr.td.find_next_sibling('td').text)
                course_credit = unicodedata.normalize('NFKD', tr.td.find_next_sibling(class_='hourscol').text)

                if 'or ' in course_code:
                   course_code = course_code.split('or ')
                   course_name = course_name.split('or ')

                year = tr.find_previous_sibling(class_='plangridyear').text
                term = tr.find_previous_sibling(class_='plangridterm').th.text
                schedule[year][term].append({"courseCode": course_code, "courseName": course_name, "courseCredit": course_credit})

else:
    print("Error loading class-schedule web page...")

# print(schedule)

# Web Scrape area-courses
def get_area_courses(url, container_id):

    page = requests.get(url)
    results = {}

    if page.status_code == 200:
        soup = bs(page.content, "html.parser")

        table = soup.css.iselect(f'{container_id} tbody tr')

        area = ""
        subarea = ""
        for tr in table:
            
            if len(tr['class']) > 1 and 'areaheader' in tr['class'][1]:
                if 'Area' in tr.text:
                    results[tr.text] = {}
                    area = tr.text
                            
            elif tr.td.css.match('[colspan="2"]') and 'Total' not in tr.td.text:
            
                if 'following' in tr.td.text or 'each' in tr.td.text:
                    results[area][tr.td.text] = []
                    subarea = tr.td.text

            elif tr.td.css.match('.codecol'):
                for sibling in tr.previous_siblings:
                    if 'following' in sibling.text or 'each' in sibling.text:
                        course_code = unicodedata.normalize('NFKD', tr.td.text)
                        course_name = unicodedata.normalize('NFKD', tr.td.find_next_sibling('td').text)
                        results[area][subarea].append(
                            {
                                "courseCode": course_code,
                                "courseName": course_name
                            },
                        )
                        break

                    elif 'Area' in sibling.text:
                        break   
    else:
        print("Error loading area-courses web page...")

    return results


area_req_url = 'https://catalog.columbusstate.edu/academic-units/business/computer-science/computer-science-bs-software-systems-track/#programofstudytextcontainer'
container_id = area_req_url[area_req_url.index("#") :]

results = get_area_courses(area_req_url, container_id)
area_courses = {}

# clean up / rearrange area-courses web results 
for area, contents in results.items():
    area_text = area[0:6].upper()    # e.g., AREA A
    content_keys = list(contents.keys())

    if len(content_keys) == 1:
        area_courses[area_text] = contents[content_keys[0]]
    elif len(content_keys) > 1:
        for key in content_keys:
            if key[2] == ":":
                area_courses[f'{area_text} {key[0:3].capitalize()}'] = contents[key]
            elif 'following' in key:
                after_following_idx = key.index('following') + len('following') + 1
                area_courses[f'{area_text} {key[after_following_idx:].capitalize()}'] = contents[key]
                
# replace area-courses in schedule
for year, semesters in schedule.items():

    for semester, courses in semesters.items():
        
        for course in courses:
            code = course['courseCode']
            name = course['courseName']

            if "OR " in code:
                course['courseCode'] = [i for i in course['courseCode'].split("OR ")]
                course['courseName'] = [i for i in course['courseName'].split("or ")]
                continue

            if code == "AREA B1":

                course['courseCode'] = [i for i in course['courseName'].split(" or ")]
                course['courseName'] = [i for i in course['courseName'].split(" or ")]
                
                course['courseCode'] =[ i[0 : i.find(' ', i.find(' ')+1)] for i in course['courseCode'] ]
                continue

            if code == "AREA B2":
                course['courseCode'] = [i['courseCode'] for i in area_courses['AREA B B2:']]
                course['courseName'] = [i['courseName'] for i in area_courses['AREA B B2:']]
                continue

            if code == "AREA D":
                course['courseCode'] = [i["courseCode"] for i in area_courses['AREA D D1:'] if "no lab" not in i["courseName"]]
                course['courseName'] = [i["courseName"] for i in area_courses['AREA D D1:'] if "no lab" not in i["courseName"]]
                
                course['courseCode'] = [ i[0:i.index('&')] + " " + i[i.index('&'):] if '&' in i else i for i in course['courseCode']]
                continue

            if isinstance(code, str) and code.startswith("AREA") and "I" not in code:
                for area, courses in area_courses.items():
                    if len(area.split(" ")) > 2:
                        if not code[-1].isnumeric() and code in area: 
                            if area.split(" ")[2] in name:
                                course['courseCode'] = [i["courseCode"] for i in courses]
                                course['courseName'] = [i["courseName"] for i in courses]
                    else: # area A, F, G, H
                        if area in code:
                            course['courseCode'] = [i["courseCode"] for i in courses]
                            course['courseName'] = [i["courseName"] for i in courses]


# print(schedule)

formatted_schedule = {
    "First Year": {"Fall": [], "Spring": []},
    "Second Year": {"Fall": [], "Spring": []},
    "Third Year": {"Fall": [], "Spring": []},
    "Fourth Year": {"Fall": [], "Spring": []},
}

for year, semesters in formatted_schedule.items():

    for s, l in semesters.items():

        for course in schedule[year][s]:
            if type(course['courseCode']) is not list:
                
                l.append(
                    {
                        "courses": [
                            {
                                "code": course['courseCode'],
                                "name": course['courseName']
                            }
                        ],
                        "courseCredit": course['courseCredit']
                    }
                )
            else:
                l.append(
                        {
                            "courses": [ {"code": c, "name": course['courseName'][i]} for i, c in enumerate(course['courseCode']) ],
                            "courseCredit": course['courseCredit']
                        }
                    )  

# print(formatted_schedule)

json_object = json.dumps(formatted_schedule, indent=4)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open("../data/class_schedule.json", 'w') as scheduleFile:
    scheduleFile.write(json_object)

