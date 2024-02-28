import nltk
import numpy
import json
import pyresparser


# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')


def extract_text_from_docx(path_to_file):
    with open(path_to_file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        texts = [item['content'] for item in data]
        #print(texts[0])
        return texts
    return 'error'


def extract_names(txt):
    person_names = []
    for resume_text in txt:
        #print(resume_text)
        for sent in nltk.sent_tokenize('_ ' + resume_text):
            for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
                if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                    person_names.append(
                        ' '.join(chunk_leave[0] for chunk_leave in chunk.leaves())
                    )

    return person_names


if __name__ == '__main__':
    text = extract_text_from_docx('resume_texts_without_lowercase.json')
    names = extract_names(text)

    if names:
        print(names)  # noqa: T001
    else:
        print("NOTHING")