# mapa.py

def carregar_mapa(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()
        mapa = [list(linha.strip()) for linha in linhas]
    return mapa

def salvar_mapa(mapa, caminho):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        for linha in mapa:
            arquivo.write("".join(linha) + "\n")