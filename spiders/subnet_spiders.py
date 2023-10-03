import ipaddress
import re


class SubnetSpider:
    """
    Класс для поиска ipv6 адресов в заданном диапазоне. Данный класс используется для
    поиска subnet-ipv6 адресов, которые обращаются к мультикастингу.
    """
    def __init__(self,
                 raw_text_default,
                 default_subnet_ip_lower_border='::',
                 default_subnet_ip_higher_border='ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'):

        self.raw_text = raw_text_default
        self.subnet_ip_lower_border = default_subnet_ip_lower_border
        self.subnet_ip_higher_border = default_subnet_ip_higher_border

    def _is_taget(self, ip: str):
        """
        Внутренний метод класса, который проверяет соответствие найденного ip
        заданному диапазону.
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
        """
        try:
            ipv6_addr = ipaddress.IPv6Address(ip)
            if ipv6_addr >= ipaddress.IPv6Address('ff00::'):
                return True
        except:
            pass

    def find_ip(self, pattern=None):

        frame = self.raw_text
        ip_list = re.findall(pattern, frame)
        try:
            source_address = ip_list[0]
            source_address = re.sub(r'\r', '', source_address)
            destination_address = ip_list[1]
            destination_address = re.sub(r'\r', '', destination_address)
            if self._is_multicast(destination_address) is True:
                yield source_address
        except IndexError:
            pass


