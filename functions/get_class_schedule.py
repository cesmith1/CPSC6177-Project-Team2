"To write tests for the code provided, I needed to refactor the code into functions/classes so that it can be easily tested. I'll provide a basic structure for the tests and some example tests."

import requests
from bs4 import BeautifulSoup as bs
import unicodedata
import json

def fetch_page_content(url):
    page = requests.get(url)
    if page.status_code == 200:
        return page.content
    else:
        print("Error loading web page...")
        return None

def extract_schedule(content):
    soup = bs(content, "html.parser")
    table = soup.select('#programmaptextcontainer tr')
    schedule = {}

def get_request_page_content(url):
    page = requests.get(url)
    if page.status_code == 200:
        content = bs(page.content, "html.parser")
        return content
    else:
        error = "Error loading web page"
        print(error)
        return error

def fetch_program_schedule(container_id):
    soup_content = get_request_page_content(program_schedule_url)
    if soup_content == "Error loading web page":
        return soup_content + " - program schedule"
    
    results = {}
    selector = f"{container_id} tr"
    table = soup_content.css.iselect(selector)
    for tr in table:
        if len(tr['class']) == 1:
            rowClass = tr['class'][0]
            if rowClass == 'plangridyear':
                results[tr.text] = {}
            elif rowClass == 'plangridterm':
                year = tr.find_previous_sibling(class_='plangridyear').text
                results[year][tr.th.text] = []
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

    return schedule

def get_area_courses(url, container_id):
    content = fetch_page_content(url)
    if not content:
        return {}

    soup = bs(content, "html.parser")
    table = soup.select(f'{container_id} tbody tr')
    results = {}
    area = ""
    subarea = ""

    for tr in table:
        if len(tr['class']) > 1 and 'areaheader' in tr['class'][1]:
            if 'Area' in tr.text:
                results[tr.text] = {}
                area = tr.text
        elif tr.td.has_attr('colspan') and tr.td['colspan'] == "2" and 'Total' not in tr.td.text:
            if 'following' in tr.td.text or 'each' in tr.td.text:
                results[area][tr.td.text] = []
                subarea = tr.td.text
        elif tr.td.has_attr('class') and 'codecol' in tr.td['class']:
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

    return results


def format_schedule(schedule):
    formatted = {
        "First Year": {"Fall": [], "Spring": []},
        "Second Year": {"Fall": [], "Spring": []},
        "Third Year": {"Fall": [], "Spring": []},
        "Fourth Year": {"Fall": [], "Spring": []},
    }

    for year, semesters in formatted.items():
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
                            "courses": [{"code": c, "name": course['courseName'][i]} for i, c in enumerate(course['courseCode'])],
                            "courseCredit": course['courseCredit']
                        }
                    )
    print(formatted)
    return formatted


def save_schedule_to_json(schedule, filename):
    json_object = json.dumps(schedule, indent=4)
    with open(filename, 'w') as scheduleFile:
        scheduleFile.write(json_object)

if __name__ == "__main__":
    URL = "https://catalog.columbusstate.edu/academic-units/business/computer-science/computer-science-bs-software-systems-track/#programmaptextcontainer"
    content = fetch_page_content(URL)

    if content:
        schedule = extract_schedule(content)
        area_req_url = 'https://catalog.columbusstate.edu/academic-units/business/computer-science/computer-science-bs-software-systems-track/#programofstudytextcontainer'
        container_id = area_req_url[area_req_url.index("#") :]
        area_courses = get_area_courses(area_req_url, container_id)
        formatted_schedule = format_schedule(schedule)
        save_schedule_to_json(formatted_schedule, "../data/class_schedule.json")
