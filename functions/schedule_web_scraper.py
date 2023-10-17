from pathlib import Path
import requests
from bs4 import BeautifulSoup as bs
import unicodedata
import json

ROOT_DIR = Path(__file__).parent.parent

class ScheduleWebScraper:

    def __init__(self) -> None:
        self.class_schedule_json_path = ROOT_DIR / 'data/class_schedule.json'
        self.program_schedule_url = "https://catalog.columbusstate.edu/academic-units/business/computer-science/computer-science-bs-software-systems-track/#programmaptextcontainer"
        self.area_courses_url = 'https://catalog.columbusstate.edu/academic-units/business/computer-science/computer-science-bs-software-systems-track/#programofstudytextcontainer'
        self.program_schedule_container_id = self.program_schedule_url[self.program_schedule_url.index("#") :]
        self.area_courses_container_id = self.area_courses_url[self.area_courses_url.index("#") :]
        self.schedule = self.fetch_program_schedule()
        self.area_courses = self.fetch_area_courses()
        self.formatted_schedule = self.get_formatted_schedule()

    def get_request_page_content(self, url):
        page = requests.get(url)
        return bs(page.content, "html.parser") if page.status_code == 200 else "Error loading page"

    def fetch_program_schedule(self):
        results = {}
        soup_content = self.get_request_page_content(self.program_schedule_url)
        if soup_content != "Error loading page":
            selector = f"{self.program_schedule_container_id} tr"
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
                        results[year][term].append({"courseCode": course_code, "courseName": course_name, "courseCredit": course_credit})
        return results

    def fetch_area_courses(self):
        results = {}
        soup_content = self.get_request_page_content(self.area_courses_url)
        if soup_content != "Error loading page":
            selector = f"{self.area_courses_container_id} tbody tr"
            table = soup_content.css.iselect(selector)
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
                                {"courseCode": course_code, "courseName": course_name},
                            )
                            break
                        elif 'Area' in sibling.text: break
        return results

    # clean up / rearrange area-courses web results 
    def reformat_area_courses(self):
        results = {}
        for area, contents in self.area_courses.items():
            area_text = area[0:6].upper()    # e.g., AREA A
            content_keys = list(contents.keys())

            if len(content_keys) == 1:
                results[area_text] = contents[content_keys[0]]
            elif len(content_keys) > 1:
                for key in content_keys:
                    if key[2] == ":":
                        results[f'{area_text} {key[0:3].capitalize()}'] = contents[key]
                    elif 'following' in key:
                        after_following_idx = key.index('following') + len('following') + 1
                        results[f'{area_text} {key[after_following_idx:].capitalize()}'] = contents[key]
        return results
    
    # replace area-courses in schedule
    def replace_schedule_area_section(self):
        formatted_area_courses = self.reformat_area_courses()
        for year, semesters in self.schedule.items():
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
                        course['courseCode'] = [i['courseCode'] for i in formatted_area_courses['AREA B B2:']]
                        course['courseName'] = [i['courseName'] for i in formatted_area_courses['AREA B B2:']]
                        continue

                    if code == "AREA D":
                        course['courseCode'] = [i["courseCode"] for i in formatted_area_courses['AREA D D1:'] if "no lab" not in i["courseName"]]
                        course['courseName'] = [i["courseName"] for i in formatted_area_courses['AREA D D1:'] if "no lab" not in i["courseName"]]
                        
                        course['courseCode'] = [ i[0:i.index('&')] + " " + i[i.index('&'):] if '&' in i else i for i in course['courseCode']]
                        continue

                    if code == "AREA H":
                        course['courseCode'] = ['CPSC 3XXX', 'CYBR 3XXX']
                        course['courseName'] = ['CPSC 3000 level or above', 'CYBR 3000 level or above']
                        continue

                    if isinstance(code, str) and code.startswith("AREA") and "I" not in code:
                        for area, courses in formatted_area_courses.items():
                            if len(area.split(" ")) > 2:
                                if not code[-1].isnumeric() and code in area: 
                                    if area.split(" ")[2] in name:
                                        course['courseCode'] = [i["courseCode"] for i in courses]
                                        course['courseName'] = [i["courseName"] for i in courses]
                            else: # area A, F, G, H
                                if area in code:
                                    course['courseCode'] = [i["courseCode"] for i in courses]
                                    course['courseName'] = [i["courseName"] for i in courses]

    # final formatted class schedule for usage
    def get_formatted_schedule(self):
        if not self.can_fetch_data():
            return {"error": "failed fetching web page contents"}
        
        self.replace_schedule_area_section()
        # print(self.schedule)
        formatted_schedule = { "First Year": {"Fall": [], "Spring": []},
                                "Second Year": {"Fall": [], "Spring": []},
                                "Third Year": {"Fall": [], "Spring": []},
                                "Fourth Year": {"Fall": [], "Spring": []} }

        for year, semesters in formatted_schedule.items():
            for s, l in semesters.items():
                for course in self.schedule[year][s]:
                    if type(course['courseCode']) is not list:
                        l.append({
                                    "courses": [
                                        {"code": course['courseCode'], "name": course['courseName']}
                                    ],
                                    "courseCredit": course['courseCredit']
                                })
                    else:
                        l.append({
                                    "courses": [ {"code": c, "name": course['courseName'][i]} for i, c in enumerate(course['courseCode']) ],
                                    "courseCredit": course['courseCredit']
                                })  
        json_str = json.dumps(formatted_schedule, indent=4) 
        with open(self.class_schedule_json_path, 'w') as scheduleFile:
            scheduleFile.write(json_str)

        return formatted_schedule
           
    def can_fetch_data(self):
        return True if (self.schedule and self.area_courses) else False


# web_scraper = ScheduleWebScraper()
# web_scraper.get_formatted_schedule()   # get formatted class schedule dictionary

# print(web_scraper.class_schedule_json_path)   # get path to class schedule json file
# print(web_scraper.formatted_schedule)         # get formatted class schedule dictionary
