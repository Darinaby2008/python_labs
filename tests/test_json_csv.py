import pytest
import json
import csv
from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.lab05.json_csv import json_to_csv, csv_to_json


def test_json_to_csv_simple(tmp_path):
    """Простая конвертация JSON → CSV"""
    json_file = tmp_path / "test.json"
    csv_file = tmp_path / "test.csv"

    test_data = [{"name": "Alice", "age": 22}, {"name": "Bob", "age": 25}]

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
    """Простая конвертация CSV → JSON"""
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
    """Полный цикл конвертации"""
    original_data = [{"name": "Alice", "age": 22}, {"name": "Bob", "age": 25}]

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
    """Тестируем ошибку когда файл не существует"""
    with pytest.raises(FileNotFoundError):
        json_to_csv("nonexistent.json", "output.csv")

    with pytest.raises(FileNotFoundError):
        csv_to_json("nonexistent.csv", "output.json")


def test_invalid_json(tmp_path):
    """Тестируем некорректный JSON"""
    json_file = tmp_path / "broken.json"
    csv_file = tmp_path / "output.csv"

    json_file.write_text("{ invalid json }", encoding="utf-8")

    with pytest.raises(ValueError):
        json_to_csv(str(json_file), str(csv_file))


def test_empty_files(tmp_path):
    """Тестируем пустые файлы"""
    json_file = tmp_path / "empty.json"
    csv_file = tmp_path / "empty.csv"
    output_json = tmp_path / "output.json"
    output_csv = tmp_path / "output.csv"

    # Пустой JSON
    json_file.write_text("", encoding="utf-8")
    with pytest.raises(ValueError):
        json_to_csv(str(json_file), str(output_csv))

    # Пустой CSV
    csv_file.write_text("", encoding="utf-8")
    with pytest.raises(ValueError):
        csv_to_json(str(csv_file), str(output_json))


def test_json_to_csv_different_fields(tmp_path):
    """Тестируем JSON с разными полями в записях"""
    json_file = tmp_path / "test.json"
    csv_file = tmp_path / "test.csv"

    test_data = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 30, "city": "London"},  # дополнительное поле
        {"name": "Charlie", "city": "Paris"},  # отсутствует поле age
    ]

    json_file.write_text(json.dumps(test_data), encoding="utf-8")
    json_to_csv(str(json_file), str(csv_file))

    assert csv_file.exists()

    with csv_file.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        assert len(rows) == 3
        # Проверяем что есть все возможные заголовки
        assert {"name", "age", "city"} == set(rows[0].keys())


def test_csv_to_json_number_conversion(tmp_path):
    """Тестируем преобразование чисел из строк"""
    csv_file = tmp_path / "test.csv"
    json_file = tmp_path / "test.json"

    csv_content = "name,age,score\nAlice,25,95.5\nBob,30,87.0"
    csv_file.write_text(csv_content, encoding="utf-8")

    csv_to_json(str(csv_file), str(json_file))

    with json_file.open(encoding="utf-8") as f:
        data = json.load(f)

        # Проверяем что числа преобразованы правильно
        assert data[0]["age"] == 25  # должно быть int
        assert data[0]["score"] == 95.5  # должно быть float


def test_csv_to_json_empty_data(tmp_path):
    """Тестируем CSV только с заголовком"""
    csv_file = tmp_path / "test.csv"
    json_file = tmp_path / "test.json"

    csv_content = "name,age\n"  # только заголовки, нет данных
    csv_file.write_text(csv_content, encoding="utf-8")

    with pytest.raises(ValueError):
        csv_to_json(str(csv_file), str(json_file))

def test_check_file_extension():
    """Тестируем функцию проверки расширений"""
    from src.lab05.json_csv import check_file_extension
    
    assert check_file_extension("file.json", ('.json',)) == True
    assert check_file_extension("file.csv", ('.csv',)) == True
    assert check_file_extension("data.JSON", ('.json',)) == True
    assert check_file_extension("file.txt", ('.json', '.csv')) == False

def test_is_float():
    """Тестируем функцию проверки float чисел"""
    from src.lab05.json_csv import _is_float
    
    assert _is_float("3.14") == True
    assert _is_float("95.5") == True
    assert _is_float("42") == True
    assert _is_float("text") == False
    assert _is_float("") == False

def test_json_to_csv_empty_data(tmp_path):
    """Тестируем JSON с пустым списком"""
    json_file = tmp_path / "empty.json"
    csv_file = tmp_path / "empty.csv"
    
    # Пустой список
    json_file.write_text(json.dumps([]), encoding="utf-8")
    
    with pytest.raises(ValueError):
        json_to_csv(str(json_file), str(csv_file))

def test_csv_to_json_only_headers(tmp_path):
    """Тестируем CSV только с заголовками"""
    csv_file = tmp_path / "headers.csv"
    json_file = tmp_path / "headers.json"
    
    csv_content = "name,age,city\n"  # только заголовки
    csv_file.write_text(csv_content, encoding="utf-8")
    
    with pytest.raises(ValueError):
        csv_to_json(str(csv_file), str(json_file))

