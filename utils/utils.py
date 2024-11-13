import csv
import json
import os
import re
import time

from unidecode import unidecode
from shutil import rmtree


CSV_PATH = './files/csv'
JSON_PATH = './files/json'


def measure_run_time(func):
    """
    The `measure_run_time` function is a Python decorator that measures the execution time of a given
    function.
    
    :param func: The `func` parameter in the `measure_run_time` function is a function that you want to
    measure the execution time of. The `measure_run_time` function is a decorator that calculates the
    time taken for the provided function to execute and prints out the duration in seconds after the
    function has completed its
    :return: The `measure_run_time` function is returning the `wrap` function, which is a wrapper
    function that measures the execution time of the input function `func`.
    """
    def wrap(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'\t>>> La función {func.__name__}() tardó {end_time - start_time} segundos en ejecución')
        return result
    return wrap


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