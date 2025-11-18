import sys
import argparse

from lib import csv_to_xlsx
from lib import json_to_csv
from lib import csv_to_json
from cli_text import check_file


def main():
    parser = argparse.ArgumentParser(description="Конвертеры данных")
    sub = parser.add_subparsers(dest="command", required=True) 
    
    p1 = sub.add_parser("json2csv")
    p1.add_argument("--in", dest="input", required=True, help="Входной JSON файл")
    p1.add_argument("--out", dest="output", required=True, help="Выходной CSV файл")

    p2 = sub.add_parser("csv2json")
    p2.add_argument("--in", dest="input", required=True, help="Входной CSV файл")
    p2.add_argument("--out", dest="output", required=True, help="Выходной JSON файл")

    p3 = sub.add_parser("csv2xlsx")
    p3.add_argument("--in", dest="input", required=True, help="Входной CSV файл")
    p3.add_argument("--out", dest="output", required=True, help="Выходной XLSX файл")
    
    args = parser.parse_args()

    
    if args.command == "json2csv":
        if not check_file(args.input):
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


'''import sys
import os
import argparse
import json
import csv

def check_file(file_path: str) -> bool:
    if not os.path.isfile(file_path):
        print(f"Файл не найден: {file_path}", file=sys.stderr)
        return False
    return True

def ensure_dir(file_path: str):
    dir_name = os.path.dirname(file_path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)

def json2csv(input_file: str, output_file: str):
    if not check_file(input_file):
        sys.exit(1)
    
    ensure_dir(output_file)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list) or not data:
            print("Ошибка: JSON должен содержать непустой список", file=sys.stderr)
            sys.exit(1)
        
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"Успешно: {input_file} -> {output_file}")
        
    except Exception as e:
        print(f"Ошибка конвертации: {e}", file=sys.stderr)
        sys.exit(1)

def csv2json(input_file: str, output_file: str):
    """Конвертирует CSV в JSON"""
    if not check_file(input_file):
        sys.exit(1)
    
    ensure_dir(output_file)
    
    try:
        data = []
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Успешно: {input_file} -> {output_file}")
        
    except Exception as e:
        print(f"Ошибка конвертации: {e}", file=sys.stderr)
        sys.exit(1)

def csv2xlsx(input_file: str, output_file: str):
    """Конвертирует CSV в XLSX"""
    if not check_file(input_file):
        sys.exit(1)
    
    ensure_dir(output_file)
    
    try:
        # В реальности здесь должен быть код из lab05
        # Создаем простую замену для демонстрации
        
        data = []
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)
        
        # Создаем текстовый файл вместо XLSX для демонстрации
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("XLSX Conversion Demo\\n")
            f.write(f"Original CSV: {input_file}\\n")
            f.write(f"Rows: {len(data)}\\n")
            f.write(f"Columns: {len(data[0]) if data else 0}\\n")
        
        print(f"Демо-режим: {input_file} -> {output_file}")
        print("Для реальной конвертации используй функции из lab05")
        
    except Exception as e:
        print(f"Ошибка конвертации: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Конвертер данных между форматами",
        epilog="""
Примеры:
  python cli_convert.py json2csv --in input.json --out output.csv
  python cli_convert.py csv2json --in input.csv --out output.json
  python cli_convert.py csv2xlsx --in input.csv --out output.xlsx
        """
    )
    
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    # JSON to CSV
    p1 = subparsers.add_parser("json2csv", help="Конвертировать JSON в CSV")
    p1.add_argument("--in", dest="input", required=True, help="Входной JSON файл")
    p1.add_argument("--out", dest="output", required=True, help="Выходной CSV файл")

    # CSV to JSON
    p2 = subparsers.add_parser("csv2json", help="Конвертировать CSV в JSON")
    p2.add_argument("--in", dest="input", required=True, help="Входной CSV файл")
    p2.add_argument("--out", dest="output", required=True, help="Выходной JSON файл")

    # CSV to XLSX
    p3 = subparsers.add_parser("csv2xlsx", help="Конвертировать CSV в XLSX")
    p3.add_argument("--in", dest="input", required=True, help="Входной CSV файл")
    p3.add_argument("--out", dest="output", required=True, help="Выходной XLSX файл")

    args = parser.parse_args()

    if args.cmd == "json2csv":
        json2csv(args.input, args.output)
    elif args.cmd == "csv2json":
        csv2json(args.input, args.output)
    elif args.cmd == "csv2xlsx":
        csv2xlsx(args.input, args.output)

if __name__ == "__main__":
    main()'''


'''import sys, argparse

from lib import csv_to_xlsx
from lib import json_to_csv, csv_to_json
from cli_text import check_file


def cli_convert():
    parser = argparse.ArgumentParser(description="Конвертеры данных")
    sub = parser.add_subparsers(dest="cmd", required=True) # Создание подпарсеров для разных команд
    
    p1 = sub.add_parser("json2csv")
    p1.add_argument("--in", dest="input", required=True, help="Входной JSON файл")
    p1.add_argument("--out", dest="output", required=True, help="Выходной CSV файл")

    p2 = sub.add_parser("csv2json")
    p2.add_argument("--in", dest="input", required=True, help="Входной CSV файл")
    p2.add_argument("--out", dest="output", required=True, help="Выходной JSON файл")

    p3 = sub.add_parser("csv2xlsx")
    p3.add_argument("--in", dest="input", required=True, help="Входной CSV файл")
    p3.add_argument("--out", dest="output", required=True, help="Выходной XLSX файл")
    
    args = parser.parse_args()

    try:
        if args.cmd == "json2csv":
            if not check_file(args.input):
                print(f"Ошибка: Файл {args.input} не существует или недоступен")
                sys.exit(1)
                
            json_to_csv(args.input, args.output)
            print(f"Успешно: JSON -> CSV")
            
        elif args.cmd == "csv2json":
            if not check_file(args.input):
                print(f"Ошибка: Файл {args.input} не существует или недоступен")
                sys.exit(1)
                
            csv_to_json(args.input, args.output)
            print(f"Успешно: CSV -> JSON")
            
        elif args.cmd == "csv2xlsx":
            if not check_file(args.input):
                print(f"Ошибка: Файл {args.input} не существует или недоступен")
                sys.exit(1)
                
            csv_to_xlsx(args.input, args.output)
            print(f"Успешно: CSV -> XLSX")
            
        else:
            print("Ошибка: Неизвестная команда")
            sys.exit(1)
        return 0
        
    except Exception as e:
        print(f"Ошибка при конвертации: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    sys.exit(cli_convert())'''