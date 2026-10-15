
import random
import pygame

from config import (
	LARGURA,
	ALTURA,
	VELOCIDADE_IA,
	ERRO_IA,
	DISTANCIA_REACAO_IA,
)

# ==================================================
# CLASSE AICONTROLLER: Raquete da IA
# ==================================================
 
class AIController:
    def __init__(self):
        self.desvio = 0
        self.direcao_anterior = 0

    def update(self, raquete, bola, delta_time):
        # A IA só precisa reagir quando a bola vem em sua direção.
        if bola.vx > 0:
            # Sorteia um novo erro quando a bola passa a se
            # deslocar para a direita.
            if self.direcao_anterior <= 0:
                self.desvio = random.uniform(
                    -ERRO_IA, ERRO_IA
                )

            distancia = raquete.rect.centerx - bola.x

            if distancia <= DISTANCIA_REACAO_IA:
                alvo_y = bola.y + self.desvio
            else:
                alvo_y = ALTURA / 2

            diferenca = alvo_y - raquete.rect.centery

            # Limita a velocidade de movimentação.
            limite_movimento = VELOCIDADE_IA * delta_time
            movimento = max(
                -limite_movimento,
                min(limite_movimento, diferenca)
            )

            raquete.rect.y += round(movimento)

            # Mantém a raquete dentro da janela.
            raquete.rect.clamp_ip(
                pygame.Rect(0, 0, LARGURA, ALTURA)
            )

        self.direcao_anterior = 1 if bola.vx > 0 else -1
