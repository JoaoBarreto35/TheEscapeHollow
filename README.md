🧩 Dungeon Trigger Editor
Um jogo 2D com editor de mapas e sistema de lógica entre sensores e armadilhas. Criado com Python e Pygame, o projeto permite construir fases interativas com elementos como espinhos animados, sensores de som, e conexões entre triggers e targets. Ideal pra puzzles, exploração e desafios táticos.

📸 Preview
Imagens do jogo e do editor (adicione aqui screenshots como os que você já mandou)


🗂️ Estrutura do Projeto
code/
├── core/
│   └── image_loader.py         # Carregamento de imagens
├── mechanics/
│   ├── target.py               # Classe base para targets
│   ├── trigger.py              # Classe base para triggers
│   ├── spikes_trap.py          # Espinhos animados
│   └── sound_sensor.py         # Sensor de som com raio
├── settings.py                 # Símbolos e constantes globais
├── editor/
│   └── interface.py            # Interface visual do editor
assets/
├── spikes.png
├── sound_sensor_on.png
├── sound_sensor_off.png
└── sfx/
    └── stone_drag.wav
main.py                         # Loop principal do jogo/editor



🎮 Funcionalidades
🔧 Editor de Mapas
- Grade interativa com símbolos
- Painel lateral com scroll e seleção
- Campos de nome e dica do nível
- Visualização de raio de sensores
- Conexões visuais entre triggers e targets
🎯 Sistema de Triggers
- Triggers ativam targets com base em eventos
- Conexões persistentes entre elementos
- Visualização clara no editor
🕳️ Armadilhas animadas
- Espinhos surgem e recolhem com animação
- Temporizador de duração ativa
- Recolhimento automático
- Som de ativação
🔊 Sensor de Som
- Detecta movimento de entidades dentro de um raio
- Ativa targets ao detectar deslocamento
- Colisão virtual com área de escuta
- Visualização da aura no editor

🚀 Como rodar
- Instale o Pygame:
pip install pygame
- Execute o jogo/editor:
python main.py



🧠 Como funciona
- Cada célula do mapa contém um símbolo (MapSymbol) que representa um objeto
- Triggers (como sensores) ativam targets (como espinhos) com base em lógica definida
- O editor permite desenhar mapas e conectar elementos visualmente
- O jogo interpreta essa lógica e executa animações, sons e efeitos

🛠️ Futuras melhorias
- Inimigos com patrulha e IA simples
- Novos tipos de armadilhas (lava, gelo, pistões)
- Sistema de partículas e efeitos visuais
- Exportação/importação de mapas
- Suporte a múltiplos níveis e progressão
- Modo de jogo com HUD e objetivos

👨‍💻 Autor
João — Desenvolvedor, designer de puzzles e criador do universo sombrio de Escape the Hollow.
Feito com 💻 Python + 🎮 Pygame + 🧠 criatividade.

Se quiser, posso te ajudar a gerar uma versão em inglês, criar badges pro GitHub, ou até montar uma capa visual com o nome do projeto. Esse README já tá pronto pra brilhar!
