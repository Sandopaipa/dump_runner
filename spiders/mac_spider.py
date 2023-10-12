import re


class MacSpider:
    def __init__(
            self,
            default_raw_text=None
    ):
        self.raw_text = default_raw_text

    def find_mac(self, pattern=None):
        frame = self.raw_text
#        print(frame)
        mac_addr = re.search(pattern, frame)

        try:
            return mac_addr.group()
        except AttributeError:
            return None