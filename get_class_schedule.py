import requests
from bs4 import BeautifulSoup as bs
import unicodedata
import json

URL = "https://catalog.columbusstate.edu/academic-units/business/computer-science/computer-science-bs-software-systems-track/#programmaptextcontainer"
page = requests.get(URL)
print(page.status_code)

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
                course_code = unicodedata.normalize('NFKD', tr.td.text)
                course_name = unicodedata.normalize('NFKD', tr.td.find_next_sibling('td').text)

                if 'or ' in course_code:
                   course_code = course_code.replace('or ', ' or ')

                year = tr.find_previous_sibling(class_='plangridyear').text
                term = tr.find_previous_sibling(class_='plangridterm').th.text
                schedule[year][term].append({"courseCode": course_code, "courseName": course_name})

print(schedule)

json_object = json.dumps(schedule, indent=4)
with open("class_schedule.json", 'w') as scheduleFile:
    scheduleFile.write(json_object)

