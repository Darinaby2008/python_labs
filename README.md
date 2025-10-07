# Лабораторная работа №2
## Задание A - arrays.py
## min_max
<pre><code>
def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    if not nums:
        return 'ValueError'
    return (min(nums), max(nums))

print(min_max([3, -1, 5, 5, 0]))
print(min_max([42]))
print(min_max([-5, -2, -9]))
print(min_max([]))
print(min_max([1.5, 2, 2.0, -3.1]))
</code></pre>  
<img width="855" height="638" alt="image" src="https://github.com/user-attachments/assets/b1635522-562d-4ca9-a9f5-bff459afeb6b" />

## unique_sorted
<pre><code>
def unique_sorted(nums: list[float | int]) -> list[float | int]:
    return sorted(set(nums))

print(unique_sorted([3, 1, 2, 1, 3]))
print(unique_sorted([]))
print(unique_sorted([-1, -1, 0, 2, 2]))
print(unique_sorted([1.0, 1, 2.5, 2.5, 0]))
</code></pre>
![01_arrays_unique_sorted](https://github.com/user-attachments/assets/c11e1f92-c961-4927-b300-b164200e0a5b)
## flatten
<pre><code>
def flatten(mat: list[list | tuple]) -> list:
    a = []
    for container in mat:
        if not isinstance(container, (list, tuple)):
            return TypeError
        for item in container:
            a.append(item)
    return a

print(flatten([[1, 2], [3, 4]]))
print(flatten(([1, 2], (3, 4, 5))))
print(flatten([[1], [], [2, 3]]))
print(flatten([[1, 2], "ab"]))
</code></pre>
![01_arrays_flatten](https://github.com/user-attachments/assets/9fb0666c-a324-4c25-8708-963256d2d096)

# Задание B - matrix.py
# transpose
<pre><code>
</code></pre>

# row_sums
<pre><code>
</code></pre>

# col_sums
<pre><code>
</code></pre>

# Задание C - tuples.py
<pre><code>
</code></pre>


# Лабораторная работа №1
## Задание №1
<pre><code>
name=input("Имя: ")
age=int(input("Возраст: "))
print("Привет,",name,"! Через год тебе будет", age+1,".")
</code></pre>
<img width="758" height="346" alt="image" src="https://github.com/user-attachments/assets/1d732caf-6b5f-4c40-a1c6-96ad3e0c2c32" />

## Задание №2
<pre><code>
a=(input("a: "))
b=(input("b: "))
a=a.replace(",",".",1)
b=b.replace(",",".",1)
a=float(a)
b=float(b)
sum=a+b
avg=(a+b)/2
print("Сумма:",round(sum,2),"Среднее:",round(avg,2))
</pre></code>
<img width="729" height="705" alt="image" src="https://github.com/user-attachments/assets/e215004b-92b6-4bb1-a289-fc7ac28fdfb4" />

## Задание №3
<pre><code>
price=int(input("Исходная цена: "))
discount=int(input("Скидка(%): "))
vat=int(input("НДС(%): "))
base=price*(1-discount/100)
vat_amount=base*(vat/100)
total=base+vat_amount
print(f"База после скидки: {base:.2f}₽")
print(f"НДС: {vat_amount:.2f}₽")
print(f"Итого к оплате: {total:.2f}₽")
</code></pre>
<img width="1280" height="287" alt="image" src="https://github.com/user-attachments/assets/19b111ea-b8e1-406a-8f3a-d820d59bbe82" />

## Задание №4
<pre><code>
m=int(input("Минуты: "))
day=m//1440
hours=(m%1440)//60
minutes=m%60
print(f"{day:02d}:{hours:02d}:{minutes:02d}")
</code></pre>
<img width="668" height="552" alt="image" src="https://github.com/user-attachments/assets/816b774f-0237-405f-ab6c-05c8797867e5" />

## Задание №5
<pre><code>
fio=input("ФИО: ")
fio_clean=' '.join(fio.split())
k=len(fio_clean)
FIO=fio.split()

print(f"Иницыалы: {FIO[0][:1]}{FIO[1][:1]}{FIO[2][:1]}.")
print(f"Длина (символов): {k}")
</code></pre>
<img width="818" height="472" alt="image" src="https://github.com/user-attachments/assets/e3e23107-7ba4-409c-905a-b6dd1c10e04d" />


