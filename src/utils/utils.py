import platform


class ScraperQuery:
    def __init__(self, id: int, value: str):
        self.id = id
        self.value = value

    def __str__(self) -> str:
        return f"ScraperQuery -> ID: {self.id}, Value: {self.value}"


def get_os():
    system = platform.system().lower()
    if system == "darwin":
        return "mac"
    elif system == "windows":
        return "windows"
    elif system == "linux":
        return "linux"
    else:
        return "unknown"