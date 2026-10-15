
import pygame
import math
import random

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
COR_DESTAQUE = (175, 50, 50)
COR_TEXTO = (180, 190, 210)

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
    MENU = "menu"
    READY = "ready"
    PLAYING = "playing"
    GAME_OVER = "game_over"

    def __init__(self):
        self.fonte_titulo = pygame.font.Font(None, 76)
        self.fonte_placar = pygame.font.Font(None, 64)
        self.fonte_mensagem = pygame.font.Font(None, 36)
        self.fonte_ajuda = pygame.font.Font(None, 26)
        
        # Modo de jogo
        self.modo = "Computer"
        # Controlador de movimentos da IA
        self.ia = AIController()
        
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

        # O jogo começa no menu, sem movimentar a bola.
        self.estado = self.MENU

    def iniciar_saque(self):
        if self.estado == self.MENU:
            # Primeiro Enter: prepara a partida.
            self.estado = self.READY

        elif self.estado == self.READY:
            # Segundo Enter: inicia o movimento da bola.
            self.estado = self.PLAYING

    def update(self, delta_time):
        # No menu e após o fim, a partida fica parada.
        if self.estado in (self.MENU, self.GAME_OVER):
            return

        teclas = pygame.key.get_pressed()

        # Jogador 1: W e S.
        direcao_esquerda = (
            int(teclas[pygame.K_s])
            - int(teclas[pygame.K_w])
        )

        # Jogador 2: setas.
        direcao_direita = (
            int(teclas[pygame.K_DOWN])
            - int(teclas[pygame.K_UP])
        )
        
        self.raquete_esquerda.update(
        	direcao_esquerda, delta_time
        )
        
        if self.modo == "computer":
        	if self.estado == self.PLAYING:
        		self.ia.update(
        			self.raquete_direita,
        			self.bola,
        			delta_time
        		)
        else:
        	self.raquete_direita.update(
        		direcao_direita, delta_time
        	)

        # Durante o saque, as raquetes podem se mover,
        # mas a bola permanece parada.
        if self.estado == self.READY:
            return

        ponto = self.bola.update(
            delta_time,
            self.raquete_esquerda,
            self.raquete_direita
        )

        if ponto == "esquerda":
            self.placar_esquerda += 1
            self.bola.reset(direcao=1)

            # O jogo pausa para o próximo saque.
            self.estado = self.READY

        elif ponto == "direita":
            self.placar_direita += 1
            self.bola.reset(direcao=-1)

            self.estado = self.READY

        # Verifica se a partida terminou.
        if self.placar_esquerda >= PONTOS_PARA_VENCER:
            self.vencedor = "Jogador 1"
            self.estado = self.GAME_OVER

        elif self.placar_direita >= PONTOS_PARA_VENCER:
            self.vencedor = "Jogador 2"
            self.estado = self.GAME_OVER

    def desenhar_texto_centralizado(
        self, tela, texto, fonte, cor, y
    ):
        superficie = fonte.render(texto, True, cor)
        retangulo = superficie.get_rect(
            center=(LARGURA // 2, y)
        )
        tela.blit(superficie, retangulo)

    def draw(self, tela):
        tela.fill(COR_FUNDO)

        # Linha central tracejada.
        for y in range(0, ALTURA, 30):
            pygame.draw.rect(
                tela,
                (65, 70, 90),
                (LARGURA // 2 - 2, y, 4, 16)
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
        
        if self.modo == "computer":
        	controles = "W/S: Mover raquete - R: Menu - ESC: Sair"
        else:
        	controles = "W/S: Jogador 1 - Setas: Jogador 2 - R: Menu - ESC: Sair"
        	
       	self.desenhar_texto_centralizado(
       		tela,
       		controles,
       		self.fonte_ajuda,
       		COR_TEXTO,
       		ALTURA - 48
       	)

        # Menu inicial.
        if self.estado == self.MENU:
            self.desenhar_texto_centralizado(
                tela,
                "PONG",
                self.fonte_titulo,
                COR_DESTAQUE,
                ALTURA // 2 - 75
            )

            self.desenhar_texto_centralizado(
                tela,
                "Pressione ENTER para iniciar o jogo",
                self.fonte_mensagem,
                COR_OBJETOS,
                ALTURA // 2 + 5
            )
            
            self.desenhar_texto_centralizado(
            	tela,
            	"[1] Contra computador [2] Contra jogador",
            	self.fonte_ajuda,
            	COR_TEXTO,
            	ALTURA // 2 + 45
            )
            
            modo_texto = (
            	f"Modo selecionado: " +
                ("[1]"
                if self.modo == "computer"
                else "[2]")
            )
            
            self.desenhar_texto_centralizado(
                tela,
                modo_texto,
                self.fonte_ajuda,
                COR_TEXTO,
                ALTURA // 2 + 65
            )

            self.desenhar_texto_centralizado(
                tela,
                f"Partida até {PONTOS_PARA_VENCER} pontos",
                self.fonte_ajuda,
                COR_TEXTO,
                ALTURA // 2 + 100
            )

        # Preparação para o saque.
        elif self.estado == self.READY:
            self.desenhar_texto_centralizado(
                tela,
                "Pressione ENTER para sacar",
                self.fonte_mensagem,
                COR_DESTAQUE,
                ALTURA // 2
            )

        # Tela de vitória.
        elif self.estado == self.GAME_OVER:
            self.desenhar_texto_centralizado(
                tela,
                f"{self.vencedor} venceu!",
                self.fonte_titulo,
                COR_DESTAQUE,
                ALTURA // 2 - 30
            )

            self.desenhar_texto_centralizado(
                tela,
                "Pressione R para voltar ao menu",
                self.fonte_mensagem,
                COR_OBJETOS,
                ALTURA // 2 + 35
            )
            
    def voltar_ao_menu(self):
    	self.estado = self.MENU
    	self.placar_esquerda = 0
    	self.placar_direita = 0
    	self.vencedor = None
    	self.bola.reset()
    	

# ==================================================
# LOOP PRINCIPAL
# ==================================================


def main():
    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Pong - Python + Pygame")

    relogio = pygame.time.Clock()
    jogo = Game()

    executando = True

    while executando:
        delta_time = min(relogio.tick(FPS) / 1000, 0.03)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
                
            elif evento.type == pygame.KEYDOWN:
            	if evento.key == pygame.K_ESCAPE:
            		executando = False
            		
            	elif evento.key == pygame.K_1:
            		if jogo.estado == Game.MENU:
            			jogo.modo = "computer"
            	
            	elif evento.key == pygame.K_2:
            		if jogo.estado == Game.MENU:
            			jogo.modo = "two_players"
            	
            	elif evento.key == pygame.K_RETURN:
            		jogo.iniciar_saque()
            		
            	elif evento.key == pygame.K_r:
            		if jogo.estado != Game.MENU:
            			jogo.voltar_ao_menu()
            	
            	elif (
            		evento.key == pygame.K_r
            		and jogo.estado == Game.GAME_OVER
            	):
            		jogo.reset()

        jogo.update(delta_time)
        jogo.draw(tela)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

