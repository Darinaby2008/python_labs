import csv
import json
import os
from pathlib import Path


def check_file_extension(file_path: str, expected_extensions: tuple) -> bool:
    """Проверяет расширение файла"""
    return any(
        Path(file_path).suffix.lower().endswith(ext) for ext in expected_extensions
    )


def _is_float(value: str) -> bool:
    """Проверяет можно ли преобразовать строку в float"""
    try:
        float(value)
        return True
    except ValueError:
        return False


def json_to_csv(json_path: str, csv_path: str):
    """Конвертирует JSON в CSV"""
    # СНАЧАЛА проверяем расширения
    if not check_file_extension(json_path, ('.json',)):
        raise ValueError("Входной файл не является JSON.")
    
    if not check_file_extension(csv_path, ('.csv',)):
        raise ValueError("Выходной файл не является CSV.")
    
    # ПОТОМ проверяем существование файла
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Файл {json_path} не найден")
    
    if os.path.getsize(json_path) == 0:
        raise ValueError("JSON файл пустой")
    
    # Читаем JSON
    with open(json_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    
    # ИСПРАВЛЕНИЕ: Проверяем что данные не пустые
    if not json_data:
        raise ValueError("JSON файл не содержит данных")
    
    if not all(isinstance(x, dict) for x in json_data):
        raise ValueError("JSON должен содержать список словарей")
    
    # Получаем ВСЕ заголовки из ВСЕХ записей
    all_headers = set()
    for item in json_data:
        all_headers.update(item.keys())
    
    # Записываем CSV с ВСЕМИ заголовками
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=sorted(all_headers))
        writer.writeheader()
        
        # Записываем все строки, заполняя отсутствующие поля пустыми значениями
        for row in json_data:
            # Создаем новую строку с всеми возможными полями
            complete_row = {header: row.get(header, '') for header in sorted(all_headers)}
            writer.writerow(complete_row)

def csv_to_json(csv_path: str, json_path: str):
    """Конвертирует CSV в JSON"""
    # СНАЧАЛА проверяем расширения
    if not check_file_extension(csv_path, ('.csv',)):
        raise ValueError(f"Входной файл '{csv_path}' не является CSV.")
    
    if not check_file_extension(json_path, ('.json',)):
        raise ValueError(f"Выходной файл '{json_path}' не является JSON.")
    
    # ПОТОМ проверяем существование файла
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Файл {csv_path} не найден")
    
    if os.path.getsize(csv_path) == 0:
        raise ValueError("CSV файл пустой")
    
    try:
        # Читаем CSV
        with open(csv_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            data = list(reader)
        
        if not data:
            raise ValueError("CSV файл не содержит данных")
        
        # Преобразуем числа
        for row in data:
            for key, value in row.items():
                if not value:  # Пропускаем пустые значения
                    continue
                    
                # Пробуем преобразовать в int
                if value.isdigit():
                    row[key] = int(value)
                # Пробуем преобразовать в float
                elif _is_float(value):
                    row[key] = float(value)
                # Остальные значения оставляем как строки
        
        # Записываем JSON
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
            
    except Exception as e:
        raise ValueError(f"Ошибка при чтении CSV: {str(e)}")