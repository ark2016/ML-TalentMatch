import os
import re
import nltk
import pandas as pd
import spacy
from docx import Document
import pdfplumber
import json
from nltk.corpus import wordnet
import pymorphy2
from textblob import TextBlob
import gender_guesser

nltk.download('wordnet')


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

def file_to_text(file_path):
    try:
        text = ""
        if ".docx" in file_path:
            # Преобразование .docx файла в текст
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += " " + paragraph.text.replace("\t"," ").strip() + ' \n '
        else:
            # Преобразование .pdf файла в текст
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + ' \n '

        #text = text.lower()
        work_with_text(text)
        return text
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

def work_with_text(text):
    if "akhundov damat" in text:
        print(text)


def split_resume_into_blocks(text, keywords):
    # Получение индексов начала каждого ключевого слова
    print(text.lower())
    start_indices = []
    for keyword, synonyms in keywords.items():
        for synonym in synonyms:
            print("SYNINIUN", keyword, synonym.lower())
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


# def extract_skills(nlp_text, noun_chunks, skills_file):
#     tokens = [token.text for token in nlp_text if not token.is_stop]
#
#     data = pd.read_csv(skills_file)
#     skills = list(data.columns.values)
#     skillset = []
#     # check for one-grams
#     for token in tokens:
#         if token.lower() in skills:
#             skillset.append(token)
#
#     # check for bi-grams and tri-grams
#     for token in noun_chunks:
#         token = token.text.lower().strip()
#         if token in skills:
#             skillset.append(token)
#     return [i.capitalize() for i in set([i.lower() for i in skillset])]

def check_slills(text, skills_file):
    text = text.lower().split('\n')  # Разделяем текст по символам '\n' и получаем список строк
    text = [e.split(',') for e in text]  # Разделяем каждую строку по символу ',' и получаем список списков
    text = [sublist for sublist in text if sublist != ['']]  # Удаляем пустые списки
    text = [item for sublist in text for item in sublist]  # Объединяем все списки в один список
    text = [e.split('.') for e in text]  # Разделяем каждый элемент списка по символу '.' и получаем список списков
    text = [item for sublist in text for item in sublist]  # Объединяем все списки в один список
    text = [e.split(':') for e in text]  # Разделяем каждый элемент списка по символу '.' и получаем список списков
    text = [item for sublist in text for item in sublist]  # Объединяем все списки в один список
    text = [e.split('/') for e in text]  # Разделяем каждый элемент списка по символу '.' и получаем список списков
    text = [item for sublist in text for item in sublist]  # Объединяем все списки в один список
    text = [item.replace(' ', '') for item in text]

    str=''
    for i in text:
        str += i + ','
    print(str)
    data = pd.read_csv(skills_file)
    skills = list(data.columns.values)
    skillset = []

    print(skills)

    for e in text:
        if e.lower() in skills or e in skills:
            skillset.append(e)
    return skillset

# Список ключевых слов для блоков
keywords = {
    "summary": ["summary"],
    "education": ["education", "учеба"],
    "awards": ["awards", "achievements", "награды"],
    "experience": ["experience", "work experience", "опыт"],
    "projects": ["projects", "проекты"],
    "skills": ["skills", "навыки"],
    "activities": ["activities", "деятельность"]
}

def predict_gender(text):
    blob = TextBlob(text)
    gender_score = blob.sentiment.polarity
    if gender_score >= 0.5:
        return "Male"
    else:
        return "Female"


if __name__ == "__main__":
    # Добавление синонимов к ключевым словам
    for key, value in keywords.items():
        synonyms = []
        for word in value:
            synonyms.extend(get_synonyms(word))  # Для английских синонимов
            synonyms.extend(get_russian_synonyms(word))  # Для русских синонимов
        keywords[key] = list(set(synonyms))

    print(keywords)
    
    file_path = "resume/Alan Iusupov .pdf"
    resume_text = file_to_text(file_path)

    resume_blocks = split_resume_into_blocks(resume_text, keywords)
    for i in resume_blocks.keys():
        print("!!!!!",i, ":", resume_blocks[i])
    remaining_text = extract_remaining_text(resume_text, resume_blocks)
    print("!!!!Remaining Text: ", remaining_text)
    print(resume_blocks.keys())

    #NLP поиск скилов хуже
    #nlp = spacy.load('en_core_web_sm')
    # nlp_text_for_skills = nlp(resume_blocks['skills'])
    # key_skills = extract_skills(nlp_text_for_skills, nlp_text_for_skills.noun_chunks, "skills.csv")
    # print(key_skills)

    #Обычный поиск Нормалек
    key_skills = check_slills(resume_blocks['skills'], "skills.csv")
    #print(key_skills)
    dicta['key_skills'] = key_skills

    print(predict_gender(resume_text))



    # with open('resume_texts_without_lowercase.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(resume_texts, json_file, ensure_ascii=False, indent=4)
    #     print("JSON файл успешно сохранен.")
