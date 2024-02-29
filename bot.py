import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message


from zavod_bot.config import TOKEN

bot = Bot(TOKEN)



class working_status(StatesGroup):
    parser_works = State()
    parser_not_works = State()


dp = Dispatcher(storage=MemoryStorage())

async def parse_pdf(file_path):
    # Находим путь к PDF
    import os

    import PyPDF2
    import pdfplumber as pdfplumber
    from pdfminer.high_level import extract_pages
    from pdfminer.layout import LTTextContainer, LTChar

    def text_extraction(element):
        # Извлекаем текст из вложенного текстового элемента
        line_text = element.get_text()

        # Находим форматы текста
        # Инициализируем список со всеми форматами, встречающимися в строке текста
        line_formats = []
        for text_line in element:
            if isinstance(text_line, LTTextContainer):
                # Итеративно обходим каждый символ в строке текста
                for character in text_line:
                    if isinstance(character, LTChar):
                        # Добавляем к символу название шрифта
                        line_formats.append(character.fontname)
                        # Добавляем к символу размер шрифта
                        line_formats.append(character.size)
        # Находим уникальные размеры и названия шрифтов в строке
        format_per_line = list(set(line_formats))

        # Возвращаем кортеж с текстом в каждой строке вместе с его форматом
        return (line_text, format_per_line)

    pdf_path = file_path

    # создаём объект файла PDF
    pdfFileObj = open(pdf_path, 'rb')
    # создаём объект считывателя PDF
    pdfReaded = PyPDF2.PdfReader(pdfFileObj)

    # Создаём словарь для извлечения текста из каждого изображения
    text_per_page = {}
    # Извлекаем страницы из PDF
    for pagenum, page in enumerate(extract_pages(pdf_path)):

        # Инициализируем переменные, необходимые для извлечения текста со страницы
        pageObj = pdfReaded.pages[pagenum]
        page_text = []
        line_format = []
        text_from_images = []
        text_from_tables = []
        page_content = []
        # Инициализируем количество исследованных таблиц
        table_num = 0
        first_element = True
        table_extraction_flag = False
        # Открываем файл pdf
        pdf = pdfplumber.open(pdf_path)
        # Находим исследуемую страницу
        page_tables = pdf.pages[pagenum]
        # Находим количество таблиц на странице
        tables = page_tables.find_tables()

        # Находим все элементы
        page_elements = [(element.y1, element) for element in page._objs]
        # Сортируем все элементы по порядку нахождения на странице
        page_elements.sort(key=lambda a: a[0], reverse=True)

        # Находим элементы, составляющие страницу
        for i, component in enumerate(page_elements):
            # Извлекаем положение верхнего края элемента в PDF
            pos = component[0]
            # Извлекаем элемент структуры страницы
            element = component[1]

            # Проверяем, является ли элемент текстовым
            if isinstance(element, LTTextContainer):
                # Проверяем, находится ли текст в таблице
                if table_extraction_flag == False:
                    # Используем функцию извлечения текста и формата для каждого текстового элемента
                    (line_text, format_per_line) = text_extraction(element)
                    # Добавляем текст каждой строки к тексту страницы
                    page_text.append(line_text)
                    # Добавляем формат каждой строки, содержащей текст
                    line_format.append(format_per_line)
                    page_content.append(line_text)
                else:
                    # Пропускаем текст, находящийся в таблице
                    pass

        # Создаём ключ для словаря
        dctkey = 'Page_' + str(pagenum)
        # Добавляем список списков как значение ключа страницы
        text_per_page[dctkey] = [page_text, line_format, text_from_images, text_from_tables, page_content]

    # Закрываем объект файла pdf
    pdfFileObj.close()

    # Удаляем содержимое страницы
    result = ''.join(text_per_page['Page_0'][4])

    return result

async def some_long_operation():
    await asyncio.sleep(10)
    result = """
    {'resume': {'resume_id': 'Lead  Developer Jun 2021 - Present \n Impact Admissions',
  'first_name': 'AHMAT',
  'last_name': 'SULEIMENOV',
  'middle_name': '',
  'birth_date': 'May 2024',
  'birth_date_year_only': False,
  'country': 'New  York  University  Abu  Dhabi',
  'city': 'New  York  University  Abu  Dhabi',
  'about': '\n Lead  Developer Jun 2021 - Present \n Impact Admissions',
  'key_skills': 'Python, C++, C, Dart, JavaScript, HTML/CSS',
  'salary_expectations_amount': '',
  'salary_expectations_currency': '',
  'photo_path': '',
  'gender': '',
  'language': 'en',
  'resume_name': '',
  'source_link': '',
  'contactItems': {'resume_contact_item_id': '',
   'value': '+971 50 000 9004 ⬦',
   'comment': '',
   'contact_type': ''},
  'educationItems': [{'resume_education_item_id': '',
    'year': '',
    'organization': 'New  York  University  Abu  Dhabi',
    'faculty': 'New York University Abu Dhabi Abu Dhabi, UAE',
    'specialty': 'B.S. of Computer Science and Mathematics',
    'result': 'New  York  University  Abu  Dhabi',
    'education_type': 'New  York  University  Abu  Dhabi',
    'education_level': 'New  York  University  Abu  Dhabi'}],
  'experienceItems': [{'resume_experience_item_id': '',
    'starts': 'New  York  University  Abu  Dhabi Expected May 2024',
    'ends': 'Software Engineering School Aug 2019 - Aug 2020',
    'employer': 'New  York  University  Abu  Dhabi',
    'city': 'New  York  University  Abu  Dhabi',
    'url': '',
    'position': 'Lead  Developer',
    'description': '',
    'order': ''}],
  'languageItems': [{'resume_language_item_id': '',
    'language': '',
    'language_level': ''}]
}
}
    """
    return result

async def long_task(message: types.Message, state: FSMContext):
    # Длительная операция
    result = await some_long_operation()
    await message.answer(result)

    await state.set_state(working_status.parser_not_works)


async def parse_resume(message: types.Message, state: FSMContext):
    await long_task(message, state)
    await message.answer("Я начал решать задачу")

# only private
@dp.message(Command("start"), StateFilter(None))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(working_status.parser_not_works)
    await message.answer(f"Hello, {message.from_user.full_name}!")



@dp.message(working_status.parser_not_works,F.document)
async def parse_resume(message: types.Message, state: FSMContext):
    await message.answer("Я начал решать задачу")
    await state.set_state(working_status.parser_works)
    await long_task(message, state)




async def echo_doc(message: Message):
    document = message.document

    await bot.download(document, destination=document.file_name)

    text = parse_pdf(document.file_name)
    await message.answer(await text)


@dp.message(working_status.parser_works)
async def echo_handler(message: types.Message, state: FSMContext) -> None:
    await message.answer("Сейчас идет обработка вашего резюме, ожидайте")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())



