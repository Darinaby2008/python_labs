from pathlib import Path
import csv
import os
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
 
 def main():
    txt = read_text("../data/input.txt")
    print(txt)
    print()
    print('пустой файл:', read_text(r"C:\Users\darin\Documents\GitHub\python_labs\date\pustoy.txt"))
    
    print(read_text(r"C:\Users\darin\Documents\GitHub\python_labs\date\input.txt"))
    write_csv([("word","count"),("test",3)], r"C:\Users\darin\Documents\GitHub\python_labs\date\check.csv") 
    write_csv(rows=[], path=r"C:\Users\darin\Documents\GitHub\python_labs\date\pustoy.csv", header=None) 

if __name__ == '__main__':
    main()

    
# print(read_text(r"C:\Users\darin\Documents\GitHub\python_labs\date\input.txt"))
# write_csv([("world","count"),("test",3)], r"C:\Users\darin\Documents\GitHub\python_labs\date\check.csv", header = None)