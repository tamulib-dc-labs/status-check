from .base import ServiceCheck


class BookreaderCheck(ServiceCheck):
    def __init__(self):
        super().__init__(
            name="[Yearbooks](https://library.tamu.edu/yearbooks/)",
            url=(
                "https://bookreader.library.tamu.edu/BookReader/inside.php"
                "?item_id=yb1910&doc=yb1910&path=/mnt/yearbooks/yb1910"
                "&q=%22staff%22~1"
            )
        )

    def parse_response(self, response):
        for line in response.text.splitlines():
            if 'ValueError: No JSON object could be decoded' in line:
                return False
        return True


class YellBooksCheck(ServiceCheck):
    def __init__(self):
        super().__init__(
            name="[Yellbooks](http://library.tamu.edu/collections/digital-library/yell_books.php)",
            url=(
                "https://bookreader.library.tamu.edu/BookReader/inside.php?item_id=yellbooks_1913&doc=yellbooks_1913&path=/mnt/yearbooks/yellbooks_1913&q=%22largest%22~1"
            )
        )

    def parse_response(self, response):
        for line in response.text.splitlines():
            if 'ValueError: No JSON object could be decoded' in line:
                return False
        return True
