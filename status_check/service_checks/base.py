import requests
import inspect


class ServiceCheck:
    """Base class for any HTTP-based service check.

    Supports two patterns:
    1. Single check: Override check() and parse_response() methods
    2. Multiple checks: Define methods starting with 'check_' (e.g., check_yearbooks, check_api)
    """
    def __init__(self, name=None, url=None, timeout=30):
        self.name = name or self.__class__.__name__
        self.url = url
        self.timeout = timeout

    def get(self, url=None, **kwargs):
        """Make a GET request. Uses self.url if no url provided."""
        target_url = url or self.url
        if not target_url:
            raise ValueError("No URL provided for request")
        return requests.get(target_url, timeout=self.timeout, **kwargs)

    def get_checks(self):
        """Discover all check methods in this class."""
        checks = []
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if name.startswith('check_') and name != 'check':
                checks.append((name, method))
        return checks

    def run_all_checks(self):
        """Run all checks and return results as list of (name, status) tuples."""
        checks = self.get_checks()
        if not checks:
            # Fallback to single check() method for backward compatibility
            return [(self.name, self.check())]

        results = []
        for check_name, check_method in checks:
            # Convert check_name to readable format
            readable_name = check_name.replace('check_', '').replace('_', ' ').title()
            try:
                status = check_method()
                results.append((f"{self.name} - {readable_name}", status))
            except Exception as e:
                results.append((f"{self.name} - {readable_name}", False))
        return results

    def check(self):
        """Returns True if service is UP, False if DOWN. Override for single-check services."""
        try:
            response = self.get()
            return self.parse_response(response)
        except Exception as e:
            return False

    def parse_response(self, response):
        """Override in subclasses for single-check pattern."""
        raise NotImplementedError
