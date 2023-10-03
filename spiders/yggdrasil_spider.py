import ipaddress
import re


class YggdrasilSpider:
    '''
    Класс для поиска ip, принадлежащего к Yggdrasil.
    '''
    def __init__(self, raw_text_default):
        self.raw_text = raw_text_default
        self.yggdrasil_200_lower_border = '0200::'
        self.yggdrasil_200_higher_border = '02ff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'
        self.yggdrasil_300_lower_border = '0300::'
        self.yggdrasil_300_higher_border = '03ff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'

    def _is_yggdrasil(self, ip: str):
        """
        Внутренний метод класса, который принимает ip адрес в виде строки без '\r'.
        Проверяет принадлежность адреса к заданному диапазону адресов yggdrasil.
        """
        try:
            ipv6_addr = ipaddress.IPv6Address(ip)
            if ipv6_addr >= ipaddress.IPv6Address(self.yggdrasil_200_lower_border)\
                    and ipv6_addr <= ipaddress.IPv6Address(self.yggdrasil_300_higher_border):
                return True
            elif ipv6_addr >= ipaddress.IPv6Address(self.yggdrasil_300_lower_border)\
                and ipv6_addr <= ipaddress.IPv6Address(self.yggdrasil_300_higher_border):
                return True
            else:
                return False
        except:
            pass

    def find_ip(self, pattern=None):
        """
        Метод для поиска ip адресов по дампу.
        pattern: паттерн для регулярного выражения.
        """

        frame = self.raw_text
        ip_list = re.findall(pattern, frame)
        for ip in ip_list:
            ip = re.sub(r'\r', '', ip)
            if self._is_yggdrasil(ip) is True:
                yield ip

