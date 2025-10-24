class Map:
    def __init__(self, name: str, hint: str, grid: list[list[str]], events: list[dict]):
        self.name = name              # Nome da fase
        self.hint = hint              # Dica da fase
        self.grid = grid              # Matriz de símbolos (tiles e entidades)
        self.events = events          # Lista de triggers e seus alvos

    def get_tile(self, x: int, y: int) -> str:
        """Retorna o símbolo do tile na posição (x, y)."""
        return self.grid[y][x]

    def get_trigger_targets(self, trigger_pos: tuple[int, int]) -> list[tuple[int, int]]:
        """Retorna os alvos associados a um trigger."""
        for event in self.events:
            if tuple(event["trigger"]) == trigger_pos:
                return event["targets"]
        return []