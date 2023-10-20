import json
import os
import re
import random
import sys
from urllib.parse import urlparse
import pandas as pd
from bs4 import Tag, BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import tkinter as tk
import tkinter.font as tkfont
import datetime
from tkinter import ttk, messagebox, filedialog


# Функция отправки формы запроса(передачи данных в программу)
def submit_form():
    keyword = entry.get()
    checkbox1_state = checkbox1_var.get()
    checkbox2_state = checkbox2_var.get()
    checkbox3_state = checkbox3_var.get()
    checkbox4_state = checkbox4_var.get()
    checkbox5_state = checkbox5_var.get()
    checkbox6_state = checkbox6_var.get()
    checkbox7_state = checkbox7_var.get()
    checkbox8_state = checkbox8_var.get()
    checkbox9_state = checkbox9_var.get()
    checkbox10_state = checkbox10_var.get()
    checkbox11_state = checkbox11_var.get()
    checkbox12_state = checkbox12_var.get()
    checkbox13_state = checkbox13_var.get()
    checkbox14_state = checkbox14_var.get()
    checkbox15_state = checkbox15_var.get()
    checkbox16_state = checkbox16_var.get()
    combo_state = combo.get()
    combo2_state = combo2.get()
    combo3_state = combo3.get()
    combo4_state = combo4.get()
    combo5_state = combo5.get()

    if len(keyword) >= 2:
        entry.config(bg="white")
        error_label.config(text="")
        print("Форма отправлена!")
    else:
        error_label.config(text="Введите 2 и более символа", fg="red")  # Отображение сообщения об ошибке
        entry.config(bg='red')
        return

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    # options.add_argument("--headless")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Функция указания папки с ChromeDriver
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(__file__)
        return os.path.join(base_path, relative_path)

    driver = webdriver.Chrome(service=Service(resource_path('./driver/chromedriver.exe')), options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    # Очистка/создание JSON-файла
    empty_data = {}
    with open('data.json', 'w') as file:
        json.dump(empty_data, file)

    # Функция отправки сообщения о завершении работы программы
    def open_message_box():
        messagebox.showinfo("Завершение программы", "Программа завершена!")

    # Функция сбора ссылок на публикации
    def get_urls() -> list:
        urls = []
        url_pattern = "https://elibrary.ru/item.asp?id="
        block = driver.find_element(By.ID, "restab")
        pubs = block.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
        for pub in pubs:
            try:
                id = pub.get_attribute("id")
                id = ''.join([i for i in id if i.isdigit()])
                urls.append(url_pattern + id)
            except Exception as err:
                continue
        del urls[0]
        return urls

    # Основная функция программы. Сбор данных со страницы публикации
    def parser(i):
        title = driver.find_element(By.CLASS_NAME, "bigtext").text

        content = driver.page_source
        soup = BeautifulSoup(content, 'lxml')
        owner = ""
        p_ind = ""
        tr = soup.body.table.tbody.tr.td.table.tbody.tr
        td = ""
        for t in tr.children:
            if isinstance(t, Tag):
                td = t
        tbody = td.table.tbody
        for t in tbody.children:
            if isinstance(t, Tag):
                tr = t
        td = tr.td

        id, edn = td.table.tbody.tr.find_all('a')[:2]
        id, edn = id.text, edn.text

        t = 0
        table = ""
        div = ""
        for tag in td.contents:
            if isinstance(tag, Tag):
                t += 1
                if t == 2:
                    table = tag
                elif t == 3:
                    div = tag

        try:
            p_ind = div.tbody.tr.find('span', class_='help1 pointer')
            owner = div.tbody.tr.find('span', class_='help pointer')
            if p_ind is None:
                pass
            else:
                p_ind = p_ind.text + str(p_ind.next_sibling)
                p_ind = p_ind.replace("<br/>", "")
                p_ind = p_ind.replace("\n\xE2\x96\xBCПоказать полностью", "")
            if owner is None:
                owner = ''.join([i.text for i in div.table.tbody.tr.find_all('div')])
                owner = owner.replace("\u00A0", " ")
            else:
                owner = owner.text
                owner = owner.replace("\u00A0", " ")
                owner = re.sub(r'\d', '', owner)
        except Exception as err:
            print(err, 71)

        p_data = driver.find_elements(By.XPATH,
                                      "/html/body/table/tbody/tr/td/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td[1]/div/table")
        datas = ""
        for data in p_data:
            temp = data.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
            for d in temp:
                datas += d.text
        type_r = re.search(r"Тип:\s*(.*?)(?=[А-Я]|$)", datas)
        type_p = type_r.group(1).strip() if type_r else None

        lang_r = re.search(r"Язык:\s*(.*?)(?=[А-Я]|$)", datas)
        lang_p = lang_r.group(1).strip() if lang_r else None

        year_r = re.search(r"(?:Год(?:\sиздания)?:|Год публикации:)\s*(\d{4})(?=[А-Я]|$)", datas)
        year_p = year_r.group(1).strip() if year_r else None

        page_r = re.search(r"Страницы:\s*(.*?)(?=[А-Я]|$)", datas)
        page_p = page_r.group(1).strip() if page_r else None

        p_data = driver.find_elements(By.XPATH,
                                      "/html/body/table/tbody/tr/td/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td[1]/div/table")
        ann_tr = ""
        kw_tr = ""
        for an in p_data:
            ann_title = an.find_element(By.TAG_NAME, "tbody").find_element(By.TAG_NAME, "tr").find_element(By.TAG_NAME,
                                                                                                           "td").text
            if ann_title == "АННОТАЦИЯ:":
                ann_tr = an.text
            if ann_title == "КЛЮЧЕВЫЕ СЛОВА:":
                kw_tr = an.text
        ann_p = ann_tr[ann_tr.find("АННОТАЦИЯ: \n  ") + len("АННОТАЦИЯ: \n  "):]
        ann_p = ann_p.replace("<br/>", "")
        ann_p = ann_p.replace("\n▼Показать полностью", "")
        kw_p = kw_tr[ann_tr.find("КЛЮЧЕВЫЕ СЛОВА: \n  ") + len("КЛЮЧЕВЫЕ СЛОВА: \n  "):]
        kw_p = [keyw.strip() for keyw in kw_p.split(",")]

        data_dict = {
            "ID": id,
            "EDN": edn,
            "Type": type_p,
            "Title": title,
            "Author": owner,
            "Data": p_ind,
            "Lang": lang_p,
            "Year": year_p,
            "Pages": page_p,
            "Keywords": kw_p,
            "Annotation": ann_p
        }

        data_dict = {k: v for k, v in data_dict.items() if v not in ("", None, "Null", [""])}

        data = json.load(open('data.json', 'r', encoding='UTF-8'))
        data[i] = data_dict

        # Запись в файл
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    url = "https://elibrary.ru/querybox.asp?scope=newquery"
    driver.get(url)
    time.sleep(3)
    curr = driver.current_url
    if ("https://elibrary.ru/page_captcha.asp" in curr) and (curr != url):
        time.sleep(90)

    # Передача данных из программы на форму поиска сайта eLIBRARY
    driver.find_element(By.NAME, "where_name").click()
    driver.find_element(By.NAME, "where_abstract").click()
    driver.find_element(By.NAME, "where_keywords").click()

    if checkbox6_state:
        driver.find_element(By.NAME, "where_fulltext").click()  # on
        driver.find_element(By.NAME, "where_name").click()
        driver.find_element(By.NAME, "where_abstract").click()
        driver.find_element(By.NAME, "where_keywords").click()
        driver.find_element(By.NAME, "where_affiliation").click()
        driver.find_element(By.NAME, "where_references").click()

    if checkbox1_state:
        driver.find_element(By.NAME, "where_name").click()

    if checkbox2_state:
        driver.find_element(By.NAME, "where_abstract").click()

    if checkbox3_state:
        driver.find_element(By.NAME, "where_keywords").click()

    if checkbox4_state:
        driver.find_element(By.NAME, "where_affiliation").click()

    if checkbox5_state:
        driver.find_element(By.NAME, "where_references").click()

    if not checkbox7_state:
        driver.find_element(By.NAME, "type_article").click()

    if not checkbox8_state:
        driver.find_element(By.NAME, "type_book").click()

    if not checkbox9_state:
        driver.find_element(By.NAME, "type_conf").click()

    if not checkbox10_state:
        driver.find_element(By.NAME, "type_preprint").click()

    if not checkbox11_state:
        driver.find_element(By.NAME, "type_disser").click()

    if not checkbox12_state:
        driver.find_element(By.NAME, "type_report").click()

    if not checkbox13_state:
        driver.find_element(By.NAME, "type_patent").click()

    if not checkbox14_state:
        driver.find_element(By.NAME, "search_morph").click()

    if checkbox15_state:
        driver.find_element(By.NAME, "search_freetext").click()

    if checkbox16_state:
        driver.find_element(By.NAME, "search_fulltext").click()

    key = keyword
    driver.find_element(By.CLASS_NAME, "inputr").send_keys(key)

    year_f = combo_state
    year_t = combo2_state
    ddf = Select(driver.find_element(By.NAME, "begin_year"))
    ddf.select_by_visible_text(year_f)
    ddt = Select(driver.find_element(By.NAME, "end_year"))
    ddt.select_by_visible_text(year_t)

    pst = combo3_state
    ddp = Select(driver.find_element(By.NAME, "issues"))
    ddp.select_by_visible_text(pst)
    sort_p = combo4_state
    dds = Select(driver.find_element(By.NAME, "orderby"))
    dds.select_by_visible_text(sort_p)
    order_p = combo5_state
    ddo = Select(driver.find_element(By.NAME, "order"))
    ddo.select_by_visible_text(order_p)

    driver.find_element(By.LINK_TEXT, "Поиск").click()
    time.sleep(5)

    # Сбор ссылок на публикации
    urls = []
    urls.extend(get_urls())
    curr = driver.current_url
    if ("https://elibrary.ru/page_captcha.asp" in curr) and (curr != url):
        time.sleep(90)
    try:
        end = driver.find_element(By.LINK_TEXT, "В конец")
        end.click()
        url = driver.current_url
        parsed_url = urlparse(url)
        query_string = parsed_url.query
        page_number = None
        for param in query_string.split('&'):
            param_name, param_value = param.split('=')
            if param_name == 'pagenum':
                page_number = int(param_value)
        if page_number >= 100:
            page_number = 99

        url = "https://www.elibrary.ru/query_results.asp"
        driver.get(url)
        for i in range(2, page_number + 1):
            driver.get(url + f'?pagenum={i}')
            curr = driver.current_url
            if ("https://elibrary.ru/page_captcha.asp" in curr) and (curr != url):
                time.sleep(90)
            urls.extend(get_urls())
    except Exception as err:
        pass

    print(f'Найдено {len(urls)} ссылок для обработки')

    # Сбор данных из публикаций из списка
    for i, url in enumerate(urls, 1):
        driver.get(url)
        curr = driver.current_url
        if ("https://elibrary.ru/page_captcha.asp" in curr) and (curr != url):
            time.sleep(90)
        print(f'Сейчас обрабатывается {i} публикация по адресу: {url}')
        if i % 7 == 0:
            second = random.randrange(5, 15)
            time.sleep(second)
        parser(i)

    open_message_box()
    driver.quit()


# Функции конвертации JSON-файла в .BibTex
def generate_bibtex_key(author, year, title):
    author_lastname = author.split()[0]
    first_word = title.split()[0]
    bibtex_key = f'{author_lastname}{year}{first_word}'

    return bibtex_key


def json_to_bibtex(json_file_path, bibtex_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    bibtex_entries = []

    for item_id, item in data.items():
        bibtex_type = 'article'
        bibtex_key = generate_bibtex_key(item.get('Author', ''), item.get('Year', ''), item.get('Title', ''))

        bibtex_entry = f'@{bibtex_type}{{{bibtex_key},\n'
        bibtex_entry += f'    title = {{{item.get("Title", "")}}},\n'
        if "Author" in item:
            bibtex_entry += f'    author = {{{item["Author"]}}},\n'
        if "Year" in item:
            bibtex_entry += f'    year = {{{item["Year"]}}},\n'
        if "Pages" in item:
            bibtex_entry += f'    pages = {{{item["Pages"]}}},\n'
        if "Data" in item:
            bibtex_entry += f'    institution = {{{item["Data"]}}},\n'
        if "Annotation" in item:
            bibtex_entry += f'    note = {{{item["Annotation"]}}},\n'

        keywords = item.get('Keywords', [])
        keyword_string = ', '.join(keywords)

        if keyword_string:
            bibtex_entry += f'    keywords = {{{keyword_string}}},\n'

        bibtex_entry += '}\n'

        bibtex_entries.append(bibtex_entry)

    bibtex_string = "\n".join(bibtex_entries)

    with open(bibtex_file_path, 'w', encoding='utf-8') as bibtex_file:
        bibtex_file.write(bibtex_string)

    print(f'BibTeX file "{bibtex_file_path}" created successfully.')


def convert_json_to_bibtex():
    json_file_path = filedialog.askopenfilename(filetypes=[('JSON Files', '*.json')])
    bibtex_file_path = filedialog.asksaveasfilename(defaultextension='.bib', filetypes=[('Bibtex Files', '*.bib')])
    if bibtex_file_path:
        json_to_bibtex(json_file_path, bibtex_file_path)


# Функции конвертации JSON-файла в .ris
def json_to_ris(json_file_path, ris_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    ris_entries = []

    for item in data.values():
        ris_entry = ""

        if "Type" in item:
            ris_entry += "TY  - " + item["Type"] + "\n"

        if "Author" in item:
            ris_entry += "AU  - " + item["Author"] + "\n"

        if "Title" in item:
            ris_entry += "TI  - " + item["Title"] + "\n"

        if "Year" in item:
            ris_entry += "PY  - " + item["Year"] + "\n"

        if "Pages" in item:
            pages = item["Pages"]
            if "-" in pages:
                ris_entry += "SP  - " + pages.split("-")[0] + "\n"
                ris_entry += "EP  - " + pages.split("-")[1] + "\n"
            else:
                ris_entry += "SP  - " + pages + "\n"

        if "Data" in item:
            ris_entry += "PB  - " + item["Data"] + "\n"

        if "Annotation" in item:
            ris_entry += "N2  - " + item["Annotation"] + "\n"

        if "Keywords" in item:
            keywords = item["Keywords"]
            for keyword in keywords:
                ris_entry += "KW  - " + keyword + "\n"

        ris_entries.append(ris_entry)

    ris_string = "\n".join(ris_entries)

    with open(ris_file_path, 'w', encoding='utf-8') as ris_file:
        ris_file.write(ris_string)

    print(f'RIS file "{ris_file_path}" created successfully.')


def convert_json_to_ris():
    json_file_path = filedialog.askopenfilename(filetypes=[('JSON Files', '*.json')])
    ris_file_path = filedialog.asksaveasfilename(defaultextension='.ris', filetypes=[('RIS Files', '*.ris')])
    if ris_file_path:
        json_to_ris(json_file_path, ris_file_path)


# Функции конвертации JSON-файла в .enw
def json_to_enw(json_file_path, enw_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    enw_entries = []

    for item in data.values():
        enw_entry = ''

        if "Type" in item:
            enw_entry += f'%0 {item["Type"]}\n'

        if "Author" in item:
            enw_entry += f'%A {item["Author"]}\n'

        if "Title" in item:
            enw_entry += f'%T {item["Title"]}\n'

        if "Year" in item:
            enw_entry += f'%D {item["Year"]}\n'

        if "Pages" in item:
            enw_entry += f'%P {item["Pages"]}\n'

        if "Data" in item:
            enw_entry += f'%I {item["Data"]}\n'

        if "Annotation" in item:
            enw_entry += f'%N {item["Annotation"]}\n'

        if "Keywords" in item:
            keywords = item["Keywords"]
            for keyword in keywords:
                enw_entry += f'%K {keyword}\n'

        enw_entries.append(enw_entry)

    enw_string = "\n".join(enw_entries)

    with open(enw_file_path, 'w', encoding='utf-8') as enw_file:
        enw_file.write(enw_string)

    print(f'ENW file "{enw_file_path}" created successfully.')


def convert_json_to_enw():
    json_file_path = filedialog.askopenfilename(filetypes=[('JSON Files', '*.json')])
    enw_file_path = filedialog.asksaveasfilename(defaultextension='.enw', filetypes=[('ENW Files', '*.enw')])
    if enw_file_path:
        json_to_enw(json_file_path, enw_file_path)


# Функции конвертации JSON-файла в .xlsx
def json_to_excel(json_file_path, excel_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    rows = []
    columns = ['ID', 'EDN', 'Type', 'Title', 'Author', 'Data', 'Lang', 'Year', 'Pages', 'Keywords', 'Annotation']

    for item_id, item in data.items():
        row = [
            item.get('ID', ''),
            item.get('EDN', ''),
            item.get('Type', ''),
            item.get('Title', ''),
            item.get('Author', ''),
            item.get('Data', ''),
            item.get('Lang', ''),
            item.get('Year', ''),
            item.get('Pages', ''),
            ', '.join(item.get('Keywords', [])),
            item.get('Annotation', '')
        ]
        rows.append(row)

    df = pd.DataFrame(rows, columns=columns)

    df.to_excel(excel_file_path, index=False)

    print(f'Excel file "{excel_file_path}" created successfully.')


def convert_json_to_excel():
    json_file_path = filedialog.askopenfilename(filetypes=[('JSON Files', '*.json')])
    excel_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[('Excel Files', '*.xlsx')])
    if excel_file_path:
        json_to_excel(json_file_path, excel_file_path)


# Функция обработки кнопки "enter" в форме
def on_enter_pressed(event):
    submit_button.invoke()


# Функция для работы кнопки "в полном тексте публикации" в форме запроса
def update_checkboxes():
    if checkbox1_var.get():
        checkbox1_var.set(True)
        checkbox2_var.set(True)
        checkbox3_var.set(True)
        checkbox4_var.set(True)
        checkbox5_var.set(True)


# Функция для очистки формы запроса
def clear():
    entry.delete(0, tk.END)

    checkbox1_var.set(True)
    checkbox2_var.set(True)
    checkbox3_var.set(True)
    checkbox4_var.set(False)
    checkbox5_var.set(False)
    checkbox6_var.set(False)
    checkbox7_var.set(True)
    checkbox8_var.set(True)
    checkbox9_var.set(True)
    checkbox10_var.set(True)
    checkbox11_var.set(True)
    checkbox12_var.set(True)
    checkbox13_var.set(True)
    checkbox14_var.set(True)
    checkbox15_var.set(False)
    checkbox16_var.set(False)
    combo.set(years[0])
    combo2.set(years[0])
    combo3.set(values[0])
    combo4.set(sort[0])
    combo5.set(order[0])


# Интерфейс программы
window = tk.Tk()

# Заголовок окна
window.title("Сборщик данных из eLIBRARY")
window.resizable(width=False, height=False)

# шрифт
custom_font = tkfont.Font(family="Century Gothic", size=12)
custom_fontB = tkfont.Font(family="Century Gothic", size=12, weight="bold")

# Основной фрейм
frame0 = tk.Frame(window, borderwidth=2, relief=tk.RAISED)
frame0.pack(padx=10, pady=10)

# блок "Что искать"
frame = tk.Frame(frame0, borderwidth=2, relief=tk.RAISED)
frame.pack(padx=10, pady=5, anchor="w", fill="x", expand=True)

label = tk.Label(frame, text="Что искать:", font=custom_font, width=20)
label.pack(side='left')

entry = tk.Entry(frame)
entry.pack(fill="x", expand=True, padx=3)

error_label = tk.Label(frame, fg="red")
error_label.pack()

# блок "Где искать"
frame2 = tk.Frame(frame0, borderwidth=2, relief=tk.RAISED)
frame2.pack(padx=10, pady=5, anchor="w", fill="x", expand=True)

label2 = tk.Label(frame2, text="Где искать:", font=custom_font, width=20)
label2.pack(side='left')

checkbox1_var = tk.BooleanVar()
checkbox1_var.set(True)
checkbox1 = tk.Checkbutton(frame2, text="в названии публикации", variable=checkbox1_var, font=custom_font)
checkbox1.pack(anchor="w")

checkbox2_var = tk.BooleanVar()
checkbox2_var.set(True)
checkbox2 = tk.Checkbutton(frame2, text="в аннотации", variable=checkbox2_var, font=custom_font)
checkbox2.pack(anchor="w")

checkbox3_var = tk.BooleanVar()
checkbox3_var.set(True)
checkbox3 = tk.Checkbutton(frame2, text="в ключевых словах", variable=checkbox3_var, font=custom_font)
checkbox3.pack(anchor="w")

checkbox4_var = tk.BooleanVar()
checkbox4 = tk.Checkbutton(frame2, text="в названии организаций авторов", variable=checkbox4_var, font=custom_font)
checkbox4.pack(anchor="w")

checkbox5_var = tk.BooleanVar()
checkbox5 = tk.Checkbutton(frame2, text="в списках цитируемой литературы", variable=checkbox5_var, font=custom_font)
checkbox5.pack(anchor="w")

checkbox6_var = tk.BooleanVar()
checkbox6 = tk.Checkbutton(frame2, text="в полном тексте публикации", variable=checkbox6_var, command=update_checkboxes,
                           font=custom_font)
checkbox6.pack(anchor="w")

# блок "Тип публикации"
frame3 = tk.Frame(frame0, borderwidth=2, relief=tk.RAISED)
frame3.pack(padx=10, pady=5, anchor="w", fill="x", expand=True)

label3 = tk.Label(frame3, text="Тип публикации:", font=custom_font, width=20)
label3.pack(side='left')

checkbox7_var = tk.BooleanVar()
checkbox7_var.set(True)
checkbox7 = tk.Checkbutton(frame3, text="статьи в журналах", variable=checkbox7_var, font=custom_font)
checkbox7.pack(anchor="w")

checkbox8_var = tk.BooleanVar()
checkbox8_var.set(True)
checkbox8 = tk.Checkbutton(frame3, text="книги", variable=checkbox8_var, font=custom_font)
checkbox8.pack(anchor="w")

checkbox9_var = tk.BooleanVar()
checkbox9_var.set(True)
checkbox9 = tk.Checkbutton(frame3, text="материалы конференций", variable=checkbox9_var, font=custom_font)
checkbox9.pack(anchor="w")

checkbox10_var = tk.BooleanVar()
checkbox10_var.set(True)
checkbox10 = tk.Checkbutton(frame3, text="депонированные рукописи", variable=checkbox10_var, font=custom_font)
checkbox10.pack(anchor="w")

checkbox11_var = tk.BooleanVar()
checkbox11_var.set(True)
checkbox11 = tk.Checkbutton(frame3, text="диссертации", variable=checkbox11_var, font=custom_font)
checkbox11.pack(anchor="w")

checkbox12_var = tk.BooleanVar()
checkbox12_var.set(True)
checkbox12 = tk.Checkbutton(frame3, text="отчеты", variable=checkbox12_var, font=custom_font)
checkbox12.pack(anchor="w")

checkbox13_var = tk.BooleanVar()
checkbox13_var.set(True)
checkbox13 = tk.Checkbutton(frame3, text="патенты", variable=checkbox13_var, font=custom_font)
checkbox13.pack(anchor="w")

# блок "параметры"
frame4 = tk.Frame(frame0, borderwidth=2, relief=tk.RAISED)
frame4.pack(padx=10, pady=5, anchor="w", fill="x", expand=True)

label4 = tk.Label(frame4, text="Параметры:", font=custom_font, width=20)
label4.pack(side='left')

checkbox14_var = tk.BooleanVar()
checkbox14_var.set(True)
checkbox14 = tk.Checkbutton(frame4, text="искать с учетом морфологии", variable=checkbox14_var, font=custom_font)
checkbox14.pack(anchor="w")

checkbox15_var = tk.BooleanVar()
checkbox15 = tk.Checkbutton(frame4, text="искать похожий текст", variable=checkbox15_var, font=custom_font)
checkbox15.pack(anchor="w")

checkbox16_var = tk.BooleanVar()
checkbox16 = tk.Checkbutton(frame4, text="искать в публикациях, имеющих полный текст на eLIBRARY.ru",
                            variable=checkbox16_var, font=custom_font)
checkbox16.pack(anchor="w")

# блок "Годы и поступившие"
frame5 = tk.Frame(frame0, borderwidth=2, relief=tk.RAISED)
frame5.pack(padx=10, pady=5, anchor="w", fill="x", expand=True)

label5 = tk.Label(frame5, text="Годы публикации:", font=custom_font, width=20)
label5.pack(side='left')

current_year = datetime.date.today().year
years = [''] + [str(year) for year in range(2024, 1899, -1)]

combo = ttk.Combobox(frame5, values=years, width=8, state="readonly")
combo.pack(side='left')
combo.current(0)

label5 = tk.Label(frame5, text=" - ", font=custom_font)
label5.pack(side='left')

combo2 = ttk.Combobox(frame5, values=years, width=8, state="readonly")
combo2.pack(side='left')
combo2.current(0)

label6 = tk.Label(frame5, text="Поступившие:", font=custom_font, width=20)
label6.pack(side='left')

values = ["за все время", "за последний месяц", "за последние 3 месяца", "за последние полгода", "за последний год"]
combo3 = ttk.Combobox(frame5, values=values, width=21, state="readonly")
combo3.pack(side='left')
combo3.current(0)

# блок "сортировка и порядок"
frame6 = tk.Frame(frame0, borderwidth=2, relief=tk.RAISED)
frame6.pack(padx=10, pady=5, anchor="w", fill="x", expand=True)

label7 = tk.Label(frame6, text="Сортировка:", font=custom_font, width=20)
label7.pack(side='left')

sort = ["по релевантности", "по дате выпуска", "по дате добавления", "по названию статьи", "по названию журнала",
        "по числу цитирований"]
combo4 = ttk.Combobox(frame6, values=sort, width=21, state="readonly")
combo4.pack(side='left')
combo4.current(0)

label8 = tk.Label(frame6, text="Порядок:", font=custom_font, width=20)
label8.pack(side='left')

order = ["по убыванию", "по возрастанию"]
combo5 = ttk.Combobox(frame6, values=order, width=20, state="readonly")
combo5.pack(side='left')
combo5.current(0)

# блок "Кнопки"
frame7 = tk.Frame(frame0, borderwidth=2, relief=tk.RAISED)
frame7.pack(padx=10, pady=5, anchor="w", fill="x", expand=True)
# Кнопка очистки формы
clear_button = tk.Button(frame7, text="Очистить", command=clear, bg="gray", fg="white", font=custom_fontB, width=10,
                         height=1)
clear_button.pack(padx=10, pady=2, side="left")
# Кнопка отправки формы
submit_button = tk.Button(frame7, text="Поиск", command=submit_form, bg="red", fg="white", font=custom_fontB, width=10,
                          height=1)
submit_button.pack(padx=10, pady=2, side="right")

# блок "Продолжить"
frame8 = tk.Frame(frame0, borderwidth=2, relief=tk.RAISED)
frame8.pack(padx=10, pady=5, anchor="w", fill="x", expand=True)

b_bib = tk.Button(frame8, text="to Bibtex", command=convert_json_to_bibtex, width=10, height=1)
b_bib.pack(padx=50, pady=2, side="left")
b_ris = tk.Button(frame8, text="to RIS", command=convert_json_to_ris, width=10, height=1)
b_ris.pack(padx=50, pady=2, side="left")
b_enw = tk.Button(frame8, text="to ENW", command=convert_json_to_enw, width=10, height=1)
b_enw.pack(padx=50, pady=2, side="left")
b_xlsx = tk.Button(frame8, text="to Excel", command=convert_json_to_excel, width=10, height=1)
b_xlsx.pack(padx=50, pady=2, side="left")

entry.bind('<Return>', on_enter_pressed)

window.mainloop()