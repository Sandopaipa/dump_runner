import os

class DirExtractor:
    """
    Класс, реализующий траверс по директории для чтения
    файлов.
    """
    def __init__(self, default_src_dir='./src'):
        self.BASE_DIR = default_src_dir
        self.count = 0

    def file_inspect(self):
        """
        Метод, который возвращает объект - генератор имен файлов,
        найденных в BASE_DIR.
        """
        for root, dirs, files in os.walk(self.BASE_DIR):
            for filename in files:
                self.count += 1
                yield filename

    def count_files(self):
        return self.count