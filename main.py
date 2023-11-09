import pyshark
import os
from extractors.dir_extractor import DirExtractor
from spiders.mac_spider import MacSpider
from spiders.yggdrasil_spider import YggdrasilSpider
from spiders.subnet_spiders import SubnetIPV6Spider
from data.Node import NodeDataHandler

import nest_asyncio
nest_asyncio.apply()


def traverse_dump(file: str, mac_pattern: str, ygg_pattern: str, subnet_pattern: str):
    """
    Функция для сбора информации из файла дампа трафика.
    file:           строка - путь к файлу дампа;
    mac_pattern:    строка - паттерн для регулярного выражения, который будет использован для поиска mac-адресов;
    ygg_pattern:    строка - паттерн для регулярного выражения, который будет использован для поиска адресов,
                    которые принадлежат сети yggdrasil;
    subnet_pattern: строка - паттерн для регулярного выражения, который будет использован для поиска ip адресов
                    подсети.
    """
    packets = pyshark.FileCapture(file)
    for packet in packets:
        mac_spider = MacSpider(str(packet))
        ygg_spider = YggdrasilSpider(str(packet))
        subnet_spider = SubnetIPV6Spider(str(packet))

        mac_addr = mac_spider.find_mac(pattern=mac_pattern)
        ygg_addr = ygg_spider.find_ip(pattern=ygg_pattern)
        subnet_addr = subnet_spider.find_ip(pattern=subnet_pattern)

        node = NodeDataHandler(
            mac_addr=mac_addr,
            multicast=subnet_addr['multicast'],
            ygg_ipv6=ygg_addr,
            subnet_ipv6=subnet_addr['src'],
            dump_file_name=file
        )
        node.touch()


def dir_check(_dir: str):
    """
    Функция для проверки наличия директории. В случае, если директория не найдена - создает новую.
    dir: строка - путь к директории.
    """
    if not os.path.exists(os.path.dirname(_dir)):
        os.makedirs(_dir)


if __name__ == '__main__':

    SRC_BASE_DIR = './src/'  # Директория с дампами трафика
    """
    Паттерны для поиска ip и mac-адресов по дампу. BASE_IP_PATTERN используется как для поиска 
    ip адресов подсети - так и для поиска адресов, которые принадлежат yggdrasil.
    """
    BASE_IP_PATTERN = '(?<=Source Address:.).+|(?<=Destination Address:.).+'
    BASE_MAC_PATTERN = '(?<=Source:.)(((([a-f]|[A-F])|\d){2}):){5}(([a-f]|[A-F]|\d){2})'

    file_spider = DirExtractor()
    file_list = file_spider.file_inspect()
    for file in file_list:
        print(file)
        print('wait')
        traverse_dump(
            file=SRC_BASE_DIR+file,
            mac_pattern=BASE_MAC_PATTERN,
            subnet_pattern=BASE_IP_PATTERN,
            ygg_pattern=BASE_IP_PATTERN,
        )
