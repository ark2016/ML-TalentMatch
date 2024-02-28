import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from docx import Document
import pdfplumber
import json


countWordEducation = 0
countWordExperience = 0
countWordSkill = 0
countFiles = 0

def docx_to_text(file_path):
    global countFiles
    global countWordEducation
    global countWordExperience
    global countWordSkill
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
        if "education" in text or "образование" in text:
            countWordEducation += 1
        if "experience" in text or "опыт работы" in text:
            countWordExperience += 1
        countWordSkill += 1 if "skill" in text or "навыки" in text else 0

        countFiles += 1

        work_with_text(text)
        return text
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None


def get_resume_texts(folder_path):
    resume_texts = []

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        text = docx_to_text(file_path)
        if text:
            temp = dict()
            temp["content"] = text
            resume_texts.append(temp)

    return resume_texts


def generate_wordcloud(texts):
    all_text = ' '.join(texts)
    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          stopwords=None,
                          min_font_size=10).generate(all_text)

    # Отображение облака слов
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.show()

def work_with_text(text):
    if "akhundov damat" in text:
        print(text)


if __name__ == "__main__":
    folder_path = "resume"
    resume_texts = get_resume_texts(folder_path)
    if resume_texts:
        print(resume_texts)
        #generate_wordcloud(resume_texts)
        print("Кол-во файло: \n", countFiles)
        print("Кол-во слов education встреченных хотя бы раз в файле: \n", countWordEducation)
        print("Кол-во слов experience встреченных хотя бы раз в файле: \n", countWordExperience)
        print("Кол-во слов skill встреченных хотя бы раз в файле: \n", countWordSkill)

        with open('resume_texts_without_lowercase.json', 'w', encoding='utf-8') as json_file:
            json.dump(resume_texts, json_file, ensure_ascii=False, indent=4)
            print("JSON файл успешно сохранен.")
    else:
        print("Не удалось сконвертировать файлы.")
