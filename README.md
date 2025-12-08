# Лабораторная работа №8
## Задание А - Реализовать класс Student (models.py)
<pre><code>
from dataclasses import dataclass
from datetime import datetime, date


@dataclass
class Student:
    fio: str
    birthdate: str
    group: str
    gpa: float

    def __post_init__(self):
        try:
            datetime.strptime(self.birthdate, "%Y-%m-%d")
        except ValueError:
            raise ValueError("warning: birthdate format might be invalid")
        
        if not (0 <= self.gpa <= 5):
            raise ValueError("gpa must be between 0 and 5")


    def age(self) -> int:
        bdate = datetime.strptime(self.birthdate, "%Y-%m-%d").date()
        today = date.today()
        return today.year - b.year - ((today.month, today.day) < (bdate.month, bdate.day))

    def to_dict(self) -> dict:
        return {
            "fio": self.fio,
            "birthdate": self.birthdate,
            "gpa": self.gpa,
            "group": self.group,
        }

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            fio=d["fio"],
            birthdate=d["birthdate"],
            group=d["group"],
            gpa=d["gpa"],
    )



    def __str__(self):
        return f"Student {self.fio},from {self.group},have {self.gpa}"
            
if __name__ == "__main__":
    try:
        student = Student(
            fio="Иванов Иван Иванович",
            birthdate="2000-05-15",
            group="SE-01",
            gpa=4.5
        )
        print(student)
        print(f"Словарь: {student.to_dict()}")
    except ValueError:
        raise ValueError("Ошибка")
</code></pre>
<img width="1280" height="221" alt="image" src="https://github.com/user-attachments/assets/ec0a8422-a18e-4458-85fc-8e072d41b5f1" />

## Задание B - Реализовать модуль serialize.py
<pre><code>
import json
import os
from typing import List
from models import Student

def students_to_json(students: List[Student], path: str) -> None:
    data = [student.to_dict() for student in students]
    
    os.makedirs(os.path.dirname(path), exist_ok=True) # Создаём папки если их нет
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def students_from_json(path: str) -> List[Student]:
    
    try: #Загружает список студентов из JSON файла
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        students = []
        for item in data:
            try:
                student = Student.from_dict(item)
                students.append(student)
            except (ValueError, KeyError) as e:
                print(f"Ошибка при создании студента: {e}")
                continue
                
        return students
    except FileNotFoundError:
        print(f"Файл не найден: {path}")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON: {path}")
        return []
    
if __name__ == "__main__":
    print("=== Тест ЛР8 ===")
    
    # 1. Создаём студентов
    students = [
        Student("Иванов Иван Иванович", "2000-05-15", "SE-01", 4.5),
        Student("Петрова Анна Сергеевна", "2001-08-22", "SE-02", 3.8),
        Student("Сидоров Алексей Борисович", "1999-12-10", "SE-01", 4.2)
    ]
    
    print("1. Создано 3 студента")
    for s in students:
        print(f"   - {s}")
    
    # 2. Сохраняем в data/lab08/
    output_path = "data/lab08/students_output.json"
    students_to_json(students, output_path)
    print(f"2. Сохранено в: {output_path}")
    
    # 3. Загружаем из data/lab08/
    input_path = "data/lab08/students_input.json"
    print(f"3. Загружаем из: {input_path}")
    
    if os.path.exists(input_path):
        loaded_students = students_from_json(input_path)
        print(f"   Загружено студентов: {len(loaded_students)}")
        for s in loaded_students:
            print(f"   - {s}")
    else:
        print(f"   Файл {input_path} не найден!")
        print("   Создайте его с данными студентов")
    
    print("=== Тест завершён ===")
</code></pre>
<img width="1123" height="451" alt="image" src="https://github.com/user-attachments/assets/43e9f1ee-e15d-4d5d-9c87-87eea8a1dcf8" />
<img width="517" height="596" alt="image" src="https://github.com/user-attachments/assets/88a01e03-f106-4e0f-827f-55707d04c118" />

# Лабораторная работа №7
## Задание A - test_text.py
<pre><code>
import sys
import os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")) #путь к папке src

from src._lib_.text import normalize, tokenize, count_freq, top_n


#тесты для normalize
@pytest.mark.parametrize(
    "source, expected",
    [
        ("ПрИвЕт\nМИр\t", "привет мир"),
        ("ёжик, Ёлка", "ежик, елка"),
        ("Hello\r\nWorld", "hello world"),
        ("  двойные   пробелы  ", "двойные пробелы"),
        ("", ""),  # пустая строка
        ("   ", ""),  # только пробелы
    ],
)
def test_normalize(source, expected):
    assert normalize(source) == expected


#тесты для tokenize
@pytest.mark.parametrize(
    "text, expected",
    [
        ("привет мир", ["привет", "мир"]),
        ("hello world test", ["hello", "world", "test"]),
        ("", []),  # пустая строка
        ("   ", []),  # только пробелы
        ("знаки, препинания! тест.", ["знаки", "препинания", "тест"]),
    ],
)
def test_tokenize(text, expected):
    assert tokenize(text) == expected


#тесты для count_freq
@pytest.mark.parametrize(
    "tokens, expected",
    [
        (["a", "b", "a", "c", "b", "a"], {"a": 3, "b": 2, "c": 1}),
        ([], {}),  # пустой список
        (["word"], {"word": 1}),  # один элемент
    ],
)
def test_count_freq(tokens, expected):
    assert count_freq(tokens) == expected


