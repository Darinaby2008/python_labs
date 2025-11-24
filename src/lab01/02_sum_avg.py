a = input("a: ")
b = input("b: ")
a = a.replace(",", ".", 1)
b = b.replace(",", ".", 1)
a = float(a)
b = float(b)
sum = a + b
avg = (a + b) / 2
print("Сумма:", round(sum, 2), "Среднее:", round(avg, 2))
