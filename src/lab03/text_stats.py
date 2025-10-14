import sys

sys.path.append(r'C:\Users\darin\Documents\GitHub\python_labs\src\lab03\text.py')

from text import *

def stats(text: str) -> None:
    print(f'Всего слов: {len(tokenize(normalize(text)))}')
    print(f'Уникальных слов: {len(count_freq(tokenize(normalize(text))))}')
    print('Топ-5:')
    for cursor in top_n(count_freq(tokenize(normalize(text))))[:5]:
        print(f'{cursor[0]}: {cursor[-1]}')


text_in = sys.stdin.buffer.read().decode()

stats(text_in)