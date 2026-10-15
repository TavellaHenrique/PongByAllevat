
import pygame

from config import (
	ALTURA,
	LARGURA,
	FPS,
)
from game import Game

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

