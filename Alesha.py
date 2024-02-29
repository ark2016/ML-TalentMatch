import fitz

def extract_meaningful_blocks(pdf_path):
    combined_text = []
    doc = fitz.open(pdf_path)
    for page in doc:
        text_blocks = page.get_text_blocks()
        page_width = page.rect.width
        left_blocks = []
        right_blocks = []
        for block in text_blocks:
            #print(block)
            (x0, y0, x1, y1, _) = block[:5]
            if (x1 + x0) / 2 < page_width / 2:
                left_blocks.append(block)
            else:
                right_blocks.append(block)
        left_blocks.sort(key=lambda b: b[1])
        right_blocks.sort(key=lambda b: b[1])
        left_text = " ".join([block[4] for block in left_blocks])
        right_text = " ".join([block[4] for block in right_blocks])
        combined_text.append(left_text + " " + right_text)
    return "\n".join(combined_text)



def process_text(text, keyWord, keywords):
    lines = text.split("\n")
    found_education = False
    result = ""
    for line in lines:
        if found_education:
            if any(keyword in line for keyword in keywords):
                break
            result += line + "\n"
        #print("!!!!", line)
        if keyWord in line: ##дофиксить
            found_education = True
    return result.strip()



path = "C:/Users/edelk/Gitflic/GitHub/ML-TalentMatch/resume/Akhundov Damat.pdf"
keywords = ["Languages", "skills"]
text = extract_meaningful_blocks(path)

#print(text)
text2 = """ParsingTechniques:XML,JSON
WebServices: REST, SOAPц
 Education
 Computer Science Engineering
 New York University of
Technology
Aug 2013 - Nov 2017
 with aggregate of 6.3%
 Higher Secondary Education
 The Texas Modal School
Jun 2011 - May 2013
 with an aggregate of 78%
 Languages
 English"
"""
section = process_text(text,"education",keywords)
print(section)


