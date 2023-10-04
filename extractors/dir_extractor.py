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
        self._dir_check()
        for root, dirs, files in os.walk(self.BASE_DIR):
            for filename in files:
                self.count += 1
                yield filename

    def count_files(self):
        return self.count

    def _dir_check(self):
        if not os.path.exists(os.path.dirname(str(self.BASE_DIR + '/'))):
            os.makedirs(self.BASE_DIR)
            print('Пустая папка src. Пожалуйста, загрузите в неё дампы')

    def _file_check(self, filename):
        """
        Внутренний метод для проверки соответствия названия
        файла и его расширения допустимым названиям.
        Чтобы читать только дампы, а не все файлы в директории
        """
        pass
