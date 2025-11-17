import csv
import json
import sys
import os
from pathlib import Path

# Функция для проверки расширения файла
def check_file_extension(file_path: str, expected_extensions: tuple) -> bool:
    """
    Проверяет расширение файла на совпадение с ожидаемым списком расширений.
    :param file_path: полный путь к файлу
    :param expected_extensions: кортеж ожидаемых расширений
    :return: True, если расширение совпадает, иначе False
    """
    # Получаем суффикс файла и сравниваем его с ожидаемыми расширениями
    return any(Path(file_path).suffix.lower().endswith(ext) for ext in expected_extensions)


def json_to_csv(json_path: str, csv_path: str) -> None:
    if not os.path.exists(json_path):
        print("FileNotFoundError")
      
    # Проверяем расширение входящего файла
    if not check_file_extension(json_path, ('.json',)):
        raise ValueError(f"Входной файл не является JSON.")
         

    # Проверяем расширение выходящего файла
    if not check_file_extension(csv_path, ('.csv',)):
       raise ValueError(f"Выходной файл не является CSV.")
      
    
    if os.path.getsize(json_path) == 0:
        print("ValueError")
        sys.exit(1)
    with open(json_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        if not all(type(x) == dict for x in json_data):
            print("ValueError")
            sys.exit(1)

    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=json_data[0].keys())
        writer.writeheader()
        writer.writerows(json_data)
        

def csv_to_json(csv_path: str, json_path: str) -> None:
    if not os.path.exists(csv_path):
        print("FileNotFoundError")
        sys.exit(1)
    # Проверяем расширение входящего файла
    if not check_file_extension(csv_path, ('.csv',)):
        return "ValueError(f"Входной файл '{csv_path}' не является CSV.")"

    # Проверяем расширение выходящего файла
    if not check_file_extension(json_path, ('.json',)):
        raise ValueError(f"Выходной файл '{json_path}' не является JSON.")
    if csv_path.lower().enswith('csv'):
        print("Не тот тип фала")
    if type(csv_path)=='CSV':
        print("Не то тип файла") 
    if os.path.getsize(csv_path) == 0:
        print("ValueError")
        sys.exit(1)
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader, None)
        if not header:
            print("ValueError")
            sys.exit(1)
        reader = csv.DictReader(csvfile)
        data = list(reader)
    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

json_to_csv(r"C:\Users\darin\Documents\GitHub\python_labs\date\samples\people.json", r"C:\Users\darin\Documents\GitHub\python_labs\people_from_json.json" )
csv_to_json(r"C:\Users\darin\Documents\GitHub\python_labs\date\samples\people.json", r"C:\Users\darin\Documents\GitHub\python_labs\people_from_csv.csv")
#json_to_csv( r"C:\Users\darin\Documents\GitHub\python_labs\date\samples\people.csv", r"C:\Users\darin\Documents\GitHub\python_labs\people_from_json.json" )

