import pyshark
import datetime
import csv
import os
from extractors.dir_extractor import DirExtractor
from spiders.mac_spider import MacSpider
from spiders.yggdrasil_spider import YggdrasilSpider
from spiders.subnet_spiders import SubnetIPV6Spider
from data.Node import NodeDataHandler


def traverse_dump(file: str, mac_pattern: str, ygg_pattern: str, subnet_pattern: str):
    packets = pyshark.FileCapture(file)
    for packet in packets:
        mac_spider = MacSpider(str(packet))
        ygg_spider = YggdrasilSpider(str(packet))
        subnet_spider = SubnetIPV6Spider(str(packet))

        mac_addr = mac_spider.find_mac(pattern=mac_pattern)
        ygg_addr = ygg_spider.find_ip(pattern=ygg_pattern)
        subnet_addr = subnet_spider.find_ip(pattern=subnet_pattern)
        node = NodeDataHandler(
            default_mac=mac_addr,
            default_multicasting=subnet_addr['multicast'],
            default_ygg_ipv6=ygg_addr,
            default_subnet_ipv6=subnet_addr['src'],
            default_dump_file_name=file
        )
        node.touch()

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

    traverse_dump(
        file='./src/ygg.pcapng',
        mac_pattern=BASE_MAC_PATTERN,
        subnet_pattern=BASE_IP_PATTERN,
        ygg_pattern=BASE_IP_PATTERN
    )