#тесты для top_n 
    "freq_dict, n, expected",
    [
        # Обычный случай
        ({"a": 3, "b": 2, "c": 1}, 3, [("a", 3), ("b", 2), ("c", 1)]),
        # Одинаковые частоты → сортировка по алфавиту
        (
            {"яблоко": 2, "апельсин": 2, "банан": 2},
            3,
            [("апельсин", 2), ("банан", 2), ("яблоко", 2)],
        ),
        # Пустой словарь
        ({}, 5, []),
        # Больше элементов чем n
        (
            {"a": 5, "b": 4, "c": 3, "d": 2, "e": 1, "f": 1},
            3,
            [("a", 5), ("b", 4), ("c", 3)],
        ),
        # n = 0
        ({"a": 1, "b": 2}, 0, []),
    ],
)
def test_top_n(freq_dict, n, expected):
    assert top_n(freq_dict, n) == expected
</code></pre>

## Задание B - test_json_csv.py
<pre><code>
import pytest
import json
import csv
from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")) #путь к src
from src.lab05.json_csv import json_to_csv, csv_to_json


def test_json_to_csv_simple(tmp_path):
    #простая конвертация JSON → CSV
    json_file = tmp_path / "test.json"
    csv_file = tmp_path / "test.csv"

    test_data = [
                 {"name": "Alice", "age": 22},    
                 {"name": "Bob", "age": 25}
    ]

    json_file.write_text(json.dumps(test_data), encoding="utf-8")
    json_to_csv(str(json_file), str(csv_file))

    assert csv_file.exists()

    with csv_file.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        assert len(rows) == 2
        assert {"name", "age"} == set(rows[0].keys())
        assert rows[0]["name"] == "Alice"


def test_csv_to_json_simple(tmp_path):
    #простая конвертация CSV → JSON
    csv_file = tmp_path / "test.csv"
    json_file = tmp_path / "test.json"

    csv_content = "name,age,city\nAlice,22,London\nBob,25,Paris"
    csv_file.write_text(csv_content, encoding="utf-8")

    csv_to_json(str(csv_file), str(json_file))

    assert json_file.exists()

    with json_file.open(encoding="utf-8") as f:
        data = json.load(f)

        assert len(data) == 2
        assert set(data[0].keys()) == {"name", "age", "city"}
        assert data[0]["name"] == "Alice"


def test_json_to_csv_roundtrip(tmp_path):
    #полный цикл конвертации
    original_data = [
                      {"name": "Alice", "age": 22},
                      {"name": "Bob", "age": 25}
    ]

    original_json = tmp_path / "original.json"
    converted_csv = tmp_path / "converted.csv"
    final_json = tmp_path / "final.json"

    original_json.write_text(json.dumps(original_data), encoding="utf-8")
    json_to_csv(str(original_json), str(converted_csv))
    csv_to_json(str(converted_csv), str(final_json))

    with final_json.open(encoding="utf-8") as f:
        final_data = json.load(f)

    assert final_data == original_data


def test_file_not_found():
    #тестируем ошибку когда файл не существует
    with pytest.raises(FileNotFoundError):
        json_to_csv("nonexistent.json", "output.csv")
    with pytest.raises(FileNotFoundError):
        csv_to_json("nonexistent.csv", "output.json")


def test_invalid_cases(tmp_path):
    #тестируем различные ошибочные случаи
    # Некорректный JSON
    json_file = tmp_path / "broken.json"
    json_file.write_text("{ invalid json }", encoding="utf-8")
    with pytest.raises(ValueError):
        json_to_csv(str(json_file), "output.csv")

    # Пустые файлы
    empty_file = tmp_path / "empty.json"
    empty_file.write_text("", encoding="utf-8")
    with pytest.raises(ValueError):
        json_to_csv(str(empty_file), "output.csv")

    # Неправильная структура JSON
    json_file.write_text(json.dumps(["not", "a", "dict"]), encoding="utf-8")
    with pytest.raises(ValueError):
        json_to_csv(str(json_file), "output.csv")

    # Пустой список в JSON
    json_file.write_text(json.dumps([]), encoding="utf-8")
    with pytest.raises(ValueError):
        json_to_csv(str(json_file), "output.csv")

    # CSV только с заголовками
    csv_file = tmp_path / "headers.csv"
    csv_file.write_text("name,age\n", encoding="utf-8")
    with pytest.raises(ValueError):
        csv_to_json(str(csv_file), "output.json")


def test_json_to_csv_different_fields(tmp_path):
    #тестируем JSON с разными полями в записях
    json_file = tmp_path / "test.json"
    csv_file = tmp_path / "test.csv"

    test_data = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 30, "city": "London"},
        {"name": "Charlie", "city": "Paris"},
    ]

    json_file.write_text(json.dumps(test_data), encoding="utf-8")
    json_to_csv(str(json_file), str(csv_file))

    assert csv_file.exists()

    with csv_file.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 3
        assert {"name", "age", "city"} == set(rows[0].keys())
        
def test_csv_to_json_number_conversion(tmp_path):
    #тестируем преобразование чисел из строк
    csv_file = tmp_path / "test.csv"
    json_file = tmp_path / "test.json"

    csv_content = "name,age,score\nAlice,25,95.5\nBob,30,87.0"
    csv_file.write_text(csv_content, encoding="utf-8")
    csv_to_json(str(csv_file), str(json_file))

    with json_file.open(encoding="utf-8") as f:
        data = json.load(f)
        assert data[0]["age"] == 25
        assert data[0]["score"] == 95.5


