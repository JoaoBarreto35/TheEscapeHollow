import pygame
from code.editor.interface import desenhar_interface
from code.editor.eventos import processar_eventos
from code.editor.mapa import carregar_mapa
from code.editor.constantes import (
    TILE_SIZE, GRID_LINHAS, GRID_COLUNAS, PAINEL_LATERAL,
    CAMINHO_MAPA_TEMPLATE
)

def run_editor():
    pygame.init()

    # Carrega o mapa base
    mapa = carregar_mapa(CAMINHO_MAPA_TEMPLATE)

    # Tamanho da janela
    screen_width = GRID_COLUNAS * TILE_SIZE + PAINEL_LATERAL
    screen_height = GRID_LINHAS * TILE_SIZE
    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Editor de Mapas - Tela Preta")

    # Inicializações
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont(None, 24)

    # Estado do editor
    simbolo_selecionado = None
    movendo_simbolo = None
    old_move_l = -1
    old_move_c = -1
    trigger_selecionado = None
    Triggers = {}
    trigger_expandidos = {}
    botoes_simbolos = []
    running = True

    while running:
        dt = clock.tick(60)
        eventos = pygame.event.get()

        # Desenha interface e obtém botões
        botoes_simbolos, botao_salvar_rect = desenhar_interface(
            window, mapa, Triggers, trigger_selecionado, trigger_expandidos,
            simbolo_selecionado, movendo_simbolo, old_move_l, old_move_c,
            TILE_SIZE, GRID_LINHAS, GRID_COLUNAS, PAINEL_LATERAL, fonte
        )

        # Monta contexto para eventos
        contexto = {
            "mapa": mapa,
            "Triggers": Triggers,
            "trigger_selecionado": trigger_selecionado,
            "simbolo_selecionado": simbolo_selecionado,
            "movendo_simbolo": movendo_simbolo,
            "old_move_l": old_move_l,
            "old_move_c": old_move_c,
            "botoes_simbolos": botoes_simbolos,
            "botao_salvar_rect": botao_salvar_rect,
            "trigger_expandidos": trigger_expandidos,
            "tile_size": TILE_SIZE,
            "grid_colunas": GRID_COLUNAS,
            "grid_linhas": GRID_LINHAS,
            "running": running
        }

        # Processa eventos
        for event in eventos:
            processar_eventos(event, contexto)

        # Atualiza estado
        mapa = contexto["mapa"]
        Triggers = contexto["Triggers"]
        trigger_selecionado = contexto["trigger_selecionado"]
        simbolo_selecionado = contexto["simbolo_selecionado"]
        movendo_simbolo = contexto["movendo_simbolo"]
        old_move_l = contexto["old_move_l"]
        old_move_c = contexto["old_move_c"]
        trigger_expandidos = contexto["trigger_expandidos"]
        running = contexto["running"]

    pygame.quit()