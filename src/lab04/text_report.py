import sys
sys.path.append(r'C:\Users\darin\Documents\GitHub\python_labs\src\_lib_')
# импортирует модуль sys, который предоставляет доступ к объектам и функциям
from lib_text import tokenize, normalize, top_n 
from io_txt_csv import read_text, write_csv
from  stats import stats

input_text = read_text(r'C:\Users\darin\Documents\GitHub\python_labs\date\input_2.txt')
# читаем текст из указанного файла
stats(input_text)

write_csv(top_n(tokenize(normalize(input_text)), 15), path=r'C:\Users\darin\Documents\GitHub\python_labs\date\check_2.csv', header= ['world', 'count'])
# нормализуем текст, разбиваем на слова, получаем топ-... слов
# write_csv(...) - записываем в CSV файл с заголовком ['world', 'count'] и сохраняет файл