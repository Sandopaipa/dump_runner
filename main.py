import pyshark
import datetime
import csv
import os
from extractors.dir_extractor import DirExtractor
from spiders.mac_spider import MacSpider


class Node:
    def __init__(
            self,
            default_mac_addr=None,
            default_subnet_ipv4=None,
            default_subnet_ipv6=None,
            default_ygg_ipv6=None,
            initial_node_to_multicast_number=0,
            initial_src_packet_number=0,
            initial_multicast_freq=0.0
    ):
        self.mac_addr = default_mac_addr
        self.subnet_ipv4 = default_subnet_ipv4
        self.subnet_ipv6 = default_subnet_ipv6
        self.ygg_ipv6 = default_ygg_ipv6
        self.node_to_multicast_number = initial_node_to_multicast_number
        self.src_packet_number = initial_src_packet_number
        self.multicast_freq = initial_multicast_freq

        self._mac_addr_pattern = '(((([a-f]|[A-F])|\d){2}):){5}(([a-f]|[A-F]|\d){2})'
        self._ipv4_addr_pattern = '(\d{1,3}}.){3}\d+'
        self.subnet_ipv6_pattern = ''

    def _validate(
            self,
            pattern: str,
            data: str
    ):
        """
        Внутренний метод для проверки валидности введенных данных.
        Принимает на вход строку с данными и должен выдавать
        True или False.
        """
        pass


def dir_check(dir):
    if not os.path.exists(os.path.dirname(dir)):
        os.makedirs(dir)

def timebased_file_name(outdir='./output/'):
    dir_check(outdir)
    date = datetime.datetime.now()
    file_extension = '.csv'
    new_file_name = outdir + date.strftime('%y_%m_%d_%H%M%S') + file_extension
    return new_file_name

def src_based_filename(outdir='./output/'):
    dir_check(outdir)


def addr_output(data):
    outfile = timebased_file_name()

    with open(outfile, 'w', encoding='utf-8', newline="") as file:
        writer = csv.writer(file, delimiter='\n')
        writer.writerow(data)


if __name__ == '__main__':


    """Директория с дампами"""
    SRC_BASE_DIR = './src/'
    """Паттерн для поиска ip по дампу"""
    BASE_IP_PATTERN = '(?<=Source Address:.).+|(?<=Destination Address:.).+'
    BASE_MAC_PATTERN = '(?<=Source:.)(((([a-f]|[A-F])|\d){2}):){5}(([a-f]|[A-F]|\d){2})'

    file_spider = DirExtractor()
    file_list = file_spider.file_inspect()

    """
    На данный момент вывод информации идет через консоль.
    Выводится название файла и список уникальных ipv6 адресов.
    """
    for file in file_list:
        mac_list = []
        dump = pyshark.FileCapture(SRC_BASE_DIR + file)
        for packet in dump:
            mac_spider = MacSpider(str(packet))
            mac_addr = mac_spider.find_mac(BASE_MAC_PATTERN)
            node = Node(default_mac_addr=mac_addr)







