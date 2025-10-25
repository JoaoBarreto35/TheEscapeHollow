import os
import json


def verificar_niveis():
    pasta = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "maps")
    pasta = os.path.abspath(pasta)

    arquivos_txt = sorted([
        f for f in os.listdir(pasta)
        if f.startswith("level_") and f.endswith(".txt")
    ])
    indices_txt = [int(f.split("_")[1].split(".")[0]) for f in arquivos_txt]

    caminho_names = os.path.join(pasta, "names.json")
    caminho_hints = os.path.join(pasta, "hints.json")
    caminho_events = os.path.join(pasta, "events.json")

    with open(caminho_names, "r", encoding="utf-8") as f:
        nomes = json.load(f)
    with open(caminho_hints, "r", encoding="utf-8") as f:
        dicas = json.load(f)
    with open(caminho_events, "r", encoding="utf-8") as f:
        eventos = json.load(f)

    ...
    indices_json = list(range(len(nomes)))
    eventos_ids = [int(k.split("_")[1]) for k in eventos.keys()]

    print("📦 Arquivos .txt encontrados:", indices_txt)
    print("📝 Nomes registrados:", indices_json)
    print("🎯 Eventos registrados:", eventos_ids)

    # Verificações
    for i in indices_json:
        if i not in indices_txt:
            print(f"⚠️ level_{i}.txt está ausente, mas existe em names/hints.json")

    for i in indices_txt:
        if i >= len(nomes):
            print(f"⚠️ level_{i}.txt existe, mas não está registrado em names.json")

    for i in eventos_ids:
        if i not in indices_txt:
            print(f"⚠️ Eventos para level_{i} existem, mas o arquivo .txt está ausente")

    if len(nomes) != len(dicas):
        print(f"❌ names.json e hints.json têm tamanhos diferentes: {len(nomes)} vs {len(dicas)}")

    print("✅ Verificação concluída.")

if __name__ == "__main__":
    verificar_niveis()