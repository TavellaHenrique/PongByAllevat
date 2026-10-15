
import pygame

from config import (
	LARGURA,
	ALTURA,
	ALTURA_RAQUETE,
	LARGURA_RAQUETE,
	COR_FUNDO,
	COR_OBJETOS,
	COR_DESTAQUE,
	COR_TEXTO,
	PONTOS_PARA_VENCER,
)

from paddle import Paddle
from ai import AIController
from ball import Ball

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
        
        # Modo de jogo inicialmente selecionado
        self.modo = "Computer"
        # Conecta o controlador da IA
        self.ia = AIController()
        
        # Carrega a pontuação de vitória
        self.pontos_para_vencer = PONTOS_PARA_VENCER
        
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
        if self.placar_esquerda >= self.pontos_para_vencer:
            self.vencedor = "Jogador 1"
            self.estado = self.GAME_OVER

        elif self.placar_direita >= self.pontos_para_vencer:
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
        	controles = "[W/S: Mover raquete]"
        else:
        	controles = "[W/S: Jogador 1] [Setas: Jogador 2]"
        	
       	self.desenhar_texto_centralizado(
       		tela,
       		controles,
       		self.fonte_ajuda,
       		COR_TEXTO,
       		ALTURA - 48
       	)
       	
       	self.desenhar_texto_centralizado(
       		tela,
       		"[R: Voltar ao menu] [ESC: Sair]",
       		self.fonte_ajuda,
       		COR_TEXTO,
       		ALTURA - 20
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
                ALTURA // 2 - 30
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
                COR_DESTAQUE,
                ALTURA // 2 + 45
            )
            
            self.desenhar_texto_centralizado(
            	tela,
            	"[1] Contra computador [2] Contra jogador",
            	self.fonte_ajuda,
            	COR_TEXTO,
            	ALTURA // 2 + 65
            )
            
            pontos_texto = f"Pontos para vencer: {self.pontos_para_vencer}"

            self.desenhar_texto_centralizado(
                tela,
                pontos_texto,
                self.fonte_ajuda,
                COR_DESTAQUE,
                ALTURA // 2 + 100
            )
            
            self.desenhar_texto_centralizado(
            	tela,
            	"[Setas ESQUERDA/DIREITA]",
            	self.fonte_ajuda,
            	COR_TEXTO,
            	ALTURA // 2 + 120
            )

        # Preparação para o saque.
        elif self.estado == self.READY:
            self.desenhar_texto_centralizado(
                tela,
                "Pressione ENTER para sacar",
                self.fonte_mensagem,
                COR_DESTAQUE,
                ALTURA // 2 + 30
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
    	
