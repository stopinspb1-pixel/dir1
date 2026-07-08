import random

def generate_source_file(filename="source.txt", count=200):
    """Генерирует файл со случайными числами от 0 до 1."""
    with open(filename, "w", encoding="utf-8") as file:
        for _ in range(count):
            # random.random() генерирует float в диапазоне [0.0, 1.0)
            file.write(f"{random.random()}\n")

if __name__ == "__main__":
    generate_source_file()
    print("Файл source.txt успешно создан!")
