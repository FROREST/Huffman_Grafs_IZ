import heapq
from collections import Counter
import tkinter as tk
from tkinter import messagebox, simpledialog
import json


# Класс для узлов дерева Хаффмана
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char  # Символ
        self.freq = freq  # Частота символа
        self.left = None  # Левый дочерний узел
        self.right = None  # Правый дочерний узел

    # Метод для сравнения узлов (необходим для работы с очередью с приоритетом)
    def __lt__(self, other):
        return self.freq < other.freq


# Функция для построения дерева Хаффмана
def build_huffman_tree(freq_table):
    # Создание кучи (очереди с приоритетом) из узлов дерева
    heap = [HuffmanNode(char, freq) for char, freq in freq_table.items()]
    heapq.heapify(heap)  # Преобразование списка в кучу

    # Построение дерева
    while len(heap) > 1:
        node1 = heapq.heappop(heap)  # Извлечение узла с наименьшей частотой
        node2 = heapq.heappop(heap)  # Извлечение следующего узла с наименьшей частотой
        merged = HuffmanNode(None, node1.freq + node2.freq)  # Создание нового узла
        merged.left = node1  # Присвоение левого дочернего узла
        merged.right = node2  # Присвоение правого дочернего узла
        heapq.heappush(heap, merged)  # Вставка нового узла в кучу

    # Возврат корня дерева
    return heap[0]


# Функция для генерации кодов Хаффмана
def generate_huffman_codes(root):
    codes = {}  # Словарь для хранения кодов символов

    # Вспомогательная рекурсивная функция для генерации кодов
    def _generate_codes(node, current_code):
        if node is None:
            return

        # Если достигнут лист (символ)
        if node.char is not None:
            codes[node.char] = current_code

        # Рекурсивные вызовы для левого и правого дочерних узлов
        _generate_codes(node.left, current_code + "0")
        _generate_codes(node.right, current_code + "1")

    _generate_codes(root, "")  # Начало генерации кодов с пустым текущим кодом
    return codes


# Функция для кодирования строки
def encode_string(input_string, codes):
    return ''.join(codes[char] for char in input_string)  # Замена символов их кодами


# Функция для декодирования строки
def decode_string(encoded_string, root):
    decoded_string = ""
    current_node = root

    # Проход по закодированной строке бит за битом
    for bit in encoded_string:
        if bit == "0":
            current_node = current_node.left
        else:
            current_node = current_node.right

        # Если достигнут лист (символ)
        if current_node.char is not None:
            decoded_string += current_node.char
            current_node = root

    return decoded_string


# Функции для интерфейса

# Функция для кодирования
def encode_action():
    # Запрос строки для кодирования
    input_string = simpledialog.askstring("Ввод строки", "Введите строку для кодирования:")
    if input_string:
        # Создание таблицы частот символов
        freq_table = Counter(input_string)
        # Построение дерева Хаффмана
        huffman_tree = build_huffman_tree(freq_table)
        # Генерация кодов Хаффмана
        huffman_codes = generate_huffman_codes(huffman_tree)
        # Кодирование строки
        encoded_string = encode_string(input_string, huffman_codes)

        # Создание строк для отображения таблицы частот и кодов Хаффмана
        freq_table_text = "\n".join(f"'{char}': {freq}" for char, freq in freq_table.items())
        huffman_codes_text = "\n".join(f"'{char}': {code}" for char, code in huffman_codes.items())

        # Формирование результата для отображения пользователю
        result_text = (
            f"Таблица частот символов:\n{freq_table_text}\n\n"
            f"Коды Хаффмана для символов:\n{huffman_codes_text}\n\n"
            f"Закодированная строка:\n{encoded_string}"
        )
        # Отображение результата
        messagebox.showinfo("Результат кодирования", result_text)


# Функция для декодирования
def decode_action():
    # Запрос строки для декодирования
    encoded_string = simpledialog.askstring("Ввод строки", "Введите строку для декодирования:")
    if encoded_string:
        # Запрос кодов Хаффмана
        huffman_codes_input = simpledialog.askstring("Ввод кодов Хаффмана",
                                                     "Введите коды Хаффмана в формате символ:код (через запятую):")

        if huffman_codes_input:
            # Преобразование кодов из строки в словарь
            huffman_codes = dict(pair.split(":") for pair in huffman_codes_input.split(","))
            # Создание таблицы частот на основе длин кодов (упрощенно)
            freq_table = {char: len(code) for char, code in huffman_codes.items()}
            # Построение дерева Хаффмана
            huffman_tree = build_huffman_tree(freq_table)
            # Декодирование строки
            decoded_string = decode_string(encoded_string, huffman_tree)

            # Формирование результата для отображения пользователю
            result_text = f"Декодированная строка:\n{decoded_string}"
            # Отображение результата
            messagebox.showinfo("Результат декодирования", result_text)


# Создание GUI
def create_gui():
    root = tk.Tk()  # Создание основного окна
    root.title("Кодирование/Декодирование Хаффмана")  # Установка заголовка окна

    # Создание кнопки для кодирования
    encode_button = tk.Button(root, text="Кодировать", command=encode_action)
    encode_button.pack(pady=10)  # Расположение кнопки с отступом

    # Создание кнопки для декодирования
    decode_button = tk.Button(root, text="Декодировать", command=decode_action)
    decode_button.pack(pady=10)  # Расположение кнопки с отступом

    # Запуск главного цикла Tkinter
    root.mainloop()


# Запуск программы
if __name__ == "__main__":
    create_gui()
