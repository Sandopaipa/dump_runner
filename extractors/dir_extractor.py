import os


class DirExtractor:
    """
    Класс, реализующий траверс по директории для чтения
    файлов. По-умолчанию обращается к папке src в директории проекта.
    """
    def __init__(self, default_src_dir='./src'):
        self.BASE_DIR = default_src_dir

    def file_inspect(self):
        """
        Метод, который возвращает объект - генератор имен файлов,
        найденных в BASE_DIR.
        """
        self._dir_check()
        for root, dirs, files in os.walk(self.BASE_DIR):
            for filename in files:
                yield filename

    def _dir_check(self):
        """
        Функция для проверки наличия директории. В случае, если директория не найдена - создает новую.
        dir: строка - путь к директории.
        """
        if not os.path.exists(os.path.dirname(str(self.BASE_DIR + '/'))):
            os.makedirs(self.BASE_DIR)
            print('Пустая папка src. Пожалуйста, загрузите в неё дампы')
