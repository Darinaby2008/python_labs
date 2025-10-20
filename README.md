# Лабораторная работа №4
## Задание А - src/lab04/io_txt_csv.py
<pre><code>
from pathlib import Path
import csv
from typing import Iterable, Sequence

def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    try: #попытайся сделать это
        p = Path(path)
        return p.read_text(encoding=encoding)
    except FileNotFoundError: #выполни это, в блоке try произошла ошибка
        return "Такого файла не существует"
    except UnicodeDecodeError: #-*-
        return "Не удалось изменить кодировку"
   

def write_csv(rows: Iterable[Sequence], path: str | Path,
              header: tuple[str, ...] | None = None) -> None:
    p = Path(path)
    rows = list(rows) #Преобразовали в список
    with p.open("w", newline="", encoding="utf-8") as f:
        file_c = csv.writer(f)
        if header is not None and rows == []:
            f_c.writerow(('a','b'))
        if header is not None:
            file_c.writerow(header)
        if rows:
            const = len(rows[0])
            for r in rows:
                if len(r) != const:
                    raise ValueError("Все строки должны иметь одинаковую длину")  
            for r in rows:    
                file_c.writerow(r)
            
def ensure_parent_dir(path: str | Path) -> None:
    p = Path(path)
    parent_dir = p.parent
    parent_dir.mkdir(parents = True, exist_ok = True)
    
print(read_text(r"C:\Users\darin\Documents\GitHub\python_labs\date\input.txt"))
write_csv([("world","count"),("test",3)], r"C:\Users\darin\Documents\GitHub\python_labs\date\check.csv")
</code></pre>
<img width="962" height="425" alt="image" src="https://github.com/user-attachments/assets/7f44c343-b4f7-4196-a6a5-2eed69f45609" />
<img width="963" height="794" alt="image" src="https://github.com/user-attachments/assets/4e0a5eae-116c-424c-b8a4-4ecf64278113" />
<img width="388" height="194" alt="image" src="https://github.com/user-attachments/assets/dbb61d57-3865-4ab7-89b7-c8557ea8710d" />
<img width="1055" height="182" alt="image" src="https://github.com/user-attachments/assets/f32a8cd6-0f97-4e1b-b654-46dda0d7d067" />

## Задание B - src/lab04/text_report.py


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


