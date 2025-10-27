# D - Death Reasons
class DeathReason:
    ENEMY = "enemy"
    HOLE = "hole"
    TRAP = "trap"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"
    SPIKE = "spike"

#E
ENEMY_SPEED = 2.5

#M
class MapSymbol:
    ENEMY_HORIZONTAL = "H"
    ENEMY_VERTICAL = "V"
    FLOOR = "."
    HOLE_TRAP = "T"
    LEVEL_EXIT = "X"
    LIFE_CHEST = "C"
    PLAYER = "P"
    PRESSURE_PLATE = "L"
    PUSHABLE_ROCK = "R"
    SECRET_DOOR = "S"
    WALL = "W"
    SOUND_SENSOR = "@"
    SPIKES = "Y"
    SPIKES_TRAP = "y"

# P
PLAYER_NORMAL_SPEED = 2
PLAYER_PUSHING_SPEED = 0.5

# R
ROCK_PUSH_SPEED = 2.1

# S

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 320
SOUND_SENSOR_RAIO_TILES = 1.7

#T

TIME_SECRET_DOOR = 2000
TIME_HOLE_TRAP = 100

TYPES= {
    MapSymbol.ENEMY_HORIZONTAL : "Entity",
    MapSymbol.ENEMY_VERTICAL : "Entity",
    MapSymbol.FLOOR : "Map",
    MapSymbol.HOLE_TRAP : "Target",
    MapSymbol.LEVEL_EXIT : "Entity",
    MapSymbol.LIFE_CHEST : "Entity",
    MapSymbol.PLAYER : "Entity",
    MapSymbol.PRESSURE_PLATE : "Trigger",
    MapSymbol.PUSHABLE_ROCK : "Entity",
    MapSymbol.SECRET_DOOR : "Target",
    MapSymbol.WALL : "Map",
    MapSymbol.SOUND_SENSOR : "Trigger",
    MapSymbol.SPIKES : "Target",
    MapSymbol.SPIKES_TRAP : "Target",}

