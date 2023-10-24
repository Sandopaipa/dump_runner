import ipaddress
import re


class SubnetIPV6Spider:
    """
    Класс для поиска ipv6 адресов в заданном диапазоне. Данный класс используется для
    поиска ipv6 адресов подсети, которые производят мультиадресную рассылку.
    """
    def __init__(self,
                 raw_text_default,
                 default_subnet_ip_lower_border='fe00::',
                 default_subnet_ip_higher_border='ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'):
        """
        raw_text_default:           строковое представление пакета дампа трафика;
        subnet_ip_lower_border:     нижняя граница диапазона собираемых ip адресов;
        subnet_ip_higher_border:    верхняя граница диапазона собираемых ip адресов.
        """

        self.raw_text = raw_text_default
        self.subnet_ip_lower_border = default_subnet_ip_lower_border
        self.subnet_ip_higher_border = default_subnet_ip_higher_border

    def _is_taget(self, ip: str):
        """
        Внутренний метод класса, который проверяет соответствие найденного ip
        заданному диапазону.
        param: ip - приниматет строковое представление найденного ip адреса.
        """
        try:
            ipv6_addr = ipaddress.IPv6Address(ip)
            if ipv6_addr >= ipaddress.IPv6Address(self.subnet_ip_lower_border)\
                    and ipv6_addr <= ipaddress.IPv6Address(self.subnet_ip_higher_border):
                return True
            else:
                return False
        except:
            pass

    def _is_multicast(self, ip: str):
        """
        Проверяет, идет ли обращение найденного ip к мультикастингу.
        param: ip - приниматет строковое представление найденного ip адреса.
        """
        try:
            ipv6_addr = ipaddress.IPv6Address(ip)
            if ipv6_addr >= ipaddress.IPv6Address('ff00::'):
                return True
        except:
            pass

    def find_ip(self, pattern=None):
        """
        Метод для поиска ip адреса по заданному паттерну.
        pattern: строковое представление паттерна для регулярного выражения.
        """
        result = {
            'src': None,
            'multicast': False
        }

        frame = self.raw_text
        ip_list = re.findall(pattern, frame)
        try:
            source_address = ip_list[0]
            source_address = re.sub(r'\r', '', source_address)
            if self._is_taget(source_address) is True:
                result['src'] = source_address
            else:
                pass
        except IndexError:
            pass
        try:
            destination_address = ip_list[1]
            destination_address = re.sub(r'\r', '', destination_address)
            if self._is_multicast(destination_address) is True:
                result['multicast'] = True
        except IndexError:
            pass

        return result



