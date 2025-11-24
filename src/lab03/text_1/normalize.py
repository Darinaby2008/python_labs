import re


def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    if casefold:
        text = text.casefold()
    else:
        text
    if yo2e:
        text = text.replace("ё", "е").replace("Ё", "Е")
    else:
        text
    text = text.strip()
    text = re.sub(r"[\t\r\x00-\x1f\x7F]", " ", text)
    text = " ".join(text.split())
    return text


print(normalize("ПрИвЕт\nМИр\t"))
print(normalize("ёжик, Ёлка"))
print(normalize("Hello\r\nWorld"))
print(normalize("  двойные   пробелы  "))
