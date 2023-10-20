import xlsxwriter

class OutputClass:

    def __init__(self, code, name, semestersOffered, credits, notes):
        self.name, self.code, self.semestersOffered, self.credits, self.notes = name, code, semestersOffered, int(credits), notes

# Output writer for creating the Excel file
class OutputWriter :

    # Constructor
    # Params: name of student, student CSU ID, starting year (i.e. 2023)
    def __init__(self, name, csuId, startingYear):
        self.name = name
        self.csuId = csuId
        self.years = []
        self.startingYear = startingYear
        self.currentYeat = startingYear
        self.workbook = xlsxwriter.Workbook('./output.xlsx')

    # Method to add an additional year/semester
    # Params: year index (zero based), semester ("Fall"/"Spring"), list of OutputClass
    def addSemesterToWriter(self, yearIndex, semester, classes):
        if 0 <= yearIndex < len(self.years):
            self.years[yearIndex][semester] = classes
        else:
            self.years.insert(yearIndex, {semester : classes})

    # Execute writer. ONLY CALL THIS METHOD ONCE!
    def write(self):
        worksheet = self.workbook.add_worksheet()
        # Generic formatting
        bold_right_align = self.workbook.add_format({'bold':1,'align':'right'})
        bold =  self.workbook.add_format({'bold':1})
        bold_header =  self.workbook.add_format({'bold':1, 'valign':'bottom', 'bottom':5})

        # Title Format
        title_format = self.workbook.add_format(
            {
                "bold": 1,
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "font_size" : 36
            }
        )

        # Expand columns and rows
        worksheet.set_column('A:E', 30)
        worksheet.set_column('B:B', 7)
        worksheet.set_column('D:D', 7)
        worksheet.set_column('E:E', 15)
        worksheet.set_column('F:F', 50)
        worksheet.set_column('G:G', 7)
        worksheet.set_column('H:H', 50)
        worksheet.set_row(1, 45)

        # Add name and csu number
        worksheet.write('B1', 'Name:', bold_right_align)
        worksheet.write('C1', self.name)
        worksheet.write('D1', 'CSU ID:', bold_right_align)
        worksheet.write('E1', str(self.csuId))

        # Add headers
        worksheet.merge_range('A2:D2', "Path to Graduation", title_format)
        worksheet.write('F2', "Required Courses", bold_header)
        worksheet.write('G2', "Credits", bold_header)
        worksheet.write('H2', "Notes", bold_header)

        # Add semester borders 
        semester_border_left = self.workbook.add_format({'left':5})
        semester_border_right = self.workbook.add_format({'right':5})
        semester_border_top_right = self.workbook.add_format({'top':5, 'right':5, 'bottom':1})
        semester_border_bottom_right = self.workbook.add_format({'bottom':5, 'right':5, 'top':1})
        semester_border_top_left = self.workbook.add_format({'top':5, 'left':5, 'bottom':1})
        semester_border_bottom_left = self.workbook.add_format({'bottom':5, 'left':5, 'top':1})
        total_border_left = self.workbook.add_format({'bold':1, 'align':'right', 'bottom':5, 'left':5, 'top':5})
        total_border_right = self.workbook.add_format({'bold':1, 'align':'right' ,'bottom':5, 'right':5, 'top':5})
        
        # Store classes in upcoming loop for later
        classes = []
        # Store total hours for grand total at the end
        totalCreditHours = 0

        # Write Semester Content
        for y in range(len(self.years)):

            worksheet.conditional_format(f'A{(y*9)+3}:A{(y*9)+3}',{'type':'no_errors','format':semester_border_top_left})
            worksheet.conditional_format(f'B{(y*9)+3}:B{(y*9)+3}',{'type':'no_errors','format':semester_border_top_right})
            worksheet.conditional_format(f'A{(y*9)+4}:A{(y*9)+10}',{'type':'no_errors','format':semester_border_left})
            worksheet.conditional_format(f'B{(y*9)+4}:B{(y*9)+10}',{'type':'no_errors','format':semester_border_right})
            worksheet.conditional_format(f'A{(y*9)+11}:A{(y*9)+11}',{'type':'no_errors','format':semester_border_bottom_left})
            worksheet.conditional_format(f'B{(y*9)+11}:B{(y*9)+11}',{'type':'no_errors','format':semester_border_bottom_right})
            worksheet.conditional_format(f'C{(y*9)+3}:C{(y*9)+3}',{'type':'no_errors','format':semester_border_top_left})
            worksheet.conditional_format(f'D{(y*9)+3}:D{(y*9)+3}',{'type':'no_errors','format':semester_border_top_right})
            worksheet.conditional_format(f'C{(y*9)+4}:C{(y*9)+10}',{'type':'no_errors','format':semester_border_left})
            worksheet.conditional_format(f'D{(y*9)+4}:D{(y*9)+10}',{'type':'no_errors','format':semester_border_right})
            worksheet.conditional_format(f'C{(y*9)+11}:C{(y*9)+11}',{'type':'no_errors','format':semester_border_bottom_left})
            worksheet.conditional_format(f'D{(y*9)+11}:D{(y*9)+11}',{'type':'no_errors','format':semester_border_bottom_right})
            if 'Fall' in self.years[y]:
                worksheet.write(f'A{(y*9)+3}', f'Fall {self.startingYear+y}', bold)
                worksheet.write(f'B{(y*9)+3}', 'Credits', bold)
                worksheet.write(f'A{(y*9)+11}', 'Total', bold)
                worksheet.write(f'B{(y*9)+11}', f'=SUM(B{(y*9)+4}:B{(y*9)+10})', bold)
                index = 0
                for outputClass in self.years[y]['Fall']:
                    if index <= 7:
                        worksheet.write(f'A{(y*9)+4+index}', f'{outputClass.code} - {outputClass.name} {outputClass.semestersOffered}')
                        worksheet.write(f'B{(y*9)+4+index}', outputClass.credits)
                        totalCreditHours += outputClass.credits
                    else:
                        raise Exception("Too many classes in a semester for output writer to handle!")
                    index += 1 
                    classes.append(outputClass)
            if 'Spring' in self.years[y]:
                worksheet.write(f'C{(y*9)+3}', f'Spring {self.startingYear+y}', bold)
                worksheet.write(f'D{(y*9)+3}', 'Credits', bold)
                worksheet.write(f'C{(y*9)+11}', 'Total', bold)
                worksheet.write(f'D{(y*9)+11}', f'=SUM(D{(y*9)+4}:D{(y*9)+10})', bold)
                index = 0
                for outputClass in self.years[y]['Spring']:
                    if index <= 7:
                        worksheet.write(f'C{(y*9)+4+index}', f'{outputClass.code} - {outputClass.name} {outputClass.semestersOffered}')
                        worksheet.write(f'D{(y*9)+4+index}', outputClass.credits)
                        totalCreditHours += outputClass.credits
                    else:
                        raise Exception("Too many classes in a semester for output writer to handle!")
                    index += 1
                    classes.append(outputClass)

        # Write Total credit hours
        worksheet.write(f'C{(len(self.years)*9)+3}', 'Total Credit Hours', total_border_left)
        worksheet.write(f'D{(len(self.years)*9)+3}', totalCreditHours, total_border_right)

        # Write all required classes, credits and notes off to the right
        index = 0
        for outputClass in classes:
            worksheet.write(f'F{index+3}', f'{outputClass.code} - {outputClass.name} {outputClass.semestersOffered}')
            worksheet.write(f'G{index+3}', outputClass.credits)
            worksheet.write(f'H{index+3}', self._interpretClassNotes(outputClass.notes))
            index += 1

    # Interpret any notes from DAG
    def _interpretClassNotes(self, notes):
        interpretedNotes = []
        for note in notes:
            if note == 'last semester':
                interpretedNotes.append('Take your last semester')
            elif note == 'jr/sr':
                interpretedNotes.append('Must be junior or senior')
            else:
                interpretedNotes.append(note)

        return ', '.join(interpretedNotes)

    def close(self):
        self.workbook.close()

# TEST FOR OUTPUT WRITER
#writer = OutputWriter('Evan Smith', 909465542, 2022)
#writer.addSemesterToWriter(0, 'Fall', [OutputClass('MATH 2125', 'Intro to Discrete Math', ['Fa', 'Sp'], 3, '')])
#writer.addSemesterToWriter(0, 'Spring', [OutputClass('MATH 2125U', 'Discrete Math', ['Fa', 'Sp'], 3, '')])
#writer.addSemesterToWriter(1, 'Fall', [OutputClass('CPSC 3175', 'Object-Oriented Design', ['Fa', 'Sp'], 3, 'lul'),
#                                       OutputClass('CPSC 3165', 'Professionalism in Computing', ['Fa', 'Sp'], 3, 'Professionals have standards.')])
#writer.addSemesterToWriter(1, 'Spring', [OutputClass('CPSC 3121', 'Assembly 1', ['Sp'], 3, 'autobots...')])
#writer.addSemesterToWriter(2, 'Fall', [])
#writer.addSemesterToWriter(2, 'Spring', [])
#writer.write()
#writer.close()