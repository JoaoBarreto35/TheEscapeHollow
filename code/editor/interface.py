import inspect
import pygame
from code.settings import MapSymbol

def listar_simbolos():
    return [
        (nome, valor)
        for nome, valor in inspect.getmembers(MapSymbol)
        if not nome.startswith("__") and isinstance(valor, str)
    ]

def desenhar_interface(window, contexto, fonte):
    # 🔧 Dados do contexto
    mapa = contexto["mapa"]
    Triggers = contexto["Triggers"]
    trigger_selecionado = contexto["trigger_selecionado"]
    trigger_expandidos = contexto["trigger_expandidos"]
    simbolo_selecionado = contexto["simbolo_selecionado"]
    movendo_simbolo = contexto["movendo_simbolo"]
    old_move_l = contexto["old_move_l"]
    old_move_c = contexto["old_move_c"]
    tile_size = contexto["tile_size"]
    grid_linhas = contexto["grid_linhas"]
    grid_colunas = contexto["grid_colunas"]
    painel_lateral = contexto["painel_lateral"]
    scroll_offset = contexto.get("scroll_offset", 0)

    # 🎨 Fundo
    window.fill((0, 0, 0))

    # 🧱 Grade do mapa
    for linha in range(grid_linhas):
        for coluna in range(grid_colunas):
            x = coluna * tile_size
            y = linha * tile_size
            simbolo = mapa[linha][coluna]

            cor_fundo = (20, 20, 20)
            if (linha, coluna) == trigger_selecionado:
                cor_fundo = (0, 120, 255)
            elif (linha, coluna) == (old_move_l, old_move_c):
                cor_fundo = (255, 0, 0)

            pygame.draw.rect(window, cor_fundo, (x, y, tile_size, tile_size))
            pygame.draw.rect(window, (80, 80, 80), (x, y, tile_size, tile_size), 1)

            if simbolo != ".":
                try:
                    texto = fonte.render(str(simbolo), True, (255, 255, 255))
                    texto_rect = texto.get_rect(center=(x + tile_size // 2, y + tile_size // 2))
                    window.blit(texto, texto_rect)
                except Exception as e:
                    print(f"Erro ao renderizar símbolo: {simbolo} ({type(simbolo)}) → {e}")
                    continue

    # 📐 Painel lateral
    painel_x = grid_colunas * tile_size
    screen_height = grid_linhas * tile_size
    pygame.draw.rect(window, (30, 30, 30), (painel_x, 0, painel_lateral, screen_height))

    # ✏️ Campos de entrada
    nome_nivel = contexto.get("nome_nivel", "sem_nome")
    dica_nivel = contexto.get("dica_nivel", "sem_hint")
    editando_nome = contexto.get("editando_nome", False)
    editando_dica = contexto.get("editando_dica", False)

    campo_nome = pygame.Rect(painel_x + 10, 10, 250, 30)
    campo_dica = pygame.Rect(painel_x + 10, 50, 250, 30)

    pygame.draw.rect(window, (40, 40, 40), campo_nome)
    pygame.draw.rect(window, (40, 40, 40), campo_dica)
    pygame.draw.rect(window, (0, 200, 0) if editando_nome else (100, 100, 100), campo_nome, 2)
    pygame.draw.rect(window, (0, 200, 0) if editando_dica else (100, 100, 100), campo_dica, 2)

    texto_nome = fonte.render(f"Nome: {nome_nivel}", True, (255, 255, 255))
    texto_dica = fonte.render(f"Dica: {dica_nivel}", True, (255, 255, 255))
    window.blit(texto_nome, (campo_nome.x + 5, campo_nome.y + 5))
    window.blit(texto_dica, (campo_dica.x + 5, campo_dica.y + 5))

    # 🎛️ Botões de símbolos com scroll
    botoes_simbolos = []
    simbolos = listar_simbolos()
    linha_visivel = 0
    area_scroll = pygame.Rect(painel_x + 10, 100, 250, screen_height - 160)

    for nome, valor in simbolos:
        if valor in ("P", "X", "."):
            continue
        linha_visivel += 1
        botao_y = 100 + linha_visivel * 40 - scroll_offset

        if area_scroll.top <= botao_y <= area_scroll.bottom:
            botao_rect = pygame.Rect(painel_x + 10, botao_y, 250, 32)
            cor = (255, 255, 255) if valor == simbolo_selecionado else (180, 180, 180)
            pygame.draw.rect(window, cor, botao_rect, 1)
            texto = fonte.render(f'{valor} - {nome}', True, cor)
            window.blit(texto, (botao_rect.x + 10, botao_rect.y + 5))
            botoes_simbolos.append((nome, valor, botao_rect))

    # 🧩 Triggers e targets
    y_offset = 20
    for trigger, targets in Triggers.items():
        rect_trigger = pygame.Rect(painel_x + 300, y_offset, 160, 32)
        cor_trigger = (255, 255, 100) if trigger == trigger_selecionado else (200, 220, 180)
        pygame.draw.rect(window, cor_trigger, rect_trigger)
        texto_trigger = fonte.render(f"{mapa[trigger[0]][trigger[1]]} {trigger}", True, (0, 0, 0))
        window.blit(texto_trigger, (rect_trigger.x + 5, rect_trigger.y + 5))

        if trigger_expandidos.get(trigger, False):
            for j, target in enumerate(targets):
                y_target = y_offset + 32 + j * 24
                texto_target = fonte.render(f"{mapa[target[0]][target[1]]} {target}", True, (250, 250, 250))
                window.blit(texto_target, (painel_x + 310, y_target))
            y_offset += 32 + len(targets) * 24
        else:
            y_offset += 40

        # 🔗 Linhas entre trigger e targets
        x1 = trigger[1] * tile_size + tile_size // 2
        y1 = trigger[0] * tile_size + tile_size // 2
        for target in targets:
            x2 = target[1] * tile_size + tile_size // 2
            y2 = target[0] * tile_size + tile_size // 2
            pygame.draw.line(window, (0, 255, 0), (x1, y1), (x2, y2), 2)

    # 💾 Botão salvar
    botao_salvar_rect = pygame.Rect(painel_x + 10, screen_height - 60, 250, 40)
    pygame.draw.rect(window, (0, 180, 0), botao_salvar_rect)
    texto_salvar = fonte.render("💾 Salvar Nível", True, (255, 255, 255))
    window.blit(texto_salvar, (botao_salvar_rect.x + 10, botao_salvar_rect.y + 10))

    pygame.display.update()
    return botoes_simbolos, botao_salvar_rect