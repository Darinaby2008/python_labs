import csv
from pathlib import Path
from typing import List
import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.lab08.models import Student

class Group:
    def __init__(self, storage_path: str):
        self.path = Path(storage_path)
        if not self.path.exists():
            self.path.write_text("", encoding="utf-8")

    def __read_all(self) -> List[dict]:
        with self.path.open('r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [row for row in reader]

    def list(self) -> List[Student]:
        rows = self.__read_all()
        return [Student(r["fio"], r["birthdate"], r["group"], float(r["gpa"])) for r in rows]

    def add(self, student: Student):
        rows = self.__read_all()
        rows.append({
            "fio": student.fio,
            "birthdate": student.birthdate,
            "group": student.group,
            "gpa": str(student.gpa)
        })
        with self.path.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["fio", "birthdate", "group", "gpa"])
            writer.writeheader()
            writer.writerows(rows)

    def find(self, substr: str) -> List[Student]:
        rows = self.__read_all()
        found = [r for r in rows if substr in r["fio"]]
        return [Student(r["fio"], r["birthdate"], r["group"], float(r["gpa"])) for r in found]

    def remove(self, fio: str):
        rows = self.__read_all()
        for i, r in enumerate(rows):
            if r["fio"] == fio:
                rows.pop(i)
                break
        with self.path.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["fio", "birthdate", "group", "gpa"])
            writer.writeheader()
            writer.writerows(rows)

    def update(self, fio: str, **fields):
        rows = self.__read_all()
        for r in rows:
            if r["fio"] == fio:
                for key, value in fields.items():
                    if key in ["fio", "birthdate", "group", "gpa"]:
                        r[key] = str(value)
                break
        with self.path.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["fio", "birthdate", "group", "gpa"])
            writer.writeheader()
            writer.writerows(rows)

if __name__ == "__main__":
    group = Group(r'C:\Users\darin\Documents\GitHub\python_labs\data\lab09\students.csv')
    print(group.update('Новиков Сергей', **{'birthdate': '2007.06.24', 'group': 'БИВТ-31-4', 'gpa': 3.8}))