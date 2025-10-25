import json
from code.editor.mapa import carregar_mapa
from code.editor.editor_scene import run_editor

def listar_niveis():
    with open("assets/maps/names.json", "r", encoding="utf-8") as f:
        nomes = json.load(f)
    with open("assets/maps/hints.json", "r", encoding="utf-8") as f:
        dicas = json.load(f)

    return [(i, nomes[i], dicas[i]) for i in range(len(nomes))]

def start_editor(indice=None):
    from code.editor.mapa import carregar_mapa

    if indice is None:
        mapa, triggers, nome, dica = carregar_mapa("assets/maps/template.txt")
    else:
        mapa, triggers, nome, dica = carregar_mapa(f"assets/maps/level_{indice}.txt")

    run_editor(
        mapa,
        indice=indice,
        triggers=triggers,
        name=nome,
        hint=dica
    )