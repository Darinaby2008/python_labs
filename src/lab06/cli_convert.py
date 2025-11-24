import sys
import argparse

from _lib_ import csv_to_xlsx
from _lib_ import json_to_csv
from _lib_ import csv_to_json
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
