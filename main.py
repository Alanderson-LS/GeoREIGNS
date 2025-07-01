import pygame
import random
import time

from eventos import *
from recursos import itens_pendentes

height = 600
width = 800
fps = 60
fundo = "fundo_base_intro.jpeg"
window_name = "Teste GeoREIGNS"

estado = "MENU"

def button_create(
                    screen, 
                    caminho, 
                    pos,
                    tamanho, 
                    func):
    
    imagem_botao = pygame.image.load(caminho).convert_alpha()
    imagem_botao = pygame.transform.scale(imagem_botao, tamanho)
    botao_rect = imagem_botao.get_rect(topleft = pos)
    screen.blit(imagem_botao, botao_rect)

    return botao_rect, func

def start():
    global estado
    estado = "JOGO"

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(window_name)
    clock = pygame.time.Clock()
    
    caminho = "imagens/fundos/" + fundo
    background = pygame.image.load(caminho).convert()
    background = pygame.transform.scale(background, (width, height))
    screen.blit(background, (0, 0))
    execution = True
    while execution:
        if estado == "MENU":
            botao_rect, botao_func = button_create(screen, "imagens/botoes/jogar.png", (300, 250), (200, 100), start)
        elif estado == "JOGO":
            screen.fill((0, 0, 0))
        else:
            execution = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                execution = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if estado == "MENU":
                    if botao_rect.collidepoint(event.pos):
                        botao_func()

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    main()