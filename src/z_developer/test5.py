# def file_reader(filepath):
#     with open(filepath, 'r') as f:
#         while True:
#             lines_to_read = None  # Ждем количество строк для чтения
#             if lines_to_read is None:
#                 lines_to_read = 1  # По умолчанию читаем 1 строку
#             result = []
#             for _ in range(lines_to_read):
#                 line = f.readline()
#                 if not line:  # Если достигнут конец файла
#                     yield result or None  # Возвращаем результат или None, если файл пустой
#                     return
#                 result.append(line.strip())
#             lines_to_read = yield result  # Возвращаем результат
#
# # Пример использования генератора
# gen = file_reader("example.txt")
# next(gen)  # Инициализация генератора
#
# print(gen.send(1))   # Читаем 1 строку
# print(gen.send(3))   # Читаем 3 строки
# print(gen.send(None)) # Читаем 1 строку по умолчанию
# print(gen.send(2))   # Читаем 2 строки
from anyio.abc import value


def control_generator():
    print("Генератор запущен")
    yield "nach"
    print(1)
    # value = yield "Начальное значение"  # первая точка ожидания
    #
    # print(f"Получено через send: {value}")
    value = 2
    value = yield f"Обработано: {value}"  # вторая точка ожидания

    print(f"Получено через send: {value}")
    yield f"Последнее значение: {value}"


# Создаем экземпляр генератора
gen = control_generator()

# Инициализируем генератор до первой команды yield
print(next(gen))  # Вывод: "Генератор запущен", "Начальное значение"

# Передаем значение через send()
print(gen.send(10))  # Вывод: "Получено через send: 10", "Обработано: 10"
#
# # Еще раз передаем значение через send()
# print(gen.send(20))  # Вывод: "Получено через send: 20", "Последнее значение: 20"
