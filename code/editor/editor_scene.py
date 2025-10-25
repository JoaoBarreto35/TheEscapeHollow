import pygame
from code.editor.interface import desenhar_interface
from code.editor.eventos import processar_eventos
from code.editor.salvar import salvar_nivel

def run_editor(mapa, indice=None, triggers=None, name=None, hint=None):
    pygame.init()

    from code.editor.constantes import TILE_SIZE, GRID_LINHAS, GRID_COLUNAS, PAINEL_LATERAL
    print("Triggers recebidos:")
    for k, v in triggers.items():
        print(f"{k} → {v}")
    screen_width = GRID_COLUNAS * TILE_SIZE + PAINEL_LATERAL
    screen_height = GRID_LINHAS * TILE_SIZE
    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Editor de Mapas")

    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont(None, 24)

    # Estado inicial
    contexto = {
        "mapa": mapa,
        "Triggers": triggers if triggers else {},
        "trigger_selecionado": None,
        "simbolo_selecionado": None,
        "movendo_simbolo": None,
        "old_move_l": -1,
        "old_move_c": -1,
        "trigger_expandidos": {},
        "tile_size": TILE_SIZE,
        "grid_colunas": GRID_COLUNAS,
        "grid_linhas": GRID_LINHAS,
        "painel_lateral": PAINEL_LATERAL,
        "running": True,
        "salvar_nivel": False,
        "nome_nivel": name,
        "dica_nivel": hint,
        "editando_nome": False,
        "editando_dica": False
    }

    while contexto["running"]:
        dt = clock.tick(60)
        eventos = pygame.event.get()

        botoes_simbolos, botao_salvar_rect = desenhar_interface(window, contexto, fonte)
        contexto["botoes_simbolos"] = botoes_simbolos
        contexto["botao_salvar_rect"] = botao_salvar_rect

        for event in eventos:
            processar_eventos(event, contexto)

            # ESC para sair
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                contexto["running"] = False
            if event.type == pygame.MOUSEWHEEL:
                contexto["scroll_offset"] = max(0, contexto.get("scroll_offset", 0) - event.y * 40)

        # Salvar nível
        if contexto["salvar_nivel"]:
            salvar_nivel(
                contexto["mapa"],
                contexto["Triggers"],
                contexto["nome_nivel"],
                contexto["dica_nivel"],
                indice
            )
            contexto["salvar_nivel"] = False

    return  # Não encerra pygame aqui para permitir retorno à tela de seleção