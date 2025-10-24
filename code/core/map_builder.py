import pygame

from code.settings import MapSymbol


class MapBuilder:
    def __init__(self, tile_size, wall_path, floor_path):
        self.tile_size = tile_size

        self.wall = pygame.image.load(wall_path).convert()
        self.wall.set_colorkey(self.wall.get_at((0, 0)))
        self.wall = pygame.transform.scale(self.wall, (tile_size, tile_size))

        self.floor = pygame.image.load(floor_path).convert()
        self.floor.set_colorkey(self.floor.get_at((0, 0)))
        self.floor = pygame.transform.scale(self.floor, (tile_size, tile_size))



    def draw_map(self, surface, level_map):

        for row_index, row in enumerate(level_map):
            for col_index, cell in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size
                if cell == MapSymbol.WALL:
                    surface.blit(self.wall, (x, y))
                else:
                    surface.blit(self.floor, (x, y))


    def get_wall_rects(self, level_map):
        wall_rects = []
        for row_index, row in enumerate(level_map):
            for col_index, cell in enumerate(row):
                if cell == MapSymbol.WALL:
                    x = col_index * self.tile_size
                    y = row_index * self.tile_size
                    wall_rects.append(pygame.Rect(x, y, self.tile_size, self.tile_size))
        return wall_rects