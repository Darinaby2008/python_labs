# Лабораторная работа №5
## Задание А - JSON ↔ CSV
<pre><code>
import csv
import json
import sys
import os

def json_to_csv(json_path: str, csv_path: str) -> None:
    if not os.path.exists(json_path):
        print("FileNotFoundError")
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

from openpyxl import Workbook

def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    if not os.path.exists(csv_path):
        print("FileNotFoundError")
        sys.exit(1)

    if os.path.getsize(csv_path) == 0:
        print("ValueError")
        sys.exit(1)
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    with open(csv_path, "r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            ws.append(row)


    for column_cells in ws.columns:
        max_length = 0
        column_letter = column_cells[0].column_letter
        for cell in column_cells:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        ws.column_dimensions[column_letter].width = max(max_length + 2, 8)
    wb.save(xlsx_path)
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