def test_json_to_csv_single_record(tmp_path):
    """Тестируем JSON с одной записью"""
    json_file = tmp_path / "single.json"
    csv_file = tmp_path / "single.csv"
    
    test_data = [{"name": "Alice", "age": 25}]
    
    json_file.write_text(json.dumps(test_data), encoding="utf-8")
    json_to_csv(str(json_file), str(csv_file))
    
    assert csv_file.exists()
    
    with csv_file.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        assert len(rows) == 1
        assert rows[0]["name"] == "Alice"
        assert rows[0]["age"] == "25"

def test_csv_to_json_special_characters(tmp_path):
    """Тестируем CSV со специальными символами"""
    csv_file = tmp_path / "special.csv"
    json_file = tmp_path / "special.json"
    
    csv_content = 'name,comment\nAlice,"Text, with, commas"\nBob,"Text with ""quotes"""'
    csv_file.write_text(csv_content, encoding="utf-8")
    
    csv_to_json(str(csv_file), str(json_file))
    
    assert json_file.exists()
    
    with json_file.open(encoding="utf-8") as f:
        data = json.load(f)
        
        assert len(data) == 2
        assert data[0]["name"] == "Alice"

def test_json_to_csv_unicode(tmp_path):
    """Тестируем JSON с юникод символами"""
    json_file = tmp_path / "unicode.json"
    csv_file = tmp_path / "unicode.csv"
    
    test_data = [
        {"name": "Анна", "city": "Москва"},
        {"name": "Böb", "city": "München"}
    ]
    
    json_file.write_text(json.dumps(test_data, ensure_ascii=False), encoding="utf-8")
    json_to_csv(str(json_file), str(csv_file))
    
    assert csv_file.exists()
    
    with csv_file.open(encoding="utf-8") as f:
        content = f.read()
        assert "Анна" in content
        assert "Москва" in content
 
def test_json_to_csv_invalid_structure(tmp_path):
    """Тестируем JSON с неправильной структурой"""
    json_file = tmp_path / "invalid.json"
    csv_file = tmp_path / "invalid.csv"
    
    # Не список словарей
    json_file.write_text(json.dumps({"not": "a list"}), encoding="utf-8")
    
    with pytest.raises(ValueError):
        json_to_csv(str(json_file), str(csv_file))

def test_csv_to_json_missing_file():
    """Тестируем ошибку когда файл не существует"""
    with pytest.raises(FileNotFoundError):
        csv_to_json("nonexistent.csv", "output.json")

def test_json_to_csv_wrong_extension(tmp_path):
    """Тестируем неправильное расширение файла"""
    # Создаем временный файл с неправильным расширением
    wrong_file = tmp_path / "file.txt"
    wrong_file.write_text("some content", encoding="utf-8")
    
    with pytest.raises(ValueError):
        json_to_csv(str(wrong_file), "output.csv")

def test_csv_to_json_wrong_extension(tmp_path):
    """Тестируем неправильное расширение файла"""
    # Создаем временный файл с неправильным расширением
    wrong_file = tmp_path / "file.txt"
    wrong_file.write_text("some content", encoding="utf-8")
    
    with pytest.raises(ValueError):
        csv_to_json(str(wrong_file), "output.json")

def test_is_float_edge_cases():
    """Тестируем граничные случаи для _is_float"""
    from src.lab05.json_csv import _is_float
    
    assert _is_float("3.14") == True
    assert _is_float("-5.5") == True
    assert _is_float("0.0") == True
    assert _is_float("123") == True
    assert _is_float("12.34.56") == False
    assert _is_float("text") == False
    assert _is_float("") == False
    assert _is_float("12a.34") == False

def test_check_file_extension_comprehensive():
    """Тестируем все случаи для check_file_extension"""
    from src.lab05.json_csv import check_file_extension
    
    assert check_file_extension("file.json", ('.json',)) == True
    assert check_file_extension("file.csv", ('.csv',)) == True
    assert check_file_extension("data.JSON", ('.json',)) == True
    assert check_file_extension("data.CSV", ('.csv',)) == True
    assert check_file_extension("file.txt", ('.json', '.csv')) == False
    assert check_file_extension("file", ('.json',)) == False
    assert check_file_extension("file.json.backup", ('.json',)) == False   
def test_json_to_csv_not_list_of_dicts(tmp_path):
    """Тестируем JSON который не список словарей"""
    json_file = tmp_path / "invalid.json"
    csv_file = tmp_path / "invalid.csv"
    
    # Не список словарей
    json_file.write_text(json.dumps(["not", "a", "dict"]), encoding="utf-8")
    
    with pytest.raises(ValueError):
        json_to_csv(str(json_file), str(csv_file))

def test_csv_to_json_read_error(tmp_path):
    """Тестируем ошибку чтения CSV"""
    csv_file = tmp_path / "broken.csv"
    json_file = tmp_path / "broken.json"
    
    # Некорректный CSV
    csv_file.write_text("name,age\nAlice,25\ninvalid,line,with,extra,columns", encoding="utf-8")
    
    # Должна быть ошибка при чтении
    with pytest.raises(ValueError):
        csv_to_json(str(csv_file), str(json_file))    