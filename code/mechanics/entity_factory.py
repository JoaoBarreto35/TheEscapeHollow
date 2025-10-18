from typing import Tuple, Optional
from code.entities.player import Player
from code.entities.pushable_rock import PushableRock
from code.entities.enemy import Enemy
from code.entities.life_chest import LifeChest
from code.entities.level_exit import LevelExit

class EntityFactory:
    def __init__(self, tile_size: int):
        """
        Inicializa a fábrica de entidades com o tamanho padrão de tile.
        Esse tamanho será usado para dimensionar entidades visuais como rochas, baús e saídas.
        """
        self.tile_size = tile_size

    def create_entity(self, symbol: str, position: Tuple[int, int]) -> Optional[object]:
        """
        Cria uma instância de entidade com base no símbolo do mapa.
        Cada símbolo representa um tipo específico de entidade no jogo.

        :param symbol: caractere que representa a entidade no mapa (ex: 'P' para jogador)
        :param position: posição inicial da entidade no mapa
        :return: instância da entidade correspondente ou None se o símbolo não for reconhecido
        """

        # Jogador
        if symbol == "P":
            return Player(position, scale=2)

        # Rocha empurrável
        elif symbol == "R":
            return PushableRock(position, size=self.tile_size - 5)

        # Inimigo com patrulha horizontal
        elif symbol == "H":
            return Enemy(position, scale=2, patrol_axis="H")

        # Inimigo com patrulha vertical
        elif symbol == "V":
            return Enemy(position, scale=2, patrol_axis="V")

        # Saída do nível (porta de saída)
        elif symbol == "X":
            return LevelExit(position, tile_size=self.tile_size)

        # Baú de vida (concede coração ao abrir)
        elif symbol == "C":
            return LifeChest(position, tile_size=self.tile_size)

        # Símbolo desconhecido — nenhuma entidade criada
        return None