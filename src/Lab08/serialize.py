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