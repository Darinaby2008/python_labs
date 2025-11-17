import sys
import os
import argparse
from lib import stats_text

def check_file(file_path: str) -> bool:
    """Проверяет что файл существует"""
    if not os.path.isfile(file_path):
        print(f"Файл не найден: {file_path}", file=sys.stderr)
        return False
    return True

def cat_command(input_file: str, number_lines: bool = False):
    """Выводит содержимое файла"""
    if not check_file(input_file):
        sys.exit(1)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if number_lines:
                print(f"{i:4}  {line}", end='')
            else:
                print(line, end='')

def stats_command(input_file: str, top_n: int = 5):
    """Анализирует статистику слов"""
    if not check_file(input_file):
        sys.exit(1)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
        stats_text(text, top_n)

def main():
    parser = argparse.ArgumentParser(description="CLI утилиты")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Команда cat
    cat_parser = subparsers.add_parser("cat", help="Показать файл")
    cat_parser.add_argument("--input", required=True)
    cat_parser.add_argument("-n", action="store_true")

    # Команда stats  
    stats_parser = subparsers.add_parser("stats", help="Статистика слов")
    stats_parser.add_argument("--input", required=True)
    stats_parser.add_argument("--top", type=int, default=5)

    args = parser.parse_args()

    if args.command == "cat":
        cat_command(args.input, args.n)
    elif args.command == "stats":
        stats_command(args.input, args.top)

if __name__ == "__main__":
    main()

'''import sys
import os
import argparse
from lib import stats_text

def cat_command(input_file: str, number_lines: bool = False):
    if not check_file(input_file):
        sys.exit(1)
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, start=1): 
                if number_lines:
                    print(f"{line_number:6d}  {line}", end='') 
                else:
                    print(line, end='') 
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}", file=sys.stderr)
        sys.exit(1)

def check_file(file_path: str) -> bool:
    if not os.path.exists(file_path):
        print(f"Ошибка: файл '{file_path}' не существует", file=sys.stderr)
        return False
    if not os.path.isfile(file_path):
        print(f"Ошибка: '{file_path}' не является файлом", file=sys.stderr)
        return False

    return True

def stats_command(input_file: str, top_n: int = 5):
    if not check_file(input_file): 
        sys.exit(1)
    
    if top_n <= 0:
        print("Ошибка: значение --top должно быть положительным числом", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
            stats_text(text, top_n)

    except Exception as e: 
        print(f"Ошибка при анализе файла: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Лабораторная №6")
    subparsers = parser.add_subparsers(dest="command")

    cat_parser = subparsers.add_parser("cat", help="Вывести содержимое файла")
    cat_parser.add_argument("--input", required=True) #путь к файлу
    cat_parser.add_argument("-n", action="store_true", help="Нумеровать строки")

    stats_parser = subparsers.add_parser("stats", help="Частоты слов")
    stats_parser.add_argument("--input", required=True)
    stats_parser.add_argument("--top", type=int, default=5) 

    args = parser.parse_args() 
    if args.command == "cat":
        cat_command(args.input, args.n)
    elif args.command == "stats":
        stats_command(args.input, args.top)
    else:

        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()'''