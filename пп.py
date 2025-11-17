import numpy as np
import matplotlib.pyplot as plt

# Центр гиперболы
h, k = 2, -6

# Создаем массив значений x около центра
x = np.linspace(h - 1, h + 1, 400)

# Находим верхнюю и нижнюю ветви гиперболы из канонического уравнения
y_upper = k + np.sqrt(1 + 25 * (x - h)**2)
y_lower = k - np.sqrt(1 + 25 * (x - h)**2)

plt.figure(figsize=(8,6))
plt.plot(x, y_upper, label='Верхняя ветвь')
plt.plot(x, y_lower, label='Нижняя ветвь')

# Добавляем сетку и подписи осей
plt.grid(True)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.xlabel('x')
plt.ylabel('y')
plt.title('График однополостного гиперболоида (гиперболы)')
plt.legend()

# Сохраняем график в PNG-файл
plt.savefig('hyperbola_plot.png', dpi=300)
plt.show()