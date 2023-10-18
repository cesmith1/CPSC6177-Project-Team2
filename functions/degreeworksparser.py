import random
import re

from pdfminer.high_level import extract_text
from py_pdf_parser.loaders import load_file

filepath = ("../data/Sample Input2.pdf")


def parseDegreeworksFile(filepath):
    document = load_file(filepath)
    still_needed_elements = document.elements.filter_by_text_contains("Still Needed:")

    for el in still_needed_elements:
        try:
            elements = str(document.elements.to_the_right_of(el).extract_single_element().text())
            #print(elements)
            # Clean Parse Text
            elements = elements.replace(" Classes ", ",")
            elements = elements.replace(" Class ", ",")
            elements = elements.replace("in", "")
            elements = elements.replace("Credits", ",")
            elements = elements.replace("Credit", ",")
            elements = elements.replace("See CORE BLOCK section", '')
            elements = elements.replace("See Area F: Computer Science - Systems section", '')
            elements = elements.replace("See Major", '')
            elements = elements.replace("Computer Science - Systems section", '')
            elements = elements.replace("Choose from", 'Choose ')
            elements = elements.replace(" of the followg:", '')
            elements = elements.replace("  ", " ")
            elements = elements.replace("  ", " ")
            elements = elements.replace(" ,", ",")
            elements = elements.replace(" or", ", or")
            elements = elements.replace(" and", ", and")

            #Convert parsed text into lists
            def convert(string):
                alist = list(string.split('\n'))
                blist = [re.sub("@", "XXX", alist) for alist in alist]

                #Choose List Regex
                clist = [re.findall(r'\((.*?)\)', blist) for blist in blist]
                clist = str(clist)
                clist = clist.replace('[', '')
                clist = clist.replace(']', '')
                clist = clist.replace("' ", "'")
                clist = clist.replace(" '", "'")

                #Rest of List Regex
                dlist = [re.sub(r'\([^)]*\)','', blist) for blist in blist]
                dlist = str(dlist)
                dlist = dlist.replace(', or', ',')
                dlist = dlist.replace("','", '')
                dlist = dlist.replace("'Choose 1'", "")
                dlist = dlist.replace("'Choose 2'", "")
                dlist = dlist.replace('[', '')
                dlist = dlist.replace(']', '')
                dlist = dlist.replace("' ", "'")
                dlist = dlist.replace(" '", "'")
                dlist = dlist.replace("''", '')
                dlist = dlist.replace("5128U*", "CPSC 5128U*")
                dlist = dlist.replace("5135U*", "CPSC 5135U*")
                dlist = dlist.replace("5155U*", "CPSC 5155U*")
                dlist = dlist.replace("5157U*", "CPSC 5157U*")
                dlist = dlist.replace("MATH 3XXX, 4XXX, 5XXXU", "MATH 3XXX, MATH 4XXX, MATH 5XXXU")
                dlist = dlist.replace("CPSC 3XXX, 4XXX, 5XXX", "CPSC 3XXX, CPSC 4XXX, CPSC 5XXX")
                dlist = dlist.replace("CYBR 3XXX, 4XXX, 5XXX", "CYBR 3XXX, CYBR 4XXX, CYBR 5XXX")

                #Find Choose 1 or Choose 2
                choose = [re.findall(r'Choose (\d+)', blist) for blist in blist]
                choose = str(choose)
                choose = choose.replace('[', '')
                choose = choose.replace(']', '')
                choose = choose.replace("' ", "'")
                choose = choose.replace(" '", "'")

                this_list = choose + clist + dlist
                return this_list
            print(convert(elements))
        except:
            print("An Exception Occurred")


print(parseDegreeworksFile(filepath))
