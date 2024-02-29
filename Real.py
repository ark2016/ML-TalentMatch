import os

import nltk
from docx import Document
import pdfplumber
import json
from nltk.corpus import wordnet
import pymorphy2

nltk.download('wordnet')

def file_to_text(file_path):
    try:
        text = ""
        if ".docx" in file_path:
            # Преобразование .docx файла в текст
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text.replace("\t"," ").strip() + ' \n '
        else:е
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

# Список ключевых слов для блоков
keywords = {
    "education": ["education", "учеба"],
    "awards": ["awards", "награды"],
    "experience": ["experience", "опыт"],
    "projects": ["projects", "проекты"],
    "skills": ["skills", "навыки"],
    "activities": ["activities", "деятельность"]
}




if __name__ == "__main__":
    # Добавление синонимов к ключевым словам
    for key, value in keywords.items():
        synonyms = []
        for word in value:
            synonyms.extend(get_synonyms(word))  # Для английских синонимов
            synonyms.extend(get_russian_synonyms(word))  # Для русских синонимов
        keywords[key] = list(set(synonyms))

    print(keywords)
    
    file_path = "resume/AHMAT SULEIMENOV.docx"
    resume_text = file_to_text(file_path)

    resume_blocks = split_resume_into_blocks(resume_text, keywords)
    for i in resume_blocks.keys():
        print(i, ":", resume_blocks[i])
    remaining_text = extract_remaining_text(resume_text, resume_blocks)
    print("Remaining Text: ", remaining_text)
    # with open('resume_texts_without_lowercase.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(resume_texts, json_file, ensure_ascii=False, indent=4)
    #     print("JSON файл успешно сохранен.")
