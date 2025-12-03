import requests


class ServiceCheck:
    """Base class for any HTTP-based service check."""
    def __init__(self, name, url, timeout=30):
        self.name = name
        self.url = url
        self.timeout = timeout

    def get(self, **kwargs):
        return requests.get(self.url, timeout=self.timeout, **kwargs)

    def check(self):
        """Returns True if service is UP, False if DOWN."""
        try:
            response = self.get()
            return self.parse_response(response)
        except Exception as e:
            return False

    def parse_response(self, response):
        """Override in subclasses."""
        raise NotImplementedError
