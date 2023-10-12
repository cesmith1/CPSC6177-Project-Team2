import re
from pdfminer.high_level import extract_text

def parseDegreeworksFile():
    text = extract_text("../data/Sample Input3.pdf")
    # print(text)

    # basic matches
    pattern = re.compile(r"[A-Z]{4} \d{4}[A-Z]?")
    matches = pattern.findall(text)
    # print(matches)

    # or matches
    pattern2 = re.compile(r"[A-Z]{4} \d{4}[A-Z]?[?:*]?[?: or]+\d{4}?")
    matches2 = pattern2.findall(text)
    new_matches20 = [re.sub(" or", ", XXXX", matches2) for matches2 in matches2]
    new_matches2 = [re.split("  ", new_matches20) for new_matches20 in new_matches20]
    new_matches21 = str(new_matches2)
    new_matches21 = new_matches21.replace("[", "")
    new_matches21 = new_matches21.replace("]", "")
    new_matches21 = new_matches21.replace("*", "")
    new_matches21 = new_matches21.replace("'", "")
    new_matches211 = new_matches21.strip('][').split(', ')
    # print(new_matches211)

    # and matches
    pattern3 = re.compile(r"[A-Z]{4} \d{4}[A-Z]?[?:*]?[?: and]+\d{4}?")
    matches3 = pattern3.findall(text)
    new_matches30 = [re.sub(" and", ", XXXX", matches3) for matches3 in matches3]
    new_matches3 = [re.split("  ", new_matches30) for new_matches30 in new_matches30]
    new_matches31 = str(new_matches3)
    new_matches31 = new_matches31.replace("[", "")
    new_matches31 = new_matches31.replace("]", "")
    new_matches31 = new_matches31.replace("*", "")
    new_matches31 = new_matches31.replace("'", "")
    new_matches311 = new_matches31.strip('][').split(', ')
    # print(new_matches311)

    # @ matches
    pattern4 = re.compile(r"[A-Z]{4} \d+[?:@]?[?: or]+\d[?:@]?[?: or]+\d[?:@]?")
    matches4 = pattern4.findall(text)
    new_matches4 = [re.sub("@", "XXX", matches4) for matches4 in matches4]
    new_matches41 = [re.sub(" or", ", XXXX", new_matches4) for new_matches4 in new_matches4]
    new_matches42 = [re.split("  ", new_matches41) for new_matches41 in new_matches41]
    new_matches411 = str(new_matches42)
    new_matches411 = new_matches411.replace("[", "")
    new_matches411 = new_matches411.replace("]", "")
    new_matches411 = new_matches411.replace("'", "")
    new_matches4111 = new_matches411.strip('][').split(', ')
    # print(new_matches4111)

    # @ and whitespace matches
    pattern5 = re.compile(r"[A-Z]{4} \s\d+[?:@]?[?: or]+\d[?:@]?[?: or]+\d[?:@]?[A-Z]?")
    matches5 = pattern5.findall(text)
    new_matches55 = [re.sub("@", "XXX", matches5) for matches5 in matches5]
    new_matches5 = [re.sub("  ", " ", new_matches55) for new_matches55 in new_matches55]
    new_matches51 = [re.sub(" or", ", XXXX", new_matches5) for new_matches5 in new_matches5]
    new_matches52 = [re.split("  ", new_matches51) for new_matches51 in new_matches51]
    new_matches511 = str(new_matches52)
    new_matches511 = new_matches511.replace("[", "")
    new_matches511 = new_matches511.replace("]", "")
    new_matches511 = new_matches511.replace("'", "")
    new_matches5111 = new_matches511.strip('][').split(', ')
    # print(new_matches5111)

    # whitespace matches
    pattern6 = re.compile(r"[A-Z]{4} \s\d{4}[A-Z]?")
    matches6 = pattern6.findall(text)
    new_matches6 = [re.sub("  ", " ", matches6) for matches6 in matches6]
    # print(new_matches6)

    print("List of All Possible Classes Still Needed")
    list = new_matches211 + new_matches311 + new_matches4111 + new_matches5111 + matches + new_matches6

    beautiful_list = []
    [beautiful_list.append(item) for item in list if item not in beautiful_list]
    beautiful_list = str(beautiful_list)
    beautiful_list = beautiful_list.replace("'',", "")
    beautiful_list = beautiful_list.replace(", ''", "")
    return beautiful_list

print(parseDegreeworksFile())

