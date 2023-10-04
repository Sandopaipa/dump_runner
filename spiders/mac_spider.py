import re


class MacSpider:
    def __init__(
            self,
            default_raw_text=None
    ):
        self.raw_text = default_raw_text

    def find_mac(self, pattern=None):
        frame = self.raw_text
        mac_addr = re.search(pattern, frame)
        return mac_addr.group()
