import csv
import json
import os
import re

from unidecode import unidecode
from shutil import rmtree


CSV_PATH = './files/csv'
JSON_PATH = './files/json'



def normalize_str(original_str: str):
    """
    The function `normalize_str` takes an input string, converts it to lowercase, replaces spaces,
    commas, periods, and hyphens with underscores, and removes certain special characters.
    
    :param original_str: The `normalize_str` function takes a string `original_str` as input and
    normalizes it by replacing spaces, hyphens, commas, and periods with underscores. It also removes
    any leading or trailing whitespace and converts the string to lowercase
    :type original_str: str
    :return: The `normalize_str` function takes an input string `original_str`, normalizes it by
    replacing spaces, commas, periods, and hyphens with underscores, and removes any unwanted characters
    like special symbols or parentheses. The normalized string is then returned.
    """
    pattern_1 = re.compile(r' - |, |\s|\.')
    pattern_2 = re.compile(r'\n|\ufeff|\(|\)')

    return unidecode(
        pattern_1.sub(
            '_', pattern_2.sub(
                '', original_str.strip().lower()
            )
        )
    )


def recreate_folders():
    """
    The function `recreate_folders` deletes and recreates a directory specified by the variable
    `JSON_PATH`.
    """
    rmtree(JSON_PATH)
    os.makedirs(JSON_PATH, exist_ok=True)


def open_csv_file(path):
    """
    The function `open_csv_file` opens a CSV file located at the specified path and returns a
    `csv.DictReader` object for reading the file.
    
    :param path: The `path` parameter in the `open_csv_file` function is a string that represents the
    file path to the CSV file that you want to open and read
    :return: A `csv.DictReader` object is being returned.
    """
    # with open(path, encoding="utf-8") as file:
    file = open(path, mode="r", encoding="utf-8")
    csv_reader = csv.DictReader(file)
    return file, csv_reader


def open_json_file(path):
    """
    The function `open_json_file` reads and loads a JSON file located at the specified path.
    
    :param path: The `path` parameter in the `open_json_file` function is a string that represents the
    file path to the JSON file that you want to open and read
    :return: The function `open_json_file` is returning the contents of a JSON file located at the
    specified `path`.
    """
    with open(path, mode="r", encoding="utf-8") as file:
        return json.load(file)
    

def saves_json_file(path, data) -> None:
    """
    The function `saves_json_file` saves data to a JSON file with specified path and encoding.
    
    :param path: The `path` parameter in the `saves_json_file` function is the file path where the JSON
    data will be saved. This should be a string representing the location and name of the file where you
    want to save the JSON data
    :param data: The `data` parameter in the `saves_json_file` function is the data that you want to
    write to a JSON file. This data can be in the form of a dictionary, list, or any other
    JSON-serializable object that you want to save to a file in JSON format
    """
    with open(path, mode="w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def array_diff(a: list, b: list) -> list:
    """
    The function `array_diff` takes two lists `a` and `b` as input and returns a new list containing
    elements from `a` that are not present in `b`.
    
    :param a: The parameter `a` in the `array_diff` function is a list of elements from which we want to
    remove elements that are also present in another list `b`
    :type a: list
    :param b: The parameter `b` in the `array_diff` function is a list that contains elements to be
    removed from list `a`. The function will return a new list that contains only the elements from list
    `a` that are not present in list `b`
    :type b: list
    :return: This function `array_diff` takes two lists `a` and `b` as input and returns a new list
    containing elements from list `a` that are not present in list `b`.
    """
    return [x for x in a if x not in b]


def array_object_diff(a: list[dict], b: list[dict], key: str) -> list:
    """
    The function `array_object_diff` takes two lists of dictionaries and a key, and returns a list of
    dictionaries from the first list that have a key value not present in the second list.
    
    :param a: The parameter `a` is a list of dictionaries
    :type a: list[dict]
    :param b: b is a list of dictionaries
    :type b: list[dict]
    :param key: The `key` parameter in the `array_object_diff` function is a string that represents the
    key in the dictionaries within the input lists `a` and `b` that will be used to compare the objects
    for differences
    :type key: str
    :return: The function `array_object_diff` returns a list of dictionaries from list `a` that have a
    value for the specified key that is not present in any dictionary in list `b`.
    """
    b_key_values = {item[key] for item in b}
    return [x for x in a if x[key] not in b_key_values]