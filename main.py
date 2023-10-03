import pyshark
import datetime
import csv
import os
from extractors.dir_extractor import DirExtractor
from spiders.subnet_spiders import SubnetSpider

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

    file_spider = DirExtractor()
    file_list = file_spider.file_inspect()

    """
    На данный момент вывод информации идет через консоль.
    Выводится название файла и список уникальных ipv6 адресов.
    """
    for file in file_list:
        print(file)
        unique_ip_list = []
        cap = pyshark.FileCapture(SRC_BASE_DIR + file)

        for packet in cap:
            spider = SubnetSpider(raw_text_default=str(packet))
            ip_list = spider.find_ip(BASE_IP_PATTERN)
            for i in ip_list:
                if i in unique_ip_list:
                    continue
                else:
                    unique_ip_list.append(i)
        print(unique_ip_list)







