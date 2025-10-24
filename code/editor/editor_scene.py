import pygame
import inspect
from code.settings import MapSymbol, TYPES  # Define os símbolos e seus tipos
import json
import os

def salvar_nivel(mapa, triggers, nome_nivel, dica_nivel):
    # Caminhos dos arquivos
    pasta_mapas = "assets/maps"
    caminho_events = "assets/maps/events.json"
    caminho_names = "assets/maps/names.json"
    caminho_hints = "assets/maps/hints.json"

    # Carrega os arquivos existentes
    with open(caminho_events, "r", encoding="utf-8") as f:
        eventos = json.load(f)
    with open(caminho_names, "r", encoding="utf-8") as f:
        nomes = json.load(f)
    with open(caminho_hints, "r", encoding="utf-8") as f:
        dicas = json.load(f)

    # Determina o próximo índice de nível
    proximo_indice = len(eventos)
    nome_nivel_id = f"level_{proximo_indice}"

    # Salva o mapa como .txt
    caminho_mapa = os.path.join(pasta_mapas, f"level_{proximo_indice}.txt")
    with open(caminho_mapa, "w", encoding="utf-8") as f:
        for linha in mapa:
            f.write("".join(linha) + "\n")

    # Converte triggers para estrutura do events.json
    lista_eventos = []
    for trigger, targets in triggers.items():
        evento = {
            "trigger": [trigger[0], trigger[1]],
            "targets": [[t[0], t[1]] for t in targets]
        }
        lista_eventos.append(evento)

    # Atualiza os arquivos JSON
    eventos[nome_nivel_id] = lista_eventos
    nomes.append(nome_nivel)
    dicas.append(dica_nivel)

    # Salva os arquivos atualizados
    with open(caminho_events, "w", encoding="utf-8") as f:
        json.dump(eventos, f, indent=2, ensure_ascii=False)
    with open(caminho_names, "w", encoding="utf-8") as f:
        json.dump(nomes, f, indent=2, ensure_ascii=False)
    with open(caminho_hints, "w", encoding="utf-8") as f:
        json.dump(dicas, f, indent=2, ensure_ascii=False)

    print(f"✅ Nível {nome_nivel_id} salvo com sucesso!")

# Função para listar os símbolos disponíveis na classe MapSymbol
def listar_simbolos():
    simbolos = []
    for nome, valor in inspect.getmembers(MapSymbol):
        if not nome.startswith("__") and isinstance(valor, str):
            simbolos.append((nome, valor))
    return simbolos

# Função para carregar o mapa a partir de um arquivo
def carregar_mapa(caminho):
    with open(caminho, "r") as arquivo:
        linhas = arquivo.readlines()
        mapa = [list(linha.strip()) for linha in linhas]
    return mapa

