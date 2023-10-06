import re
from pdfminer.high_level import extract_text


text = extract_text("Sample Input1.pdf")
print(text)

pattern = re.compile(r"[A-Z]{4} \d{4}[A-Z]?([A-Za-z\s\-]+)")
matches = pattern.findall(text)
print(matches)
