# constantes.py

# Tamanho dos tiles e da grade
TILE_SIZE = 32
GRID_LINHAS = 17
GRID_COLUNAS = 17

# Tamanho do painel lateral
PAINEL_LATERAL = 600

# Cores padrão (RGB)
COR_FUNDO_GRADE = (20, 20, 20)
COR_GRADE = (80, 80, 80)
COR_TRIGGER = (200, 220, 180)
COR_TRIGGER_SELECIONADO = (255, 255, 100)
COR_TARGET = (250, 250, 250)
COR_TRIGGER_ATIVO = (0, 120, 255)
COR_MOVENDO = (255, 0, 0)
COR_PAINEL = (30, 30, 30)
COR_BOTAO = (180, 180, 180)
COR_BOTAO_SELECIONADO = (255, 255, 255)
COR_SALVAR = (0, 180, 0)

# Caminhos de arquivos
CAMINHO_MAPA_TEMPLATE = "assets/maps/template.txt"
CAMINHO_EVENTS = "assets/maps/events.json"
CAMINHO_NAMES = "assets/maps/names.json"
CAMINHO_HINTS = "assets/maps/hints.json"

# Símbolos protegidos (não podem ser apagados)
SIMBOLOS_PROTEGIDOS = ("P", "X", ".")