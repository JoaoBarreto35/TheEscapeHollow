# eventos.py
import pygame
from code.editor.salvar import salvar_nivel
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

    if event.type == pygame.QUIT:
        contexto["running"] = False

    elif event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos

        if botao_salvar_rect and botao_salvar_rect.collidepoint(x, y):
            salvar_nivel(mapa, Triggers, "sem_nome", "sem_hint")

        if event.button == 1:  # Clique esquerdo
            if x < grid_colunas * tile_size:
                coluna = x // tile_size
                linha = y // tile_size
                pos = (linha, coluna)

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

            else:
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

        elif event.button == 3:  # Clique direito
            if x < grid_colunas * tile_size:
                coluna = x // tile_size
                linha = y // tile_size
                pos = (linha, coluna)

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