def test_wrong_extensions(tmp_path):
    #тестируем неправильные расширения файлов
    wrong_file = tmp_path / "file.txt"
    wrong_file.write_text("some content", encoding="utf-8")
    
    with pytest.raises(ValueError):
        json_to_csv(str(wrong_file), "output.csv")
    with pytest.raises(ValueError):
        csv_to_json(str(wrong_file), "output.json")

def test_special_cases(tmp_path):
    #тестируем специальные случаи
    #одна запись в JSON
    json_file = tmp_path / "single.json"
    json_file.write_text(json.dumps([{"name": "Alice", "age": 25}]), encoding="utf-8")
    json_to_csv(str(json_file), tmp_path / "single.csv")

    #юникод символы
    json_file = tmp_path / "unicode.json"
    test_data = [{"name": "Анна", "city": "Москва"}, {"name": "Böb", "city": "München"}]
    json_file.write_text(json.dumps(test_data, ensure_ascii=False), encoding="utf-8")
    json_to_csv(str(json_file), tmp_path / "unicode.csv")

    #специальные символы в CSV
    csv_file = tmp_path / "special.csv"
    csv_content = 'name,comment\nAlice,"Text, with, commas"'
    csv_file.write_text(csv_content, encoding="utf-8")
    csv_to_json(str(csv_file), tmp_path / "special.json")
</code></pre>

## Задание C - стиль кода (black)
<img width="916" height="325" alt="image" src="https://github.com/user-attachments/assets/88bc43a3-c547-4850-b97a-13dfb384aaa0" />

## Дополнительное задание 
<img width="1280" height="728" alt="image" src="https://github.com/user-attachments/assets/69bc0e38-ca67-4615-bf7d-2b6cca9c9cd0" />
<img width="1280" height="119" alt="image" src="https://github.com/user-attachments/assets/09308a02-70bc-4da6-9e9f-37c96ec02eb5" />
<img width="1280" height="508" alt="image" src="https://github.com/user-attachments/assets/5b9f3e95-81ce-4a01-9cb4-c96248ded6eb" />
<img width="1280" height="652" alt="image" src="https://github.com/user-attachments/assets/65f34d46-cb32-4f9f-b574-e81ae45b1c7f" />

# Лабораторная работа №6
## Задание №1 - cli_text.py
<pre><code>
import sys
import os
import argparse
from lib import stats_text

def check_file(file_path: str) -> bool: #проверка файла, существует ли он
    if not os.path.exists(file_path): 
        print(f"Ошибка: файл '{file_path}' не существует", file=sys.stderr)
        return False
    if not os.path.isfile(file_path):
        print(f"Ошибка: '{file_path}' не является файлом", file=sys.stderr)
        return False
    return True

def cat_command(input_file: str, number_lines: bool = False):
    if not check_file(input_file): #проверка файла
        sys.exit(1)
        
    with open(input_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1): #нумеруем строки
            if number_lines: #если включена нумерация строк
                print(f"{i:6d}  {line}", end='') #то выводим номера строк(макс длиной 6 символов) и содержимое строки
            else:
                print(line, end='') #если нет, то выводим строку без номера
    

def stats_command(input_file: str, top_n: int = 5):
    if not check_file(input_file): #проверка файла
        sys.exit(1)
    
    if top_n <= 0:
        print("Ошибка: значение --top должно быть положительным числом", file=sys.stderr)
        sys.exit(1)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read() #читаем файл и проводим через функцию для выведения данных топ-5
        stats_text(text, top_n)

def main():
    parser = argparse.ArgumentParser(description="Лабораторная №6")
    subparsers = parser.add_subparsers(dest="command")

    cat_parser = subparsers.add_parser("cat", help="Вывести содержимое файла")
    cat_parser.add_argument("--input", required=True) #путь к файлу 
    cat_parser.add_argument("-n", action="store_true", help="Нумеровать строки")

    stats_parser = subparsers.add_parser("stats", help="Частоты слов")
    stats_parser.add_argument("--input", required=True) #путь к файлу
    stats_parser.add_argument("--top", type=int, default=5) 

    args = parser.parse_args()  #преобразует в объект args
        
    if args.command == "cat":
        cat_command(args.input, args.n)
    elif args.command == "stats":
        stats_command(args.input, args.top)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
</code></pre>

### Вывод строк и частоты слов
<img width="1280" height="671" alt="image" src="https://github.com/user-attachments/assets/92a1b47e-d774-44c8-b011-c2846cd11121" />

## Задание №2 - cli_convert.py
<pre><code>
import sys
import argparse

from lib import csv_to_xlsx
from lib import json_to_csv
from lib import csv_to_json
from cli_text import check_file


