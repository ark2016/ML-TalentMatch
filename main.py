import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from docx import Document
import pdfplumber
from langdetect import detect
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from transformers import pipeline
import nltk
from nltk.corpus import wordnet
import pymorphy2

PATH_TO_FILE = "resume/AHMAT SULEIMENOV.docx"

def file_to_text(file_path):
    try:
        text = ""
        if ".docx" in file_path:
            # Преобразование .docx файла в текст
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text.replace("\t"," ").strip() + ' \n '
        else:
            # Преобразование .pdf файла в текст
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + ' \n '

        #text = text.lower()
        return text
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None


def split_resume_into_blocks(text, keywords):
    # Получение индексов начала каждого ключевого слова
    start_indices = []
    for keyword, synonyms in keywords.items():
        for synonym in synonyms:
            start_index = text.lower().find(synonym.lower())
            if start_index != -1:
                start_indices.append((start_index, keyword))
                break

    # Сортировка индексов
    start_indices.sort()

    # Разделение текста на блоки по ключевым словам
    blocks = {}
    for i in range(len(start_indices)):
        start_index, block_name = start_indices[i]
        end_index = start_indices[i + 1][0] if i + 1 < len(start_indices) else len(text)
        blocks[block_name] = text[start_index:end_index].strip()

    return blocks

def extract_remaining_text(text, blocks):
    remaining_text = text
    for block_name, block_text in blocks.items():
        remaining_text = remaining_text.replace(block_text, "")
    return remaining_text.strip()

# Функция для получения синонимов с использованием nltk
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

# Функция для получения синонимов с использованием pymorphy2
def get_russian_synonyms(word):
    morph = pymorphy2.MorphAnalyzer()
    parsed_word = morph.parse(word)[0]
    return [parsed_word.normal_form] + [i.normal_form for i in parsed_word.lexeme]


def extract_contacts(file_path, json_data):
    contacts = {}
    text = file_to_text(file_path)
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    github_regex = r'(?:github\.io\s*|\s*(?:https?://)?(?:www\.)?github\.com/)(\S+)'
    phone_regex = r'(?:(?:\+1\s*-?)?(?:\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4})|(?:(?:\+7\s*-?)?(?:\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{2}[\s.-]?\d{2})|(?:(?:\+44\s*-?)?(?:\(\d{4}\)|\d{4})[\s.-]?\d{6})|(?:(?:\+33\s*-?)?(?:\(\d{1,2}\)|\d{1,2})[\s.-]?(?:\d{2}\s){4}\d{2})'
    regex_linkedin = r'(?:https?://)?(?:www\.)?linkedin\.com/\S+'

    emails = re.findall(email_regex, text)
    if emails:
        contacts['email'] = emails[0]

    phones = re.findall(phone_regex, text)
    if phones:
        contacts['phone'] = phones[0]

    github_usernames = re.findall(github_regex, text)
    if github_usernames:
        contacts['github'] = github_usernames[0]

    linkedln_links = re.findall(regex_linkedin, text)
    if linkedln_links:
        contacts['linkedin'] = linkedln_links[0]

    for key, value in contacts.items():
        contact_item = {
            "resume_contact_item_id": "",
            "value": value,
            "comment": "",
            "contact_type": key
        }
        json_data["resume"]["contactItems"].append(contact_item)

    return json.dumps(json_data, indent=4)




# Список ключевых слов для блоков
keywords = {
    "education": ["education", "учеба"],
    "awards": ["awards", "награды"],
    "experience": ["experience", "опыт"],
    "projects": ["projects", "проекты"],
    "skills": ["skills", "навыки"],
    "activities": ["activities", "деятельность"]
}




# if __name__ == "__main__":
# Добавление синонимов к ключевым словам
for key, value in keywords.items():
    synonyms = []
    for word in value:
        synonyms.extend(get_synonyms(word))  # Для английских синонимов
        synonyms.extend(get_russian_synonyms(word))  # Для русских синонимов
    keywords[key] = list(set(synonyms))

print(keywords)

# file_path = "resume/AHMAT SULEIMENOV.docx"
resume_text = file_to_text(PATH_TO_FILE)
#resume_text = text[0]

resume_blocks = split_resume_into_blocks(resume_text, keywords)
for i in resume_blocks.keys():
    print(i, ":", resume_blocks[i])
