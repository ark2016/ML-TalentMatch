import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from transformers import pipeline
import json

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

def extract_text_from_docx(path_to_file):
    with open(path_to_file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        texts = [item['content'] for item in data]
        #print(texts[0])
        return texts
    return 'error'



pipe = pipeline("question-answering", model="Kiet/autotrain-resume_parser-1159242747")



tokenizer = AutoTokenizer.from_pretrained("Kiet/autotrain-resume_parser-1159242747")
model = AutoModelForQuestionAnswering.from_pretrained("Kiet/autotrain-resume_parser-1159242747")

text = extract_text_from_docx("resume_texts_without_lowercase.json")

pipe( "What is my name?", text[0])