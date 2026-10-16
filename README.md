## Pong by Allevat
Jogo desenvolvido em Python com Pygame, inspirado no arcade clássico Pong.

## Funcionalidades
- Modo de dois jogadores locais e contra computador
- Temas visuais simples
- Pontuação de vitória ajustável
- Aumento progressivo de velocidade da bola

## Requisitos globais
- Python 3.12.x
- pip (Gerenciador de pacotes do Python)

## Como executar pela primeira vez (Sistema baseado em Linux)
1. Faça o download dos arquivos no GitHub (.zip)
2. Extraia os arquivos da pasta compactada
3. Abra um terminal na raíz da pasta
4. Crie e ative um ambiente virtual
   - python3 -m venv .venv
   - source .venv/bin/activate
5. Instale as dependências com o comando abaixo
   - python -m pip install -r requirements.txt
6. Execute o jogo
   - python main.py

## Como executar após a primeira vez
1. Abra um terminal na raíz da pasta
2. Ative o ambiente virtual
   - source .venv/bin/activate
3. Execute o jogo
   - python main.py

## Como executar pela primeira vez (Windows)
1. Faça o download dos arquivos no GitHub (.zip)
2. Extraia os arquivos da pasta compactada
3. Abra o cmd na raíz da pasta
4. Crie um ambiente virtual
   - py -3.12 -m venv .venv
5. Use o Python do ambiente virtual para satisfazer os requisitos*
   - .\.venv\Scripts\python.exe -m pip install --upgrade pip
   - .\.venv\Scripts\python.exe -m pip install -r requirements.txt
6. Inicie a execução do jogo
   - .\.venv\Scripts\python.exe main.py

*Nota: Por conta de uma política do PowerShell, é mais fácil executar o Python dentro do ambiente virtual do que ativá-lo de fato (como em distribuições Linux). Tentei simplificar as etapas de instalação e execução, incluindo substituir a clonagem do repositório pelo download em ".zip".

## Como executar após a primeira vez (Windows)
1. Abra o cmd na raíz da pasta
2. Garanta que as dependências estão prontas
   - .\.venv\Scripts\python.exe -m pip install -r requirements.txt
3. Inicie a execução do jogo
   - .\.venv\Scripts\python.exe main.py

## Controles

### Controles no menu
- Teclas númericas: Selecionar modo de jogo
- Setas esquerda/direita: Ajustar pontos para vencer
- Setas cima/baixo: Selecionar tema
- ENTER: Iniciar jogo
- ESC: Sair do jogo

### Controles contra computador
- W/S: Mover raquete
- ENTER: Continuar jogo
- R: Voltar ao menu
- ESC: Sair do jogo

### Controles em dois jogadores
- W/S: Mover raquete esquerda
- Setas Cima/Baixo: Mover raquete direita
- ENTER: Continuar jogo
- R: Voltar ao menu
- ESC: Sair do jogo
