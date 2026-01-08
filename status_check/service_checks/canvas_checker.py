from .base import ServiceCheck


class CanvasService(ServiceCheck):
    """Canvas/IIIF service checker that can check multiple items.

    Args:
        items: List or tuple of (name, url) tuples to check
               Example: [("AustinMap", "https://..."), ("OtherMap", "https://...")]
    """
    def __init__(self, items=None):
        super().__init__(name="Canvas")
        self.items = items or []

    def run_all_checks(self):
        """Check each item in the list."""
        if not self.items:
            return [("Canvas", False)]

        results = []
        for name, url in self.items:
            try:
                response = self.get(url=url)
                status = self._check_canvases(response)
                results.append((name, status))
            except Exception:
                results.append((name, False))
        return results

    def _check_canvases(self, response):
        """Parse the IIIF response to check if canvases exist."""
        try:
            canvases = response.json().get("sequences", [{}])[0].get("canvases", [])
            return len(canvases) > 0
        except (KeyError, IndexError, ValueError):
            return False


# Backward compatibility: keep old class name as alias
class CanvasCheck(ServiceCheck):
    def __init__(self):
        super().__init__(
            name="[AustinMap](https://spotlight.library.tamu.edu/spotlight/austin-map/catalog/749b8d795ee38de0e9211b9fd04a3075)",
            url=(
                "https://api.library.tamu.edu/iiif-service/dspace/presentation/1969.1/169475/25/SFA_Map_600ppi.jpg"
            )
        )

    def parse_response(self, response):
        canvases = response.json().get("sequences")[0].get("canvases")
        if len(canvases) == 0:
            return False
        else:
            return True
