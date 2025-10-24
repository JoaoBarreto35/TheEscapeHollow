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