remaining_text = extract_remaining_text(resume_text, resume_blocks)
print("Remaining Text: ", remaining_text)
# with open('resume_texts_without_lowercase.json', 'w', encoding='utf-8') as json_file:
#     json.dump(resume_texts, json_file, ensure_ascii=False, indent=4)
#     print("JSON файл успешно сохранен.")
print(resume_text)
#_____________________________________________________________________________________________________________________
dicta = {
  "resume": {
      "resume_id": "",
      "first_name": "",
      "last_name": "",
      "middle_name": "",
      "birth_date": "",
      "birth_date_year_only": "",
      "country": "",
      "city": "",
      "about": "",
      "key_skills": "",
      "salary_expectations_amount": "",
      "salary_expectations_currency": "",
      "photo_path": "",
      "gender": "",
      "language": "",
      "resume_name": "",
      "source_link": "",
      "contactItems": [
        {
          "resume_contact_item_id": "",
          "value": "",
          "comment": "",
          "contact_type": ""
        }
      ],
      "educationItems": [
        {
          "resume_education_item_id": "",
          "year": "",
          "organization": "",
          "faculty": "",
          "specialty": "",
          "result": "",
          "education_type": "",
          "education_level": ""
        }
      ],
      "experienceItems": [
        {
          "resume_experience_item_id": "",
          "starts": "",
          "ends": "",
          "employer": "",
          "city": "",
          "url": "",
          "position": "",
          "description": "",
          "order": ""
        }
      ],
      "languageItems": [
        {
          "resume_language_item_id": "",
          "language": "",
          "language_level": ""
        }
      ]
    }
}


pipe = pipeline("question-answering", model="Kiet/autotrain-resume_parser-1159242747")
tokenizer = AutoTokenizer.from_pretrained("Kiet/autotrain-resume_parser-1159242747")
model = AutoModelForQuestionAnswering.from_pretrained("Kiet/autotrain-resume_parser-1159242747")

dicta['resume']["resume_id"] = pipe("resume_id", resume_text)['answer']

FullName = pipe("what is my name", resume_text)['answer']
print("Full Name: ", FullName)
names = ["first_name", "last_name", "middle_name"]
i = 0
for name in FullName.split():
    dicta['resume'][names[i]] = name
    i += 1

birth_date = pipe("birth_date", resume_text)['answer']
print("birth date: ", birth_date)
dicta['resume']["birth_date"] = birth_date

dicta['resume']["birth_date_year_only"] = (birth_date==True)

homeland = pipe("homeland", resume_text)['answer']
print("homeland: ", homeland)
dicta['resume']["country"] = homeland

hometown = pipe("hometown", resume_text)['answer']
print("hometown: ", hometown)
dicta['resume']["city"] = hometown

about = pipe("describe me", resume_text)['answer']
print("about: ", about)
dicta['resume']["about"] = about

key_skills = pipe("tell me key skills", resume_text)['answer']
print("key_skills: ", key_skills)
dicta['resume']["key_skills"] = key_skills

dicta['resume']["language"] = detect(resume_text)
print("language: ", dicta['resume']["language"])

organization = pipe("place of education", resume_text)['answer']
print("organization: ", organization)
dicta['resume']['educationItems'][0]["organization"] = organization

faculty = pipe("faculty of education", resume_text)['answer']
print("faculty: ", faculty)
dicta['resume']['educationItems'][0]["faculty"] = faculty

specialty = pipe("specialty of education", resume_text)['answer']
print("specialty: ", specialty)
dicta['resume']['educationItems'][0]["specialty"] = specialty

result = pipe("result of education", resume_text)['answer']
print("result: ", result)
dicta['resume']['educationItems'][0]["result"] = result

education_type = pipe("type of education", resume_text)['answer']
print("education_type: ", education_type)
dicta['resume']['educationItems'][0]["education_type"] = education_type

education_level = pipe("level of education", resume_text)['answer']
print("education_level: ", education_level)
dicta['resume']['educationItems'][0]["education_level"] = education_type

starts = pipe("start of work", resume_text )['answer']
print("starts: ", starts)
dicta['resume']['experienceItems'][0]["starts"] = starts

ends = pipe("end of work", resume_text )['answer']
print("ends: ", ends)
dicta['resume']['experienceItems'][0]["ends"] = ends

employer = pipe("place of work", resume_text )['answer']
print("employer: ", employer)
dicta['resume']['experienceItems'][0]["employer"] = employer

city = pipe("city of work", resume_text )['answer']
print("city: ", city)
dicta['resume']['experienceItems'][0]["city"] = city

position = pipe("position at work", resume_text )['answer']
print("position: ", position)
dicta['resume']['experienceItems'][0]["position"] = position

dicta = extract_contacts(PATH_TO_FILE, dicta)

print(dicta)

file_path = "output/res.json"

# Запись словаря в JSON файл
with open(file_path, "w") as json_file:
    json.dump(dicta, json_file, ensure_ascii=False, indent=4)
