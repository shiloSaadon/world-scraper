class ScraperQuery:
    def __init__(self, id: int, value: str):
        self.id = id
        self.value = value

    def __str__(self) -> str:
        return f"ScraperQuery -> ID: {self.id}, Value: {self.value}"