def main():
    parser = argparse.ArgumentParser(description="Конвертеры данных")
    sub = parser.add_subparsers(dest="command", required=True) #cозданtv подпарсерs для разных команд
    
    p1 = sub.add_parser("json2csv")
    p1.add_argument("--in", dest="input", required=True, help="Входной JSON файл")
    p1.add_argument("--out", dest="output", required=True, help="Выходной CSV файл")

    p2 = sub.add_parser("csv2json")
    p2.add_argument("--in", dest="input", required=True, help="Входной CSV файл")
    p2.add_argument("--out", dest="output", required=True, help="Выходной JSON файл")

    p3 = sub.add_parser("csv2xlsx")
    p3.add_argument("--in", dest="input", required=True, help="Входной CSV файл")
    p3.add_argument("--out", dest="output", required=True, help="Выходной XLSX файл")
    
    args = parser.parse_args()  #преобразует в объект args

    
    if args.command == "json2csv":
        if not check_file(args.input): #проверка файла
            print(f"Ошибка: Файл {args.input} не существует или недоступен")
            sys.exit(1)
                
        json_to_csv(args.input, args.output)
        print(f"Успешно: JSON -> CSV")
            
    elif args.command == "csv2json":
        if not check_file(args.input):
            print(f"Ошибка: Файл {args.input} не существует или недоступен")
            sys.exit(1)
                
        csv_to_json(args.input, args.output)
        print(f"Успешно: CSV -> JSON")
            
    elif args.command == "csv2xlsx":
        if not check_file(args.input):
            print(f"Ошибка: Файл {args.input} не существует или недоступен")
            sys.exit(1)
                
        csv_to_xlsx(args.input, args.output)
        print(f"Успешно: CSV -> XLSX")
            
    else:
        print("Ошибка: Неизвестная команда")
        sys.exit(1)
    return 0
        

if __name__ == "__main__":
    main()
</code></pre>

### Вывод JSON => CSV
<img width="1280" height="96" alt="image" src="https://github.com/user-attachments/assets/469e6e8e-2a4f-43e7-b6c4-3b06d4d81652" />
<img width="531" height="187" alt="image" src="https://github.com/user-attachments/assets/cdb212d9-dd9a-495d-8332-b306998003ac" />
<img width="404" height="166" alt="image" src="https://github.com/user-attachments/assets/5cacb6f3-ee75-4dd1-bc66-55854fdd9038" />

### Вывод CSV => JSON
<img width="1280" height="101" alt="image" src="https://github.com/user-attachments/assets/12779514-88ea-4b57-992e-5565d2123378" />
<img width="370" height="168" alt="image" src="https://github.com/user-attachments/assets/82b7a77d-e51d-441c-a394-2b2a5c6a5c10" />
<img width="487" height="251" alt="image" src="https://github.com/user-attachments/assets/fb3b66df-9999-4ccd-a3fd-9d1588e1efe5" />

### Вывод CSV => XLSX
<img width="1280" height="88" alt="image" src="https://github.com/user-attachments/assets/7ea5d6ef-729a-4bf3-8d9e-1117f5aa90ff" />
<img width="504" height="209" alt="image" src="https://github.com/user-attachments/assets/2ff33f23-6e62-48d6-ba89-aaade59acce4" />
<img width="451" height="171" alt="image" src="https://github.com/user-attachments/assets/f98e7738-6396-4cce-b6fd-c8794bd80a01" />

# Лабораторная работа №5
## Задание А - JSON ↔ CSV
<pre><code>
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

def json_to_csv(json_path: str, csv_path: str) -> None: #функция конвертанции JSON в CSV
    if not os.path.exists(json_path): #проверяет, существует ли файл по указанному пути
        print("FileNotFoundError") #если не существует выдает ошибку
   
    if not check_file_extension(json_path, ('.json',)):  #проверяем расширение входящего файла
        raise ValueError(f"Входной файл не является JSON.")
    
    if not check_file_extension(csv_path, ('.csv',)):   #проверяем расширение выходящего файла
       raise ValueError(f"Выходной файл не является CSV.")
    
    if os.path.getsize(json_path) == 0: #получает размер файла в байтах и проверяет, равен ли размер нулю (пустой файл или нет)
        print("ValueError1")
        sys.exit(1) #завершает программу с кодом ошибка 1
    with open(json_path, 'r', encoding='utf-8') as json_file: #безопасно открывае файл для прочтения(автомвтически закрывает после использовния #json_path - путь к файлу
        json_data = json.load(json_file) #закгружает и преобразовывает JSON данные в Python объект #json_data - переменная, содержащая данные из JSON файла
        if not all(type(x) == dict for x in json_data): #type(x) == dict - проверяет, является ли элемент словарем
                                                        #for x in json_data - перебирает все элементы в данных
                                                        #all() - проверяет, что ВСЕ элементы соответствуют условию
                                                        #if not all() - если НЕ все элементы являются словарями
            print("ValueError2") #если не все элементы подходят под условие выдает ошибку
            sys.exit(1)

    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile: #открывает CSV файл для записи(или замены)                                                                           #newline='' - убирает лишние пустые строки 
        writer = csv.DictWriter(csvfile, fieldnames=json_data[0].keys()) #csv.DictWriter() - создает объект для записи CSV из словарей
                                                                         #fieldnames=json_data[0].keys() - название колонок берутся из ключей первого словаря
        writer.writeheader() #запиывает заголовок(название колонок) в CSV файл
        writer.writerows(json_data) #записывает все данные из JSON в CSV файл

