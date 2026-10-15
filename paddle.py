
import pygame

from config import (
	LARGURA,
	ALTURA,
	LARGURA_RAQUETE,
	ALTURA_RAQUETE,
	VELOCIDADE_RAQUETE,
	COR_OBJETOS
)

# ==================================================
# CLASSE PADDLE: RAQUETE
# ==================================================

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(
            x,
            y,
            LARGURA_RAQUETE,
            ALTURA_RAQUETE
        )

    def update(self, direcao, delta_time):
        self.rect.y += int(
            direcao * VELOCIDADE_RAQUETE * delta_time
        )

        # Mantém a raquete dentro da janela.
        self.rect.clamp_ip(pygame.Rect(0, 0, LARGURA, ALTURA))

    def draw(self, tela):
        pygame.draw.rect(
            tela,
            COR_OBJETOS,
            self.rect,
            border_radius=5
        )
