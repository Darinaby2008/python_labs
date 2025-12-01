import json
from models import Student


def students_to_json(students, path):
    data = [s.to_dict() for s in students]
    with open(path, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def students_from_json(path):
    with open(path, "r", encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise TypeError

    student_list = []
    for d in data:
        if not isinstance(d, dict):
            raise TypeError
        if not isinstance(d.get("fio"), str):
            raise TypeError
        if not isinstance(d.get("birthdate"), str):
            raise TypeError
        if not isinstance(d.get("group"), str):
            raise TypeError
        if not isinstance(d.get("gpa"), (float, int)):
            raise TypeError

        try:
            student = Student.from_dict(d)
        except Exception as e:
            raise ValueError

        student_list.append(student)

    return student_list

students_list = students_from_json('data/lab08/students_input.json')
for item in students_list:
    print(item)