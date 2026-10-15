
import pygame
import math

# ==================================================
# CONFIGURAÇÕES
# ==================================================

# Tela e Gráficos
LARGURA = 900
ALTURA = 600
FPS = 60

# Cores
COR_FUNDO = (18, 20, 30)
COR_OBJETOS = (235, 240, 255)
COR_DESTAQUE = (80, 220, 160)
COR_TEXTO = (180, 190, 210)

# Raquete
LARGURA_RAQUETE = 16
ALTURA_RAQUETE = 110
VELOCIDADE_RAQUETE = 420

# Bola
RAIO_BOLA = 10
VELOCIDADE_INICIAL_BOLA = 360
VELOCIDADE_MAXIMA_BOLA = 650
AUMENTO_VELOCIDADE = 1.05
ANGULO_MAXIMO = math.radians(60)

# Condições de vitórias
PONTOS_PARA_VENCER = 5


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



# ==================================================
# CLASSE GAME: REGRAS E ESTADO DA PARTIDA
# ==================================================

class Game:
    def __init__(self):
        self.fonte_placar = pygame.font.Font(None, 64)
        self.fonte_mensagem = pygame.font.Font(None, 36)
        self.fonte_ajuda = pygame.font.Font(None, 26)

        self.reset()

    def reset(self):
        self.raquete_esquerda = Paddle(
            35,
            ALTURA // 2 - ALTURA_RAQUETE // 2
        )

        self.raquete_direita = Paddle(
            LARGURA - 35 - LARGURA_RAQUETE,
            ALTURA // 2 - ALTURA_RAQUETE // 2
        )

        self.bola = Ball()

        self.placar_esquerda = 0
        self.placar_direita = 0
        self.vencedor = None

    def update(self, delta_time):
        if self.vencedor is not None:
            return

        teclas = pygame.key.get_pressed()

        # Jogador da esquerda: W e S.
        direcao_esquerda = (
            int(teclas[pygame.K_s])
            - int(teclas[pygame.K_w])
        )

        # Jogador da direita: setas para cima e para baixo.
        direcao_direita = (
            int(teclas[pygame.K_DOWN])
            - int(teclas[pygame.K_UP])
        )

        self.raquete_esquerda.update(
            direcao_esquerda, delta_time
        )

        self.raquete_direita.update(
            direcao_direita, delta_time
        )

        ponto = self.bola.update(
            delta_time,
            self.raquete_esquerda,
            self.raquete_direita
        )

        if ponto == "esquerda":
            self.placar_esquerda += 1
            self.bola.reset(direcao=1)

        elif ponto == "direita":
            self.placar_direita += 1
            self.bola.reset(direcao=-1)

        # Verifica a condição de vitória.
        if self.placar_esquerda >= PONTOS_PARA_VENCER:
            self.vencedor = "Jogador 1"

        elif self.placar_direita >= PONTOS_PARA_VENCER:
            self.vencedor = "Jogador 2"

    def draw(self, tela):
        tela.fill(COR_FUNDO)

        # Linha central tracejada.
        x_centro = LARGURA // 2

        for y in range(0, ALTURA, 30):
            pygame.draw.rect(
                tela,
                (65, 70, 90),
                (x_centro - 2, y, 4, 16)
            )

        # Placar.
        texto_esquerda = self.fonte_placar.render(
            str(self.placar_esquerda), True, COR_TEXTO
        )

        texto_direita = self.fonte_placar.render(
            str(self.placar_direita), True, COR_TEXTO
        )

        tela.blit(
            texto_esquerda,
            (LARGURA // 2 - 80, 35)
        )

        tela.blit(
            texto_direita,
            (LARGURA // 2 + 45, 35)
        )

        self.raquete_esquerda.draw(tela)
        self.raquete_direita.draw(tela)
        self.bola.draw(tela)

        # Instruções na parte inferior.
        ajuda = self.fonte_ajuda.render(
            "W / S: Jogador 1     Setas: Jogador 2     ESC: Sair",
            True,
            COR_TEXTO
        )

        tela.blit(
            ajuda,
            ajuda.get_rect(
                center=(LARGURA // 2, ALTURA - 25)
            )
        )

        # Tela de vitória.
        if self.vencedor is not None:
            mensagem = self.fonte_mensagem.render(
                f"{self.vencedor} venceu!",
                True,
                COR_DESTAQUE
            )

            reiniciar = self.fonte_ajuda.render(
                "Pressione R para jogar novamente",
                True,
                COR_TEXTO
            )

            tela.blit(
                mensagem,
                mensagem.get_rect(
                    center=(LARGURA // 2, ALTURA // 2 - 25)
                )
            )

            tela.blit(
                reiniciar,
                reiniciar.get_rect(
                    center=(LARGURA // 2, ALTURA // 2 + 20)
                )
            )


# ==================================================
# LOOP PRINCIPAL
# ==================================================

def main():
    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Pong - Python e Pygame")

    relogio = pygame.time.Clock()
    jogo = Game()

    executando = True

    while executando:
        # Tempo decorrido em segundos.
        delta_time = min(relogio.tick(FPS) / 1000, 0.03)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    executando = False

                elif evento.key == pygame.K_r:
                    if jogo.vencedor is not None:
                        jogo.reset()

        jogo.update(delta_time)
        jogo.draw(tela)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
