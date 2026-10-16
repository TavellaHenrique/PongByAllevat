
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
            # Sair do jogo em ação padrão de encerrar
            if evento.type == pygame.QUIT:
                executando = False
            
            # Eventos acionados por tecla
            elif evento.type == pygame.KEYDOWN:
                # Tecla para sair do jogo
                if evento.key == pygame.K_ESCAPE:
                    executando = False
                    
                # Mudar modo de jogo na tela de Menu
                elif evento.key == pygame.K_1:
                    if jogo.estado == Game.MENU:
                        jogo.modo = "computer"
                elif evento.key == pygame.K_2:
                    if jogo.estado == Game.MENU:
                        jogo.modo = "two_players"
                
                # Mudar pontuação de vitória na tela de Menu
                elif evento.key == pygame.K_LEFT:
                    if jogo.estado == Game.MENU:
                        if jogo.pontos_para_vencer > 1:
                            jogo.pontos_para_vencer -= 1
                elif evento.key == pygame.K_RIGHT:
                    if jogo.estado == Game.MENU:
                        jogo.pontos_para_vencer += 1
                
                elif evento.key == pygame.K_UP:
                    if jogo.estado == Game.MENU:
                        jogo.alterar_tema(-1)
                elif evento.key == pygame.K_DOWN:
                    if jogo.estado == Game.MENU:
                        jogo.alterar_tema(1)
                
                # Iniciar jogo
                elif evento.key == pygame.K_RETURN:
                    jogo.iniciar_saque()
                    
                # Tecla para retornar ao Menu
                elif evento.key == pygame.K_r:
                    if jogo.estado != Game.MENU:
                        jogo.voltar_ao_menu()
                
                # Tecla para reiniciar o jogo ao terminar partida
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

