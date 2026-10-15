# Pong — Python e Pygame

Uma versão simples do clássico Pong, desenvolvida em Python com Pygame e formas geométricas.

## Requisitos

- Linux Mint (ou outra distribuição Linux com ambiente gráfico)
- Python 3
- `venv` e `pip` para Python
- Pygame
- VS Code (opcional, recomendado para editar o código)

## Estrutura do projeto

```text
meu_jogo/
├── .venv/       # Ambiente virtual local (criado durante a configuração)
├── main.py      # Código do jogo
└── README.md    # Estas instruções
```

> A pasta `.venv/` é criada localmente e não precisa ser incluída no controle de versão.

## 1. Instalar os pré-requisitos

No Linux Mint, abra o terminal e execute:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

Se esses pacotes já estiverem instalados, você pode seguir para a próxima etapa.

Confira as versões:

```bash
python3 --version
python3 -m pip --version
```

## 2. Preparar o projeto

Entre na pasta do projeto. Por exemplo, se ela estiver em `~/projetos/meu_jogo`:

```bash
cd ~/projetos/meu_jogo
```

Se ainda não criou a pasta, você pode criá-la assim:

```bash
mkdir -p ~/projetos/meu_jogo
cd ~/projetos/meu_jogo
```

Crie o ambiente virtual:

```bash
python3 -m venv .venv
```

Ative-o:

```bash
source .venv/bin/activate
```

Quando estiver ativo, o terminal normalmente exibirá `(.venv)` no início da linha.

## 3. Instalar o Pygame

Com o ambiente virtual ativo, execute:

```bash
python -m pip install --upgrade pip
python -m pip install pygame
```

Para confirmar a instalação:

```bash
python -m pygame --version
```

## 4. Executar o jogo

Confirme que você está na pasta que contém `main.py` e que o ambiente virtual está ativo. Em seguida, execute:

```bash
python main.py
```

Uma janela do jogo deverá abrir. Para fechar, pressione `Esc` ou use o botão de fechar da janela.

## 5. Controles

| Ação | Teclas |
|---|---|
| Mover a raquete do jogador 1 (esquerda) para cima | `W` |
| Mover a raquete do jogador 1 (esquerda) para baixo | `S` |
| Mover a raquete do jogador 2 (direita) para cima | `↑` |
| Mover a raquete do jogador 2 (direita) para baixo | `↓` |
| Reiniciar após o fim da partida | `R` |
| Sair do jogo | `Esc` |

O primeiro jogador a marcar **5 pontos** vence a partida.

## 6. Abrir no VS Code

1. Abra o VS Code.
2. Selecione **File → Open Folder** e abra a pasta do projeto.
3. Instale a extensão **Python**, da Microsoft, se ainda não estiver instalada.
4. Pressione `Ctrl + Shift + P`.
5. Selecione **Python: Select Interpreter**.
6. Escolha o interpretador `./.venv/bin/python`.
7. Abra um terminal integrado e execute:

   ```bash
   source .venv/bin/activate
   python main.py
   ```

## 7. Próximas execuções

Depois da configuração inicial, normalmente basta abrir um terminal, entrar na pasta do projeto, ativar o ambiente virtual e executar o jogo:

```bash
cd ~/projetos/meu_jogo
source .venv/bin/activate
python main.py
```

Não é necessário reinstalar o Pygame a cada execução. Se abrir um terminal novo, ative o ambiente virtual novamente.

## Solução de problemas

### `ModuleNotFoundError: No module named 'pygame'`

Ative o ambiente virtual e instale o Pygame nele:

```bash
source .venv/bin/activate
python -m pip install pygame
```

### `python: command not found`

Em algumas instalações Linux, use `python3` para criar o ambiente virtual. Depois de ativá-lo, o comando `python` normalmente estará disponível dentro do ambiente.

### `No module named venv`

No Linux Mint, instale o pacote necessário:

```bash
sudo apt install python3-venv
```

### O VS Code não reconhece o Pygame

Selecione o interpretador `./.venv/bin/python` em **Python: Select Interpreter** e abra um novo terminal integrado.

### A janela gráfica não abre

Execute `python main.py` a partir de um terminal em uma sessão gráfica do Linux e verifique se alguma mensagem de erro aparece no terminal.

---

## Tecnologias

- [Python](https://www.python.org/)
- [Pygame](https://www.pygame.org/)