def csv_to_json(csv_path: str, json_path: str) -> None: #функция конвертанции CSV в JSON
    if not os.path.exists(csv_path): #проверяет, существует ли файл по указанному пути
        print("FileNotFoundError")  #если не существует выдает ошибку
        sys.exit(1) #завершает программу с кодом ошибка 1
  
    if not check_file_extension(csv_path, ('.csv',)): #проверяем расширение входящего файла
        raise ValueError(f"Входной файл '{csv_path}' не является CSV.")

    if not check_file_extension(json_path, ('.json',)):  #проверяем расширение выходящего файла
        raise ValueError(f"Выходной файл '{json_path}' не является JSON.")
    
    if os.path.getsize(csv_path) == 0: #получает размер файла в байтах и проверяет, равен ли размер нулю (пустой файл или нет)
        print("ValueError3")
        sys.exit(1) #завершает программу с кодом ошибка 1
    with open(csv_path, 'r', encoding='utf-8') as csvfile: #безопасно открывае файл для прочтения(автомвтически закрывает после использовния #csv_path - путь к файлу
        reader = csv.reader(csvfile) #создает объект для чтения CSV
        header = next(reader, None) #читает первую строку(заголовок), NONE - значение по умолчанию, если файл пустой
        if not header: #проверяет, что заголовк есть
            print("ValueError4") #если заголовка нет выводит ошибку
            sys.exit(1)
        reader = csv.DictReader(csvfile) #читает файл
        data = list(reader) #преобразовывет все данные в список
    with open(json_path, 'w', encoding='utf-8') as jsonfile:  #открывает JSON файл для записи(или замены)            
        json.dump(data, jsonfile, ensure_ascii=False, indent=4) #json.dump() - записывает Python объект в JSON файл
                                                                #ensure_ascii=False - разрешает русские символы
                                                                #indent=4 - красивое форматирование с отступами
csv_to_json(r"C:\Users\darin\Documents\GitHub\python_labs\date\samples\people.csv",r"C:\Users\darin\Documents\GitHub\python_labs\date\out\people_from_csv.json")

json_to_csv( r"C:\Users\darin\Documents\GitHub\python_labs\date\samples\people.json",  r"C:\Users\darin\Documents\GitHub\python_labs\date\out\people_from_json.csv" )    
</code></pre>
<img width="1230" height="697" alt="image" src="https://github.com/user-attachments/assets/36555183-9f28-42d4-8dfa-b8cbc6eae1e9" />
<img width="1280" height="669" alt="image" src="https://github.com/user-attachments/assets/e0959a3f-d1bc-4365-88c8-2ec155e6bcf9" />
<img width="396" height="184" alt="image" src="https://github.com/user-attachments/assets/bbd51687-10f6-42ab-94b5-3e00902f8a5a" /> <img width="499" height="291" alt="image" src="https://github.com/user-attachments/assets/7c936017-3121-478a-b4d6-c2273b28cb5f" />
<img width="936" height="244" alt="image" src="https://github.com/user-attachments/assets/1fd2e43e-1b92-4769-93e1-c0b9f65276b1" /> <img width="740" height="168" alt="image" src="https://github.com/user-attachments/assets/b68cdc51-60df-4886-a518-0317d0cbc460" />

## Задание B - CSV → XLSX
<pre><code>
import os
import csv
import sys

from openpyxl import Workbook #из библиотеки openpyx1 импортирует только класс Workbook для создаия Excel файлов

def check_file_type(file_path: str, valid_types: tuple) -> bool: #функция для проверки типа файла по расширению
    """
    Проверяет, соответствует ли расширение файла одному из указанных типов.
    Возвращает True, если файл имеет одно из разрешенных расширений, иначе False.
    """
    return Path(file_path).suffix.lower() in valid_types
    
def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None: #функция конвертанции CSV в XLSX
    if not os.path.exists(csv_path): #если не существует файл по указанному пути, то 
        print("FileNotFoundError") #выводит сообщение об ошибке
        sys.exit(1) #завершает программу с кодом ошибки 1

    if not check_file_type(csv_path, ('.csv',)): #проверка расширения входящего файла (должен быть .csv)
        raise ValueError(f"Входной файл '{csv_path}' не является CSV.")

    if not check_file_type(xlsx_path, ('.xlsx',)):  #проверка расширения выходящего файла (должен быть .xlsx)
        raise ValueError(f"Выходной файл '{xlsx_path}' не является XLSX.")

    if os.path.getsize(csv_path) == 0: #получает размер в байтах и проверяет не равен ли он 0 (пустой файл) 
        print("ValueError")
        sys.exit(1)
    wb = Workbook() #создаем новую Excel книгу
    ws = wb.active #берем первый лист 
    ws.title = "Sheet1" #переменовываем лист в Sheet1

    with open(csv_path, "r", encoding="utf-8") as csv_file: #безопасно открывае файл для прочтения(автомвтически закрывает после использовния #csv_path - путь к файлу
        reader = csv.reader(csv_file) #создает объект для чтения CSV файла
        for row in reader: #перебирает каждую строку в CSV файле, row - переменная, содержащая данные одной строки(как список)
            ws.append(row) #добавляет строку данных в Excel лист

#Настройка ширины колонок
    for column_cells in ws.columns: #перебирает содержания ячейки одной колонки и возвращает все колонки листа 
        max_length = 0 #создает переменную для хранения максимальной длины теста в колонке 
        column_letter = column_cells[0].column_letter #присваивает букву колонки
        for cell in column_cells: #перебирает все ячейки в текущей колонке
            if cell.value: #проверяет есть ли значение в ячейки(не пустая)
                max_length = max(max_length, len(str(cell.value))) #обновляет длину строкиб сравнивая прошлое значение с настоящим 
        ws.column_dimensions[column_letter].width = max(max_length + 2, 8) #обращается к настройкам ширины конкретной колонки, устанавливает ширину колонки, максимальная длина + 2 символа для отступа, 8- выбирает большее значение между расчитанной шириной и минимальной шириной 8 
    wb.save(xlsx_path) #сохраняет Excel книгу по указанному пути
