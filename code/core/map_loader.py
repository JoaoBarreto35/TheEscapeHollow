import os
import json
from code.core.map import Map  # Certifique-se de que a classe Map está acessível

class MapLoader:
    def __init__(self, maps_path="assets/maps"):
        self.maps_path = maps_path

    def load(self, level_id: str) -> Map:
        """Carrega todos os dados de um nível e retorna um objeto Map."""
        level_index = int(level_id.split("_")[1])
        grid = self.load_grid(level_id)
        events = self.load_events(level_id)
        name = self.load_names()[level_index]
        hint = self.load_hints()[level_index]
        return Map(name, hint, grid, events)

    def list_levels(self) -> list[str]:
        return sorted([
            filename.replace(".txt", "")
            for filename in os.listdir(self.maps_path)
            if filename.startswith("level_") and filename.endswith(".txt")
        ])

    def load_grid(self, level_id: str) -> list[list[str]]:
        """Carrega a grade de símbolos do mapa a partir do arquivo .txt."""
        path = os.path.join(self.maps_path, f"{level_id}.txt")
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        return [list(line.strip()) for line in lines]

    def load_events(self, level_id: str) -> list[dict]:
        """Carrega os eventos (gatilhos e alvos) do mapa a partir do events.json."""
        path = os.path.join(self.maps_path, "events.json")
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data.get(level_id, [])

    def load_names(self) -> list[str]:
        """Carrega os nomes de todos os níveis a partir do names.json."""
        path = os.path.join(self.maps_path, "names.json")
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def load_hints(self) -> list[str]:
        """Carrega as dicas de todos os níveis a partir do hints.json."""
        path = os.path.join(self.maps_path, "hints.json")
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)