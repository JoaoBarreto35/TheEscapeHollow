import pygame
from code.settings import TYPES  # ajuste o caminho conforme seu projeto

def processar_eventos(event, contexto):
    mapa = contexto["mapa"]
    Triggers = contexto["Triggers"]
    trigger_selecionado = contexto["trigger_selecionado"]
    simbolo_selecionado = contexto["simbolo_selecionado"]
    movendo_simbolo = contexto["movendo_simbolo"]
    old_move_l = contexto["old_move_l"]
    old_move_c = contexto["old_move_c"]
    botoes_simbolos = contexto["botoes_simbolos"]
    botao_salvar_rect = contexto["botao_salvar_rect"]
    trigger_expandidos = contexto["trigger_expandidos"]
    tile_size = contexto["tile_size"]
    grid_colunas = contexto["grid_colunas"]
    grid_linhas = contexto["grid_linhas"]

    # Fecha o editor
    if event.type == pygame.QUIT:
        contexto["running"] = False

    # Clique do mouse
    elif event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        painel_x = grid_colunas * tile_size

        # Verifica clique no campo de nome
        if painel_x + 10 <= x <= painel_x + 260 and 10 <= y <= 40:
            contexto["editando_nome"] = True
            contexto["editando_dica"] = False
            return

        # Verifica clique no campo de dica
        if painel_x + 10 <= x <= painel_x + 260 and 50 <= y <= 80:
            contexto["editando_dica"] = True
            contexto["editando_nome"] = False
            return

        # Botão salvar
        if botao_salvar_rect and botao_salvar_rect.collidepoint(x, y):
            contexto["salvar_nivel"] = True

        # Clique dentro do mapa
        if x < grid_colunas * tile_size:
            coluna = x // tile_size
            linha = y // tile_size
            pos = (linha, coluna)

            if event.button == 1:  # Clique esquerdo
                if trigger_selecionado:
                    if TYPES.get(mapa[linha][coluna]) == "Target":
                        if pos not in Triggers[trigger_selecionado]:
                            Triggers[trigger_selecionado].append(pos)
                            print(f"Adicionado target {pos} ao trigger {trigger_selecionado}")
                        else:
                            print(f"Target {pos} já está vinculado ao trigger {trigger_selecionado}")
                    else:
                        print(f"A célula {pos} não é um target válido")
                    contexto["trigger_selecionado"] = None
                    return

                if simbolo_selecionado:
                    if mapa[linha][coluna] == ".":
                        mapa[linha][coluna] = simbolo_selecionado
                        print(f"Pintou ({linha}, {coluna}) com '{simbolo_selecionado}'")
                        if TYPES[simbolo_selecionado] == "Trigger":
                            Triggers.setdefault((linha, coluna), [])
                    elif TYPES[simbolo_selecionado] == "Trigger" and TYPES[mapa[linha][coluna]] == "Target":
                        Triggers[(linha, coluna)] = True
                else:
                    if movendo_simbolo and mapa[linha][coluna] == ".":
                        mapa[linha][coluna] = movendo_simbolo
                        mapa[old_move_l][old_move_c] = "."

                        origem = (old_move_l, old_move_c)
                        destino = (linha, coluna)

                        if origem in Triggers:
                            Triggers[destino] = Triggers.pop(origem)
                            print(f"Trigger movido de {origem} para {destino}")

                        for trigger, targets in Triggers.items():
                            for i, t in enumerate(targets):
                                if t == origem:
                                    targets[i] = destino
                                    print(f"Target movido de {origem} para {destino} no trigger {trigger}")

                    if mapa[linha][coluna] != ".":
                        contexto["movendo_simbolo"] = mapa[linha][coluna]
                        contexto["old_move_l"] = linha
                        contexto["old_move_c"] = coluna

            elif event.button == 3:  # Clique direito
                for trigger, targets in Triggers.items():
                    if pos in targets:
                        targets.remove(pos)
                        print(f"Target {pos} removido do trigger {trigger}")

                if pos in Triggers:
                    del Triggers[pos]
                    print(f"Trigger {pos} removido completamente")

                if mapa[linha][coluna] not in ("P", "X"):
                    mapa[linha][coluna] = "."
                    print(f"Apagou célula ({linha}, {coluna})")

        # Clique na interface lateral
        else:
            if event.button == 1:
                for nome, valor, rect in botoes_simbolos:
                    if simbolo_selecionado == valor:
                        contexto["simbolo_selecionado"] = None
                        contexto["movendo_simbolo"] = None
                    elif rect.collidepoint(x, y):
                        contexto["old_move_l"] = -1
                        contexto["old_move_c"] = -1
                        contexto["movendo_simbolo"] = None
                        contexto["trigger_selecionado"] = None
                        contexto["simbolo_selecionado"] = valor
                        print(f"Selecionado: {nome} → símbolo '{valor}'")

                y_offset = 20
                for trigger, targets in Triggers.items():
                    rect_trigger = pygame.Rect(grid_colunas * tile_size + 300, y_offset, 160, 32)
                    if rect_trigger.collidepoint(x, y):
                        trigger_expandidos[trigger] = not trigger_expandidos.get(trigger, False)
                        contexto["trigger_selecionado"] = trigger if trigger_expandidos[trigger] else None
                        contexto["simbolo_selecionado"] = None
                        contexto["movendo_simbolo"] = None
                        print(f"Trigger {trigger} {'expandido' if trigger_expandidos[trigger] else 'recolhido'}")
                    y_offset += 32 + len(targets) * 24 if trigger_expandidos.get(trigger, False) else 40
    elif event.type == pygame.KEYDOWN:
        if contexto.get("editando_nome"):
            if event.key == pygame.K_BACKSPACE:
                contexto["nome_nivel"] = contexto["nome_nivel"][:-1]
            elif event.key == pygame.K_RETURN:
                contexto["editando_nome"] = False
            elif event.unicode.isprintable():
                contexto["nome_nivel"] += event.unicode

        elif contexto.get("editando_dica"):
            if event.key == pygame.K_BACKSPACE:
                contexto["dica_nivel"] = contexto["dica_nivel"][:-1]
            elif event.key == pygame.K_RETURN:
                contexto["editando_dica"] = False
            elif event.unicode.isprintable():
                contexto["dica_nivel"] += event.unicode