# Função principal do editor
def run_editor():
    pygame.init()

    # Configurações da grade
    tile_size = 32
    grid_linhas = 17
    grid_colunas = 17
    mapa = carregar_mapa("assets/maps/template.txt")

    # Tamanho da janela
    painel_lateral = 600
    screen_width = grid_colunas * tile_size + painel_lateral
    screen_height = grid_linhas * tile_size

    # Criação da janela
    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Editor de Mapas - Tela Preta")

    # Inicializações
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont(None, 24)

    simbolo_selecionado = None
    movendo_simbolo = None
    old_move_l = -1
    old_move_c = -1
    trigger_selecionado = None

    Triggers = {}  # Dicionário de triggers e seus targets
    trigger_expandidos = {}  # ← NOVO: controla quais triggers estão expandidos
    botoes_simbolos = []

    running = True
    while running:
        dt = clock.tick(60)
        eventos = pygame.event.get()

        # Processamento de eventos
        for event in eventos:
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Clique no botão SALVAR

                x, y = event.pos
                if botao_salvar_rect.collidepoint(x, y):
                    salvar_nivel(mapa, Triggers, "sem_nome", "sem_hint")

                if event.button == 1:  # Clique esquerdo
                    if x < grid_colunas * tile_size:
                        coluna = x // tile_size
                        linha = y // tile_size
                        pos = (linha, coluna)

                        # Se um trigger estiver selecionado, adiciona target
                        if trigger_selecionado:
                            if TYPES.get(mapa[linha][coluna]) == "Target":
                                if pos not in Triggers[trigger_selecionado]:
                                    Triggers[trigger_selecionado].append(pos)
                                    print(f"Adicionado target {pos} ao trigger {trigger_selecionado}")
                                else:
                                    print(f"Target {pos} já está vinculado ao trigger {trigger_selecionado}")
                            else:
                                print(f"A célula {pos} não é um target válido")
                            trigger_selecionado = None
                            continue

                        # Pintar símbolo na grade
                        if simbolo_selecionado:
                            if mapa[linha][coluna] == ".":
                                mapa[linha][coluna] = simbolo_selecionado
                                print(f"Pintou ({linha}, {coluna}) com '{simbolo_selecionado}'")
                                if TYPES[simbolo_selecionado] == "Trigger":
                                    Triggers.setdefault((linha, coluna), [])
                            elif TYPES[simbolo_selecionado] == "Trigger" and TYPES[mapa[linha][coluna]] == "Target":
                                Triggers[(linha, coluna)] = True
                        else:
                            # Mover símbolo

                            if movendo_simbolo and mapa[linha][coluna] == ".":
                                # Atualiza mapa visual
                                mapa[linha][coluna] = movendo_simbolo
                                mapa[old_move_l][old_move_c] = "."

                                origem = (old_move_l, old_move_c)
                                destino = (linha, coluna)

                                # 🔁 Se era um trigger, atualiza a chave no dicionário
                                if origem in Triggers:
                                    Triggers[destino] = Triggers.pop(origem)
                                    print(f"Trigger movido de {origem} para {destino}")

                                # 🔁 Se era um target, atualiza nas listas de todos os triggers
                                for trigger, targets in Triggers.items():
                                    for i, t in enumerate(targets):
                                        if t == origem:
                                            targets[i] = destino
                                            print(f"Target movido de {origem} para {destino} no trigger {trigger}")


                            if mapa[linha][coluna] != ".":
                                movendo_simbolo = mapa[linha][coluna]
                                old_move_l = linha
                                old_move_c = coluna
                    else:
                        # Clique em botão de símbolo
                        for nome, valor, rect in botoes_simbolos:
                            if simbolo_selecionado == valor:
                                simbolo_selecionado = None
                                movendo_simbolo = None
                            else:
                                if rect.collidepoint(x, y):
                                    old_move_l = -1
                                    old_move_c = -1
                                    movendo_simbolo = None
                                    trigger_selecionado = None
                                    simbolo_selecionado = valor
                                    print(f"Selecionado: {nome} → símbolo '{valor}'")

                        # Clique em botão de trigger no painel lateral
                        y_offset = 20
                        for trigger, targets in Triggers.items():
                            rect_trigger = pygame.Rect(grid_colunas * tile_size + 300, y_offset, 160, 32)
                            if rect_trigger.collidepoint(x, y):
                                # Alterna expansão
                                trigger_expandidos[trigger] = not trigger_expandidos.get(trigger, False)
                                trigger_selecionado = trigger if trigger_expandidos[trigger] else None
                                simbolo_selecionado = None
                                movendo_simbolo = None
                                print(f"Trigger {trigger} {'expandido' if trigger_expandidos[trigger] else 'recolhido'}")
                            # Atualiza y_offset com base na expansão
                            if trigger_expandidos.get(trigger, False):
                                y_offset += 32 + len(targets) * 24
                            else:
                                y_offset += 40


                elif event.button == 3:  # Clique direito

                    if x < grid_colunas * tile_size:
                        coluna = x // tile_size
                        linha = y // tile_size
                        pos = (linha, coluna)

                        # Verifica se é um target de algum trigger
                        for trigger, targets in Triggers.items():
                            if pos in targets:
                                targets.remove(pos)
                                print(f"Target {pos} removido do trigger {trigger}")

                        #Remover como trigger principal
                        if pos in Triggers:
                            del Triggers[pos]
                            print(f"Trigger {pos} removido completamente")

                        # Se não era target, apaga normalmente
                        if mapa[linha][coluna] not in ("P", "X"):
                            mapa[linha][coluna] = "."
                            print(f"Apagou célula ({linha}, {coluna})")

        # Desenha fundo
        window.fill((0, 0, 0))

        # Desenha grade
        for linha in range(grid_linhas):
            for coluna in range(grid_colunas):
                x = coluna * tile_size
                y = linha * tile_size
                simbolo = mapa[linha][coluna]

                # 🔍 Verifica se é a célula do trigger selecionado
                if (linha, coluna) == trigger_selecionado:
                    cor_fundo = (0, 120, 255)  # azul claro para destaque
                elif (linha, coluna) == (old_move_l, old_move_c):
                    cor_fundo = (255, 0, 0)  # vermelho para símbolo em movimento
                else:
                    cor_fundo = (20, 20, 20)  # cor padrão
                pygame.draw.rect(window, cor_fundo, (x, y, tile_size, tile_size))
                pygame.draw.rect(window, (80, 80, 80), (x, y, tile_size, tile_size), 1)

                if simbolo != ".":
                    texto = fonte.render(simbolo, True, (255, 255, 255))
                    texto_rect = texto.get_rect(center=(x + tile_size // 2, y + tile_size // 2))
                    window.blit(texto, texto_rect)

        # Painel lateral
        painel_x = grid_colunas * tile_size
        pygame.draw.rect(window, (30, 30, 30), (painel_x, 0, painel_lateral, screen_height))

        # Botões de símbolos
        botoes_simbolos.clear()
        simbolos = listar_simbolos()
        linha_visivel = 0

        for i, (nome, valor) in enumerate(simbolos):
            if valor not in ("P", "X", "."):
                linha_visivel += 1
                botao_y = 20 + linha_visivel * 40
                botao_rect = pygame.Rect(painel_x + 10, botao_y, 250, 32)
                cor = (255, 255, 255) if valor == simbolo_selecionado else (180, 180, 180)
                pygame.draw.rect(window, cor, botao_rect, 1)
                texto = fonte.render(f'{valor} - {nome}', True, cor)
                window.blit(texto, (botao_rect.x + 10, botao_rect.y + 5))
                botoes_simbolos.append((nome, valor, botao_rect))

        # Triggers e targets com expansão
        y_offset = 20
        for trigger, targets in Triggers.items():
            # Botão do trigger
            rect_trigger = pygame.Rect(painel_x + 300, y_offset, 160, 32)
            # 🔍 Verifica se é o trigger selecionado
            if trigger == trigger_selecionado:
                cor_trigger = (255, 255, 100)  # amarelo claro para destaque

            else:
                cor_trigger = (200, 220, 180)  # cor padrão
            pygame.draw.rect(window, cor_trigger, rect_trigger)
            texto_trigger = fonte.render(f"{mapa[trigger[0]][trigger[1]]} {trigger}", True, (0, 0, 0))
            window.blit(texto_trigger, (rect_trigger.x + 5, rect_trigger.y + 5))

            # Targets se estiver expandido
            if trigger_expandidos.get(trigger, False):
                for j, target in enumerate(targets):
                    y_target = y_offset + 32 + j * 24
                    texto_target = fonte.render(f"{mapa[target[0]][target[1]]} {target}", True, (250, 250, 250))
                    window.blit(texto_target, (painel_x + 310, y_target))
                y_offset += 32 + len(targets) * 24
            else:
                y_offset += 40  # espaço padrão se não estiver expandido


            #desenhando a linha entre target e trigger
            x1 = trigger[1] * tile_size + tile_size // 2
            y1 = trigger[0] * tile_size + tile_size // 2

            for target in targets:
                x2 = target[1] * tile_size + tile_size // 2
                y2 = target[0] * tile_size + tile_size // 2

                pygame.draw.line(window, (0, 255, 0), (x1, y1), (x2, y2), 2)  # linha verde
        # Botão SALVAR
        botao_salvar_rect = pygame.Rect(painel_x + 10, screen_height - 60, 250, 40)
        pygame.draw.rect(window, (0, 180, 0), botao_salvar_rect)
        texto_salvar = fonte.render("💾 Salvar Nível", True, (255, 255, 255))
        window.blit(texto_salvar, (botao_salvar_rect.x + 10, botao_salvar_rect.y + 10))


        pygame.display.update()

    pygame.quit()