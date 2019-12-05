"""
Description: Using the WilI-2018 dataset this file generates a ".xls" files with
the text fetched from the Wikipedia websites along with the language of the text.
Languages considered for the project:
        1. English
        2. Bengali
        3. Tamil
        4. Telugu
        5. Hindi
        6. German
        7. French
        8. Polish
        9. Russian
        10. Turkish
Authors: Diptanu Sarkar, ds9297@rit.edu, Saral Nyathawada, sn5409@rit.edu

Dependencies:
        1. Python libraries
        2. Download and unzipped dataset.
         https://zenodo.org/record/841984#.Xa0duC-ZNTY
"""

# Importing python3 libraries for the project
import bs4
import requests
from xlwt import Workbook
import math
import re
import csv

# GLOBAL INDEX TO ADD ROWS
INDEX = 1


def reading_labels(languages):
    """
    This method accepts a list of languages considered
    and returns a map of the languages and their respective
    wiki codes. Example: English -> EN
    :param languages: list()
    :return: dict()
    """
    separated_urls = dict()
    label_file = open("wili-2018/labels.csv", "r")
    # Skipping the first line
    next(label_file)
    words = []
    for f in label_file:
        words.append(f.split(";"))
    for lang in languages:
        for eachLine in words:
            if eachLine[1] == lang:
                separated_urls[lang] = eachLine[2]
    label_file.close()
    return separated_urls


def get_urls(language_encoded):
    """
    This method accepts wiki encoded language name and appends
    all the URLs from the WiLI-2018 dataset into a list, and
    returns it.
    :param language_encoded: String (EN)
    :return: list()
    """
    url_file = open("wili-2018/urls.txt", "r")
    urls_list = list()
    for url in url_file:
        if re.findall('//' + language_encoded, url):
            urls_list.append(url)
    url_file.close()
    return urls_list


def fetch_text_from_url(target_url):
    """
    This method accepts url as a parameter, fetches the text
    and returns it.
    :param target_url: String(url)
    :return: String(Paragraph)
    """
    response = requests.get(target_url)
    if response is not None:
        html = bs4.BeautifulSoup(response.text, 'html.parser')
        paragraphs = html.select("p")
        text_body = '\n'.join([para.text for para in paragraphs])
        return text_body
    return None


def create_excel_file(name="wiki_data.xls"):
    """
    This method creates a .XLS file and returns
    the workbook and sheet parameter.
    :param name:
    :return: Workbook, Sheet
    """
    wb = Workbook()
    sheet = wb.add_sheet('Wiki')
    sheet.write(0, 0, "Data")
    sheet.write(0, 1, "Language")
    wb.save(name)
    return wb, sheet


def write_csv_file(target_text, target_language, limit, file_writer):
    """
    This method creates a .CSV file
    :param name:
    :return: None
    """
    div_paragraph = math.ceil(len(target_text) / limit)
    if div_paragraph > 1:
        prev = 0
        threshold = limit
        while div_paragraph > 0:
            sub_text = target_text[prev: threshold]
            file_writer.writerow([str(sub_text), str(target_language)])
            prev = threshold
            threshold += limit
            div_paragraph -= 1
    else:
        file_writer.writerow([target_text, target_language])


def write_excel_file(target_text, target_language, workbook, sheet, limit):
    """
    This methods writes the data in the .XLS file.
    :param target_text: String
    :param target_language: String
    :param workbook: Workbook
    :param sheet: Sheet
    :return: None
    """
    div_paragraph = math.ceil(len(target_text) / limit)
    global INDEX
    if div_paragraph > 1:
        prev = 0
        # XLS has max character limit ~32K
        threshold = limit
        while div_paragraph > 0:
            sub_text = target_text[prev: threshold]
            sheet.write(INDEX, 0, sub_text)
            sheet.write(INDEX, 1, target_language)
            INDEX += 1
            prev = threshold
            threshold += limit
            div_paragraph -= 1
    else:
        sheet.write(INDEX, 0, target_text)
        sheet.write(INDEX, 1, target_language)
        INDEX += 1
    workbook.save('wiki_data.xls')


def preprocess_text(text):
    """
    This function takes in a string, removes all numbers,
    special characters, and combines two sentences with a
    space. The text is converted to lower case and consecutive
    spaces are converted into one space. New lines and empty
    text is ignored.
    :param text:
    :return:
    """
    punctuation = ['~', ':', "'", '+', '[', '\\', '@', '^', '{',
                   '%', '(', '-', '"', '*', '|', ',', '&', '<', '`',
                   '}', '_', '=', ']', '!', '>', ';', '?', '#',
                   '$', ')', '/']
    cleaned_text = ""
    for char in text:
        if char is '.' or char is '?' or char is '!' or char is ':':
            cleaned_text += ' '
        elif char in punctuation or char.isdigit():
            cleaned_text += ''
        else:
            cleaned_text += char
    cleaned_text = " ".join(cleaned_text.split())
    cleaned_text = cleaned_text.lower()
    if cleaned_text is "" or cleaned_text is "\n":
        return None
    return cleaned_text


def make_csv():
    """
    The main method to run the program.
    :return: None
    """
    considered_languages = ["English", "Bengali", "Tamil", "Telugu", "Hindi", "German",
                            "French", "Polish", "Russian", "Turkish"]
    with open('wiki_data.csv', 'w+') as csv_file:
        file_writer = csv.writer(csv_file, delimiter=',')
        file_writer.writerow(["Data", "Language"])
        print("MESSAGE: Data generation started.")
        languages_code_map = reading_labels(considered_languages)
        for language, encoded_name in languages_code_map.items():
            target_language = language
            target_url_list = get_urls(encoded_name)
            if target_url_list is not None:
                print(language, len(target_url_list))
                for target_url in target_url_list[:2]:
                    target_text = fetch_text_from_url(target_url)
                    target_text = preprocess_text(target_text)
                    if target_text is not None and len(target_text) != 0:
                        write_csv_file(target_text, target_language, 10000, file_writer)
    csv_file.close()


def main():
    """
    The main method to run the program.
    :return: None
    """
    try:
        characters_limit = 10000
        considered_languages = ["English", "Bengali", "Tamil", "Telugu", "Hindi", "German",
                                "French", "Polish", "Russian", "Turkish"]
        wb, sheet = create_excel_file()
        print("MESSAGE: Data generation started.")
        languages_code_map = reading_labels(considered_languages)
        for language, encoded_name in languages_code_map.items():
            target_language = language
            target_url_list = get_urls(encoded_name)
            if target_url_list is not None:
                # Debug Message
                print(language, len(target_url_list), INDEX)
                for target_url in target_url_list:
                    target_text = fetch_text_from_url(target_url)
                    target_text = preprocess_text(target_text)
                    if target_text is not None and len(target_text) != 0:
                        write_excel_file(target_text, target_language, wb, sheet, characters_limit)
    except Exception as e:
        print("ERROR: An exception occurred: " + str(e))
    finally:
        print("MESSAGE: The data is successfully loaded into 'wiki_data.xls' file.")


# The following condition checks whether we are
# running as a script, in which case run the code.
# If the file is being imported, don't run the code.
if __name__ == '__main__':
    main()
