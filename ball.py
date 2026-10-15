
import math
import pygame

from config import (
	LARGURA,
	ALTURA,
	COR_OBJETOS,
	COR_DESTAQUE,
	ALTURA_RAQUETE,
	RAIO_BOLA,
	VELOCIDADE_INICIAL_BOLA,
	VELOCIDADE_MAXIMA_BOLA,
	AUMENTO_VELOCIDADE,
	ANGULO_MAXIMO,
)

# ==================================================
# CLASSE BALL: BOLA
# ==================================================

class Ball:
    def __init__(self):
        self.reset()

    def reset(self, direcao=1):
        self.x = LARGURA / 2
        self.y = ALTURA / 2

        # Velocidade inicial com um pequeno ângulo.
        angulo_inicial = math.radians(12)

        self.vx = (
            VELOCIDADE_INICIAL_BOLA
            * math.cos(angulo_inicial)
            * direcao
        )

        self.vy = (
            VELOCIDADE_INICIAL_BOLA
            * math.sin(angulo_inicial)
        )

        self.rect = pygame.Rect(
            0, 0, RAIO_BOLA * 2, RAIO_BOLA * 2
        )

        self.sync_rect()

    def sync_rect(self):
        self.rect.center = (round(self.x), round(self.y))

    def update(
        self,
        delta_time,
        raquete_esquerda,
        raquete_direita
    ):
        # Movimento usando velocidade em pixels por segundo.
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time

        # Colisão com a borda superior.
        if self.y - RAIO_BOLA <= 0:
            self.y = RAIO_BOLA
            self.vy = abs(self.vy)

        # Colisão com a borda inferior.
        elif self.y + RAIO_BOLA >= ALTURA:
            self.y = ALTURA - RAIO_BOLA
            self.vy = -abs(self.vy)

        self.sync_rect()

        # Colisão com a raquete esquerda.
        if (
            self.vx < 0
            and self.rect.colliderect(raquete_esquerda.rect)
        ):
            self.x = raquete_esquerda.rect.right + RAIO_BOLA
            self.bounce(raquete_esquerda, direcao=1)

        # Colisão com a raquete direita.
        elif (
            self.vx > 0
            and self.rect.colliderect(raquete_direita.rect)
        ):
            self.x = raquete_direita.rect.left - RAIO_BOLA
            self.bounce(raquete_direita, direcao=-1)

        self.sync_rect()

        # Verifica se alguém marcou um ponto.
        if self.x + RAIO_BOLA < 0:
            return "direita"

        if self.x - RAIO_BOLA > LARGURA:
            return "esquerda"

        return None

    def bounce(self, raquete, direcao):
        # -1: extremidade superior; 0: centro; 1: inferior.
        impacto = (
            self.y - raquete.rect.centery
        ) / (ALTURA_RAQUETE / 2)

        # Evita valores fora do intervalo esperado.
        impacto = max(-1.0, min(1.0, impacto))

        # Mantém o aumento da velocidade sob controle.
        velocidade_atual = math.hypot(self.vx, self.vy)

        nova_velocidade = min(
            velocidade_atual * AUMENTO_VELOCIDADE,
            VELOCIDADE_MAXIMA_BOLA
        )

        # O ponto de impacto determina o ângulo de saída.
        angulo = impacto * ANGULO_MAXIMO

        self.vx = (
            math.cos(angulo)
            * nova_velocidade
            * direcao
        )

        self.vy = math.sin(angulo) * nova_velocidade

    def draw(self, tela):
        pygame.draw.circle(
            tela,
            COR_DESTAQUE,
            (round(self.x), round(self.y)),
            RAIO_BOLA
        )
