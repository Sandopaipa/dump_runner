import re


class MacSpider:
    """
    Класс для получения mac-адреса из дампа трафика.
    """
    def __init__(
            self,
            default_raw_text: str
    ):
        """
        default_raw_text: строковое представление пакета дампа трафика.
        """
        self.raw_text = default_raw_text

    def find_mac(self, pattern: str):
        """
        Метод для поиска при помощи паттерна для регулярного выражения.
        """
        frame = self.raw_text
#        print(frame)
        mac_addr = re.search(pattern, frame)

        try:
            return mac_addr.group()
        except AttributeError:
            return None