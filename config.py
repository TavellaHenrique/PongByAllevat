
import math

# ==================================================
# CONFIGURAÇÕES
# ==================================================

# Tela e Gráficos
LARGURA = 900
ALTURA = 600
FPS = 60

# Raquete
LARGURA_RAQUETE = 16
ALTURA_RAQUETE = 110
VELOCIDADE_RAQUETE = 420

# Inteligência artificial
VELOCIDADE_IA = 300
ERRO_IA = 35
DISTANCIA_REACAO_IA = 360

# Bola
RAIO_BOLA = 10
VELOCIDADE_INICIAL_BOLA = 360
VELOCIDADE_MAXIMA_BOLA = 650
AUMENTO_VELOCIDADE = 1.05
ANGULO_MAXIMO = math.radians(60)

# Condições de vitórias
PONTOS_PARA_VENCER = 5

# Cores
COR_FUNDO = (18, 20, 30)
COR_OBJETOS = (235, 240, 255)
COR_DESTAQUE = (80, 230, 230)
COR_TEXTO = (180, 190, 210)

TEMAS = [
	{
		"nome": "Clássico",
		"fundo": (18, 20, 30),
		"objetos": (235, 240, 255),
		"destaque": (80, 220, 160),
		"texto": (180, 190, 210),
	},
	{
		"nome": "Gelo",
		"fundo": (240, 242, 245),
		"objetos": (35, 40, 55),
		"destaque": (35, 100, 220),
		"texto": (70, 75, 90),
	},
    {
        "nome": "Futuro Retrô",
        "fundo": (16, 10, 35),
        "objetos": (0, 240, 255),
        "destaque": (255, 45, 160),
        "texto": (210, 190, 255),
    },
    {
        "nome": "Halloween",
        "fundo": (10, 10, 10),
        "objetos": (230, 215, 112),
        "destaque": (255, 125, 75),
        "texto": (230, 215, 112),
    },
]

