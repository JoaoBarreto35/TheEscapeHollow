# mapa.py

def carregar_mapa(caminho):
    import os, json

    with open(caminho, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()
        mapa = [list(linha.strip()) for linha in linhas]

    # Extrai índice do nome do arquivo
    base = os.path.basename(caminho)
    indice = int(base.split("_")[1].split(".")[0])

    # Caminhos dos arquivos auxiliares
    pasta = os.path.dirname(caminho)
    caminho_events = os.path.join(pasta, "events.json")
    caminho_names = os.path.join(pasta, "names.json")
    caminho_hints = os.path.join(pasta, "hints.json")

    # Carrega triggers
    triggers = {}
    try:
        with open(caminho_events, "r", encoding="utf-8") as f:
            eventos = json.load(f)
        for evento in eventos.get(f"level_{indice}", []):
            trigger = tuple(evento["trigger"])
            targets = [tuple(t) for t in evento["targets"]]
            triggers[trigger] = targets
    except Exception as e:
        print(f"⚠️ Erro ao carregar eventos: {e}")

    # Carrega nome e dica
    try:
        with open(caminho_names, "r", encoding="utf-8") as f:
            nomes = json.load(f)
        nome = nomes[indice]
    except:
        nome = "sem_nome"

    try:
        with open(caminho_hints, "r", encoding="utf-8") as f:
            dicas = json.load(f)
        dica = dicas[indice]
    except:
        dica = "sem_hint"

    return mapa, triggers, nome, dica
def salvar_mapa(mapa, caminho):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        for linha in mapa:
            arquivo.write("".join(linha) + "\n")