from .base import ServiceCheck


class BookreaderService(ServiceCheck):
    """Bookreader service with multiple checks for different collections."""

    def __init__(self):
        super().__init__(name="Bookreader")

    def check_yearbooks(self):
        """Check Yearbooks collection at https://library.tamu.edu/yearbooks/"""
        try:
            response = self.get(
                url=(
                    "https://bookreader.library.tamu.edu/BookReader/inside.php"
                    "?item_id=yb1910&doc=yb1910&path=/mnt/yearbooks/yb1910"
                    "&q=%22staff%22~1"
                )
            )
            for line in response.text.splitlines():
                if 'ValueError: No JSON object could be decoded' in line:
                    return False
            return True
        except Exception:
            return False

    def check_yellbooks(self):
        """Check Yellbooks collection at http://library.tamu.edu/collections/digital-library/yell_books.php"""
        try:
            response = self.get(
                url=(
                    "https://bookreader.library.tamu.edu/BookReader/inside.php"
                    "?item_id=yellbooks_1913&doc=yellbooks_1913&path=/mnt/yearbooks/yellbooks_1913"
                    "&q=%22largest%22~1"
                )
            )
            for line in response.text.splitlines():
                if 'ValueError: No JSON object could be decoded' in line:
                    print('Failing')
                    return False
                else:
                    print('Success')
            return True
        except Exception:
            return False


# Backward compatibility: keep old class names as aliases
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