csv_to_xlsx(r"C:\Users\darin\Documents\GitHub\python_labs\date\samples\cities.csv", r"C:\Users\darin\Documents\GitHub\python_labs\date\out\people.xlsx")    
</code></pre>
<img width="901" height="737" alt="image" src="https://github.com/user-attachments/assets/e4fad318-43d9-4124-971a-da09ce552695" />
<img width="1280" height="275" alt="image" src="https://github.com/user-attachments/assets/856b53ee-f8eb-411c-8b35-8e94c6d38e86" />
<img width="580" height="212" alt="image" src="https://github.com/user-attachments/assets/1533ea41-aaa3-4368-b5a5-fe7f8cc45bb9" /><img width="522" height="168" alt="image" src="https://github.com/user-attachments/assets/239547f4-ebf7-4b85-a89b-b1844b4ac57b" />

# Лабораторная работа №4
## Задание А - src/lab04/io_txt_csv.py
<pre><code>
import csv #импортируем встроенную библиотеку для работы с CSV-файлами
import os #импортируем библиотеку для работы с операционной системой
from typing import Iterable, Sequence #импортируем типы для подсказки типов(аннотаций)

def read_text(path: str | Path, encoding: str = "utf-8") -> str: #объявляем функцию для чтения текста
    try: #попытка выполнения кода
        p = Path(path) #преобразуем путь в объект Path
        return p.read_text(encoding=encoding) #читаем текст из файла в указанной кодировке и возвращения его
    except FileNotFoundError: #выполни это, в блоке try произошла ошибка, файл не найден
        return "Такого файла не существует"
    except UnicodeDecodeError: #выполни это, в блоке try произошла ошибка, не правильная кодировка
        return "Не удалось изменить кодировку"
   

def write_csv(rows: Iterable[Sequence], path: str | Path,
              header: tuple[str, ...] | None = None) -> None: #объявляем функция для перевода в CSV(работа с заголовком)
    p = Path(path) #преобразуем путь в объект Path
    rows = list(rows) #Преобразовали объект в список
    with p.open("w", newline="", encoding="utf-8") as f: #with-гарантирует правильное закрытие файла после работы
                                                         #открываем файл в режиме записи "w"
                                                         #newline="" -для корректной работы с переносами строк в CSV
        file_c = csv.writer(f) #создаем объект writer для записи CSV-данных в открытый файл
        if header is not None and rows == []: #записывает тестовые данные, если предан заголовок, но нет строк
            file_c.writerow(('a','b')) 
        if header is not None: #если заголовок указан, то записывается первой строкой в файл
            file_c.writerow(header)
        if rows: #проеряем, что все строки имеют одинаковую количество элементов
            const = len(rows[0])
            for r in rows:
                if len(r) != const: #строки разной длины => ошибка
                    raise ValueError("Все строки должны иметь одинаковую длину")  
            for r in rows:  #записываем все строки в CSV-файл  
                file_c.writerow(r)
            
def ensure_parent_dir(path: str | Path) -> None: #объявляем функцию для создания родительской директории файла
    p = Path(path) #преобразуем путь в объект Path
    parent_dir = p.parent #получаем путь к род. директории
    parent_dir.mkdir(parents = True, exist_ok = True) #создаем директорию со всеми род. директориями если нужно
                                                      #exist_ok=True- не вызфвает ошибку если директория уже существует
    
print(read_text(r"C:\Users\darin\Documents\GitHub\python_labs\date\input.txt"))
write_csv([("world","count"),("test",3)], r"C:\Users\darin\Documents\GitHub\python_labs\date\check.csv", header = None) #записываем все данные CSV-файл без заголовка
</code></pre>
<img width="962" height="425" alt="image" src="https://github.com/user-attachments/assets/7f44c343-b4f7-4196-a6a5-2eed69f45609" />
<img width="963" height="794" alt="image" src="https://github.com/user-attachments/assets/4e0a5eae-116c-424c-b8a4-4ecf64278113" />
<img width="1055" height="182" alt="image" src="https://github.com/user-attachments/assets/f32a8cd6-0f97-4e1b-b654-46dda0d7d067" />
<img width="388" height="194" alt="image" src="https://github.com/user-attachments/assets/dbb61d57-3865-4ab7-89b7-c8557ea8710d" />

## Задание B - src/lab04/text_report.py
<pre><code>
import sys #импортируем встроенный модуль, предоставляет доступ к системным параметрам и функциям
sys.path.append(r'C:\Users\darin\Documents\GitHub\python_labs\src\_lib_') #импортирует модуль sys, который предоставляет доступ к объектам и функциям
from lib_text import * #импортирует все функции из файла lib_text
from io_txt_csv import read_text, write_csv #импортирует конкретные функции 
from stats import statistics #импортирует функцию statistics из модуля stats

input_text = read_text(r'C:\Users\darin\Documents\GitHub\python_labs\date\input_2.txt') #читаем текст из указанного файла
statistics(input_text) #вызываем функцию и передаем ей прочитанный текст 

write_csv(top_n(count_freq(tokenize(normalize(input_text))), 15), path = r'C:\Users\darin\Documents\GitHub\python_labs\date\check_2.csv', header= ['word', 'count']) #нормализуем текст, разбиваем на слова, получаем топ-15 слов
</code></pre>
<img width="1280" height="715" alt="image" src="https://github.com/user-attachments/assets/5981f91c-03da-4cc4-8d32-cd59b2f27921" />
<img width="306" height="547" alt="image" src="https://github.com/user-attachments/assets/f4d0965f-46e5-43ed-9fda-b00654798930" />

# Лабораторная работа №3
## Задание А - src/lib/text.py
## normalize
<pre><code>
import re

