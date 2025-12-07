from service_checks import BookreaderCheck, YellBooksCheck
import datetime


class CheckRunner:
    def __init__(self, checks):
        self.checks = checks

    def run(self):
        results = []
        for check in self.checks:
            status = check.check()
            results.append((check.name, status))
        return results


if __name__ == '__main__':
    checks = [
        BookreaderCheck(),
        YellBooksCheck(),
    ]
    runner = CheckRunner(checks)
    results = runner.run()

    with open("status.md", "w") as f:
        f.write("# Service Status\n\n")
        f.write(f"**Last Updated**: {datetime.datetime.now(datetime.UTC)} UTC\n\n")
        f.write(f"## Services Checked:\n\n")
        for name, status in results:
            icon = "🟢 UP" if status else "🔴 DOWN"
            f.write(f"- **{name}**: {icon}\n")