def format_record(student: tuple[str, str, float]) -> str:
    if len(student) != 3: #проверяем, что ровно 3 элемента в кортеже
        return "ValueError"
    
    if not (isinstance(student[0], str) and isinstance(student[1], str) and isinstance(student[2], float)): #проверяем, что именно 1-фио, 2-группа,3-GPA.
        return "TypeError"

    fio_parts = student[0].split() # Разделяем ФИО на части
    
    if len(fio_parts) < 2:
        return "ValueError: ФИО должно содержать фамилию и имя"
    
    # Очищаем от лишних пробелов и формируем фамилию и имя
    fio_parts = [part.strip() for part in fio_parts if part.strip()]
    
    res = fio_parts[0].title() + " " + fio_parts[1][0].upper() # Формируем фамилию и первую букву имени с большой буквы
    
    # Добавляем инициалы отчества, если оно есть
    if len(fio_parts) == 3:
        res += "." + fio_parts[2][0].upper() + "., "  
        res += "., "  

    res += "гр. " + student[1] + ", GPA " + f"{round(student[2],2):.2f}" #соединяем все в одно и округляем
    return res 

print(format_record(("Иванов Иван Иванович","BIVT-25",4.6)))
print(format_record(("Петров Пётр", "IKBO-12", 5.0)))
print(format_record(("Петров Пётр Петрович", "IKBO-12", 5.0)))
print(format_record(("  сидорова  анна   сергеевна ", "ABB-01", 3.999)))
print(format_record(("Иванов Иван Иванович","BIVT-25", 4.5))) 