import sys
sys.path.append(r'C:\Users\darin\Documents\GitHub\python_labs\src\_lib_')
# импортирует модуль sys, который предоставляет доступ к объектам и функциям
from lib_text import *
from io_txt_csv import read_text, write_csv
from stats import statistics

input_text = read_text(r'C:\Users\darin\Documents\GitHub\python_labs\date\input_2.txt')
# читаем текст из указанного файла
statistics(input_text)

write_csv(top_n(count_freq(tokenize(normalize(input_text))), 15), path = r'C:\Users\darin\Documents\GitHub\python_labs\date\check_2.csv', header= ['word', 'count'])
# нормализуем текст, разбиваем на слова, получаем топ-... слов