def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    if casefold:
         text = text.casefold()
    if yo2e:
        text = text.replace('ё','е').replace('Ё','Е') 
    text = text.strip()
    text = re.sub(r'[\t\r\x00-\x1f\x7F]', ' ', text) 
    text = ' '.join(text.split())
    return text

print(normalize("ПрИвЕт\nМИр\t"))
print(normalize("ёжик, Ёлка"))
print(normalize("Hello\r\nWorld"))
print(normalize("  двойные   пробелы  "))
</code></pre>
![normalized](https://github.com/user-attachments/assets/18dacafc-58af-4c25-87b1-529aeee0f2d1)
## tokenize
<pre><code>
import re

def tokenize(text: str) -> list[str]:
    pattern = r'\w+(?:-\w+)*'
    tokens  = re.findall(pattern, text)
    return tokens

print(tokenize("привет мир"))
print(tokenize("hello,world!!!"))
print(tokenize("по-настоящему круто"))
print(tokenize("2025 год"))
print(tokenize("emoji 😀 не слово"))
</code></pre>
![tokenize](https://github.com/user-attachments/assets/066308b7-0058-4722-83d1-cdbcc25cd3fa)
## count_freq
<pre><code>
import re

def count_freq(tokens: list[str]) -> dict[str, int]:
    unique_words = list(set(tokens))
    list_count = [tokens.count(i) for i in unique_words]
    dict_count = {key: word for key, word in list(zip(unique_words, list_count))}
    return dict_count

print(count_freq(["a","b","a","c","b","a"]))
print(count_freq(["bb","aa","bb","aa","cc"]))
</code></pre>
![tokenize](https://github.com/user-attachments/assets/ff9ea428-53f3-4c4e-a8ab-d6861f66ef8d)
## top_n
<pre><code>
import re

def count_freq(tokens: list[str]) -> dict[str, int]:
    unique_words = list(set(tokens))
    list_count = [tokens.count(i) for i in unique_words]
    dict_count = {key: word for key, word in list(zip(unique_words, list_count))}
    return dict_count

def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    list_dict = list(freq.items())
    top = sorted(list_dict, key=lambda x:  x[0])
    top_plus = sorted(top, key=lambda x: x[1], reverse=True)[:n]
    return top_plus

print(top_n(count_freq(["a","b","a","c","b","a"]),n=2))
print(top_n(count_freq(["bb","aa","bb","aa","cc"]),n=2))
</code></pre>
![top_n](https://github.com/user-attachments/assets/afb36419-2727-44df-8c35-78be46ae1b82)
## Задание В - src/text_stats.py
Вводим в PowerShell эту команду для изменения кодировки Windows: $OutputEncoding = [System.Text.Encoding]::UTF8. После вводим строку с которой нужно сделать действие
<pre><code>
import sys

sys.path.append(r'C:\Users\darin\Documents\GitHub\python_labs\src\lib')

from text_lib import *

def stats(text: str) -> None:
    print(f'Всего слов: {len(tokenize(normalize(text)))}')
    print(f'Уникальных слов: {len(count_freq(tokenize(normalize(text))))}')
    print('Топ-5:')
    for cursor in top_n(count_freq(tokenize(normalize(text))))[:5]:
        print(f'{cursor[0]}: {cursor[-1]}')


text_in = sys.stdin.buffer.read().decode()

stats(text_in)
</code></pre>
![text_stats](https://github.com/user-attachments/assets/c3765a52-e1e0-4c3c-99ae-2e5cfdd8bf13)

# Лабораторная работа №2
## Задание A - arrays.py
## min_max
<pre><code>
def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    if not nums:
        return 'ValueError'
    return (min(nums), max(nums))

print(min_max([3, -1, 5, 5, 0]))
print(min_max([42]))
print(min_max([-5, -2, -9]))
print(min_max([]))
print(min_max([1.5, 2, 2.0, -3.1]))
</code></pre>  
<img width="855" height="638" alt="image" src="https://github.com/user-attachments/assets/b1635522-562d-4ca9-a9f5-bff459afeb6b" />

## unique_sorted
<pre><code>
def unique_sorted(nums: list[float | int]) -> list[float | int]:
    return sorted(set(nums))

print(unique_sorted([3, 1, 2, 1, 3]))
print(unique_sorted([]))
print(unique_sorted([-1, -1, 0, 2, 2]))
print(unique_sorted([1.0, 1, 2.5, 2.5, 0]))
</code></pre>
![01_arrays_unique_sorted](https://github.com/user-attachments/assets/c11e1f92-c961-4927-b300-b164200e0a5b)
## flatten
<pre><code>
def flatten(mat: list[list | tuple]) -> list:
    a = []
    for container in mat:
        if not isinstance(container, (list, tuple)):
            return TypeError
        for item in container:
            a.append(item)
    return a

print(flatten([[1, 2], [3, 4]]))
print(flatten(([1, 2], (3, 4, 5))))
print(flatten([[1], [], [2, 3]]))
print(flatten([[1, 2], "ab"]))
</code></pre>
![01_arrays_flatten](https://github.com/user-attachments/assets/9fb0666c-a324-4c25-8708-963256d2d096)

# Задание B - matrix.py
# transpose
<pre><code>
def transpose(mat: list[list[float | int]]) -> list[list]:
    if not mat:
        return []
    n = len(mat[0]) 
    for row in mat:
        if len(row) != n:
            return "ValueError"  
    res = [] 
    for j in range(n): 
        new_row = []  
        for i in range(len(mat)): 
            new_row.append(mat[i][j])  
        res.append(new_row)  
    return res  

print(transpose([[1, 2, 3]]))
print(transpose([[1], [2], [3]]))
print(transpose([[1, 2], [3, 4]]))
print(transpose([]))
print(transpose([[1, 2], [3]]))
</code></pre>
![matrix_transpose](https://github.com/user-attachments/assets/6dc14cf2-e439-47d4-a83f-701398b16cc4)
# row_sums
<pre><code>
def row_sums(mat: list[list[float | int]]) -> list[float]:
    if not mat:
        return [] 
    n = len(mat[0])
    for row in mat:
        if len(row) != n:
            return "ValueError" 
    res = []  
    for row in mat:  
        k = 0  
        for a in row:  
            k += a 
        res.append(k)  
    return res  

print(row_sums([[1, 2, 3], [4, 5, 6]]))
print(row_sums([[-1, 1], [10, -10]]))
print(row_sums([[0, 0], [0, 0]]))
print(row_sums([[1, 2], [3]]))
</code></pre>
![matrix_row_sums](https://github.com/user-attachments/assets/e646e50a-154a-4437-8d0d-438c3da03a4b)
# col_sums
<pre><code>
def col_sums(mat):
    if not mat:
        return [] 
    n = len(mat[0])
    for row in mat:
        if len(row) != n:
            return "ValueError"  
    res = []  
    for j in range(n):  
        k = 0  
        for i in range(len(mat)):  
            k += mat[i][j] 
        res.append(k)  
    return res 
print(col_sums([[1, 2, 3], [4, 5, 6]]))
print(col_sums([[-1, 1], [10, -10]]))
print(col_sums([[0, 0], [0, 0]]))
print(col_sums([[1, 2], [3]]))
</code></pre>
![matrix_col_sums](https://github.com/user-attachments/assets/4086dd06-95f8-4fb6-aed3-78449d695c60)
# Задание C - tuples.py
<pre><code>
def format_record(student: tuple[str, str, float]) -> str:
    if len(student) != 3: 
        return "ValueError"
    
    if not (isinstance(student[0], str) and isinstance(student[1], str) and isinstance(student[2], float)): 
        return "TypeError"

    fio_parts = student[0].split() 
    
    if len(fio_parts) < 2:
        return "ValueError: ФИО должно содержать фамилию и имя"
    
    fio_parts = [part.strip() for part in fio_parts if part.strip()]
    
    res = fio_parts[0].title() + " " + fio_parts[1][0].upper()  
   
    if len(fio_parts) == 3:
        res += "." + fio_parts[2][0].upper() + "., "  
        res += "., "  

    res += "гр. " + student[1] + ", GPA " + f"{round(student[2],2):.2f}" 
    return res 

print(format_record(("Иванов Иван Иванович","BIVT-25",4.6)))
print(format_record(("Петров Пётр", "IKBO-12", 5.0)))
print(format_record(("Петров Пётр Петрович", "IKBO-12", 5.0)))
print(format_record(("  сидорова  анна   сергеевна ", "ABB-01", 3.999)))
print(format_record(("Иванов Иван Иванович","BIVT-25", 4.5))) 
</code></pre>
![typles](https://github.com/user-attachments/assets/e7ce9b88-dc29-44c5-af1a-4c3e3208b630)

# Лабораторная работа №1
## Задание №1
<pre><code>
name=input("Имя: ")
age=int(input("Возраст: "))
print("Привет,",name,"! Через год тебе будет", age+1,".")
</code></pre>
<img width="758" height="346" alt="image" src="https://github.com/user-attachments/assets/1d732caf-6b5f-4c40-a1c6-96ad3e0c2c32" />

## Задание №2
<pre><code>
a=(input("a: "))
b=(input("b: "))
a=a.replace(",",".",1)
b=b.replace(",",".",1)
a=float(a)
b=float(b)
sum=a+b
avg=(a+b)/2
print("Сумма:",round(sum,2),"Среднее:",round(avg,2))
</pre></code>
<img width="729" height="705" alt="image" src="https://github.com/user-attachments/assets/e215004b-92b6-4bb1-a289-fc7ac28fdfb4" />

## Задание №3
<pre><code>
price=int(input("Исходная цена: "))
discount=int(input("Скидка(%): "))
vat=int(input("НДС(%): "))
base=price*(1-discount/100)
vat_amount=base*(vat/100)
total=base+vat_amount
print(f"База после скидки: {base:.2f}₽")
print(f"НДС: {vat_amount:.2f}₽")
print(f"Итого к оплате: {total:.2f}₽")
</code></pre>
<img width="1280" height="287" alt="image" src="https://github.com/user-attachments/assets/19b111ea-b8e1-406a-8f3a-d820d59bbe82" />

## Задание №4
<pre><code>
m=int(input("Минуты: "))
day=m//1440
hours=(m%1440)//60
minutes=m%60
print(f"{day:02d}:{hours:02d}:{minutes:02d}")
</code></pre>
<img width="668" height="552" alt="image" src="https://github.com/user-attachments/assets/816b774f-0237-405f-ab6c-05c8797867e5" />

## Задание №5
<pre><code>
fio=input("ФИО: ")
fio_clean=' '.join(fio.split())
k=len(fio_clean)
FIO=fio.split()

print(f"Иницыалы: {FIO[0][:1]}{FIO[1][:1]}{FIO[2][:1]}.")
print(f"Длина (символов): {k}")
</code></pre>
<img width="818" height="472" alt="image" src="https://github.com/user-attachments/assets/e3e23107-7ba4-409c-905a-b6dd1c10e04d" />


