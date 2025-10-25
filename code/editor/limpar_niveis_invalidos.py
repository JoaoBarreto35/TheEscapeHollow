import os
import json

def limpar_niveis_invalidos():
    pasta = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "maps")
    pasta = os.path.abspath(pasta)

    # Arquivos .txt válidos
    arquivos_txt = sorted([
        f for f in os.listdir(pasta)
        if f.startswith("level_") and f.endswith(".txt")
    ])
    indices_validos = [int(f.split("_")[1].split(".")[0]) for f in arquivos_txt]

    # Carrega JSONs
    with open(os.path.join(pasta, "names.json"), "r", encoding="utf-8") as f:
        nomes = json.load(f)
    with open(os.path.join(pasta, "hints.json"), "r", encoding="utf-8") as f:
        dicas = json.load(f)
    with open(os.path.join(pasta, "events.json"), "r", encoding="utf-8") as f:
        eventos = json.load(f)

    # Filtra apenas os índices válidos
    nomes_filtrados = [nomes[i] for i in indices_validos if i < len(nomes)]
    dicas_filtradas = [dicas[i] for i in indices_validos if i < len(dicas)]
    eventos_filtrados = {
        f"level_{i}": eventos[f"level_{i}"]
        for i in indices_validos if f"level_{i}" in eventos
    }

    # Salva os arquivos corrigidos
    with open(os.path.join(pasta, "names.json"), "w", encoding="utf-8") as f:
        json.dump(nomes_filtrados, f, indent=2, ensure_ascii=False)
    with open(os.path.join(pasta, "hints.json"), "w", encoding="utf-8") as f:
        json.dump(dicas_filtradas, f, indent=2, ensure_ascii=False)
    with open(os.path.join(pasta, "events.json"), "w", encoding="utf-8") as f:
        json.dump(eventos_filtrados, f, indent=2, ensure_ascii=False)

    print("🧹 Limpeza concluída. JSONs sincronizados com os arquivos .txt.")

if __name__ == "__main__":
    limpar_niveis_invalidos()