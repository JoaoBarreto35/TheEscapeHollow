import pygame
from code.editor.salvar import remover_nivel
from code.editor.selecao_nivel_utils import listar_niveis, start_editor

def tela_selecao():
    pygame.init()
    largura = 800
    altura = 800
    painel_lateral = 200
    window = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Seleção de Mapas")

    fonte = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()

    niveis = listar_niveis()
    indice_selecionado = None
    running = True

    while running:
        window.fill((10, 10, 10))
        eventos = pygame.event.get()

        # Lista de níveis
        for i, (indice, nome, dica) in enumerate(niveis):
            y = 30 + i * 40
            cor = (255, 255, 100) if indice == indice_selecionado else (200, 200, 200)
            texto = fonte.render(f"{indice}: {nome} - {dica}", True, cor)
            window.blit(texto, (20, y))

        # Painel lateral
        pygame.draw.rect(window, (30, 30, 30), (largura - painel_lateral, 0, painel_lateral, altura))

        botoes = [
            ("Novo", (largura - painel_lateral + 20, 100, 160, 40)),
            ("Editar", (largura - painel_lateral + 20, 160, 160, 40)),
            ("Apagar", (largura - painel_lateral + 20, 220, 160, 40)),
        ]

        for nome, (x, y, w, h) in botoes:
            pygame.draw.rect(window, (80, 80, 80), (x, y, w, h))
            texto = fonte.render(nome, True, (255, 255, 255))
            window.blit(texto, (x + 10, y + 10))

        pygame.display.update()
        clock.tick(60)

        for event in eventos:
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Seleção de nível
                for i, (indice, _, _) in enumerate(niveis):
                    item_y = 30 + i * 40
                    if 20 <= x <= largura - painel_lateral and item_y <= y <= item_y + 30:
                        indice_selecionado = indice

                # Clique em botões
                for nome, (bx, by, bw, bh) in botoes:
                    if bx <= x <= bx + bw and by <= y <= by + bh:
                        if nome == "Novo":
                            start_editor(None)
                            niveis = listar_niveis()
                        elif nome == "Editar" and indice_selecionado is not None:
                            start_editor(indice_selecionado)
                            niveis = listar_niveis()
                        elif nome == "Apagar" and indice_selecionado is not None:
                            remover_nivel(indice_selecionado)
                            indice_selecionado = None
                            niveis = listar_niveis()

    return "menu"