import os
import json

from code.editor.limpar_niveis_invalidos import limpar_niveis_invalidos
from code.editor.verificar_niveis import verificar_niveis


def remover_nivel(indice):
    pasta = "assets/maps"
    caminho_events = os.path.join(pasta, "events.json")
    caminho_names = os.path.join(pasta, "names.json")
    caminho_hints = os.path.join(pasta, "hints.json")

    # Remove o arquivo .txt
    os.remove(os.path.join(pasta, f"level_{indice}.txt"))

    # Carrega os arquivos JSON
    with open(caminho_events, "r", encoding="utf-8") as f:
        eventos = json.load(f)
    with open(caminho_names, "r", encoding="utf-8") as f:
        nomes = json.load(f)
    with open(caminho_hints, "r", encoding="utf-8") as f:
        dicas = json.load(f)

    # Remove os dados do nível
    del eventos[f"level_{indice}"]
    del nomes[indice]
    del dicas[indice]

    # Reorganiza os arquivos restantes
    total = len(nomes)
    for i in range(indice + 1, total + 1):
        os.rename(os.path.join(pasta, f"level_{i}.txt"), os.path.join(pasta, f"level_{i-1}.txt"))
        eventos[f"level_{i-1}"] = eventos.pop(f"level_{i}")

    # Salva os arquivos atualizados
    with open(caminho_events, "w", encoding="utf-8") as f:
        json.dump(eventos, f, indent=2, ensure_ascii=False)
    with open(caminho_names, "w", encoding="utf-8") as f:
        json.dump(nomes, f, indent=2, ensure_ascii=False)
    with open(caminho_hints, "w", encoding="utf-8") as f:
        json.dump(dicas, f, indent=2, ensure_ascii=False)

    print(f"🗑️ Nível {indice} removido com sucesso!")
    verificar_niveis()
    limpar_niveis_invalidos()


def salvar_nivel(mapa, triggers, nome_nivel, dica_nivel, indice=None):
    pasta = "assets/maps"
    caminho_mapa = os.path.join(pasta, f"level_{indice if indice is not None else len(os.listdir(pasta))}.txt")
    caminho_names = os.path.join(pasta, "names.json")
    caminho_hints = os.path.join(pasta, "hints.json")
    caminho_events = os.path.join(pasta, "events.json")

    # Carrega JSONs
    with open(caminho_names, "r", encoding="utf-8") as f:
        nomes = json.load(f)
    with open(caminho_hints, "r", encoding="utf-8") as f:
        dicas = json.load(f)
    with open(caminho_events, "r", encoding="utf-8") as f:
        eventos = json.load(f)

    # Define índice
    if indice is None:
        indice = len(nomes)
        nomes.append(nome_nivel)
        dicas.append(dica_nivel)
    else:
        nomes[indice] = nome_nivel
        dicas[indice] = dica_nivel

    # Salva mapa
    with open(os.path.join(pasta, f"level_{indice}.txt"), "w", encoding="utf-8") as f:
        for linha in mapa:
            f.write("".join(linha) + "\n")

    # Salva eventos
    eventos[f"level_{indice}"] = [
        {"trigger": list(trigger), "targets": [list(t) for t in targets]}
        for trigger, targets in triggers.items()
    ]

    # Salva JSONs
    with open(caminho_names, "w", encoding="utf-8") as f:
        json.dump(nomes, f, indent=2, ensure_ascii=False)
    with open(caminho_hints, "w", encoding="utf-8") as f:
        json.dump(dicas, f, indent=2, ensure_ascii=False)
    with open(caminho_events, "w", encoding="utf-8") as f:
        json.dump(eventos, f, indent=2, ensure_ascii=False)

    print(f"💾 Nível {indice} salvo com sucesso!")