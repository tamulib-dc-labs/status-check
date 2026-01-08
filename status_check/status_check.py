import datetime
from status_check.service_checks import BookreaderCheck, YellBooksCheck, CanvasCheck, BookreaderService, CanvasService


class CheckRunner:
    def __init__(self, checks):
        self.checks = checks

    def run(self):
        results = []
        for check in self.checks:
            # Each check can return multiple results if it has check_* methods
            check_results = check.run_all_checks()
            results.extend(check_results)
        return results


if __name__ == '__main__':
    # You can use either approach:
    # 1. New multi-check pattern: One service class with multiple check methods
    # 2. Old single-check pattern: One check class per service

    # Example using the new multi-check pattern:
    checks = [
        BookreaderService(),  # This will run check_yearbooks() and check_yellbooks()
        CanvasService([
            (
                "[AustinMap](https://spotlight.library.tamu.edu/spotlight/austin-map/catalog/749b8d795ee38de0e9211b9fd04a3075)",
                "https://api.library.tamu.edu/iiif-service/dspace/presentation/1969.1/169475/25/SFA_Map_600ppi.jpg"
            ),
            (

            )
            # Add more items here as needed:
            # ("ItemName", "https://api.url.here"),
        ]),
    ]

    # Or use the old way (backward compatible):
    # checks = [
    #     BookreaderCheck(),
    #     YellBooksCheck(),
    #     CanvasCheck(),
    # ]

    runner = CheckRunner(checks)
    results = runner.run()

    with open("status.md", "w") as f:
        f.write("# Service Status\n\n")
        f.write(f"**Last Updated**: {datetime.datetime.now(datetime.UTC)} UTC\n\n")
        f.write(f"## Services Checked:\n\n")
        for name, status in results:
            icon = "🟢 UP" if status else "🔴 DOWN"
            f.write(f"- **{name}**: {icon}\n")