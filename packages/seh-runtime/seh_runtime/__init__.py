class Runtime:
    def __init__(self, name: str = "seh-runtime") -> None:
        self.name = name
        self.state: dict[str, object] = {}

    def set(self, key: str, value: object) -> None:
        self.state[key] = value

    def get(self, key: str, default: object | None = None) -> object | None:
        return self.state.get(key, default)
