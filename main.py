import pygame
import random
import time
import asyncio

from eventos import *
from recursos import itens_pendentes

height = 600
width = 800
fps = 60
fundo_menu = "fundo_base_intro.jpeg"
fundo_jogo = "castelo_interno.png"
window_name = "Teste GeoREIGNS"

estado = "MENU"

def button_create(
                    screen, 
                    caminho_menu, 
                    pos,
                    tamanho, 
                    func):
    
    imagem_botao = pygame.image.load(caminho_menu).convert_alpha()
    imagem_botao = pygame.transform.scale(imagem_botao, tamanho)
    botao_rect = imagem_botao.get_rect(topleft = pos)
    screen.blit(imagem_botao, botao_rect)

    return botao_rect, func

def start():
    global estado
    estado = "JOGO"

async def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(window_name)
    clock = pygame.time.Clock()
    
    caminho_menu = "imagens/bg/" + fundo_menu
    background_menu = pygame.image.load(caminho_menu).convert()
    background_menu = pygame.transform.scale(background_menu, (width, height))
    
    caminho_jogo = "imagens/bg/" + fundo_jogo
    background_jogo = pygame.image.load(caminho_jogo).convert()
    background_jogo = pygame.transform.scale(background_jogo, (width, height))
    
    fonte = "fonte/MedievalSharp.ttf"
    fonte_pygame = pygame.font.Font(fonte, 16)
    def dialogo(
        surface, 
        mensagem, 
        pos, 
        caixa,
        fonte_texto=fonte_pygame, 
        cor_texto=(0, 0, 0), 
        padding = screen.get_width() / 10
            ):
        box = pygame.image.load(caixa)
        largura = surface.get_width()
        altura = surface.get_height()
        caixa_redimensionada = pygame.transform.scale(box, (largura/2, altura/2))
        box_rect = caixa_redimensionada.get_rect(topleft=pos)
        surface.blit(caixa_redimensionada, box_rect)
        


        palavras = mensagem.split(' ')
        linhas = []
        max_larg = box_rect.width - 2 * padding
        linha_atual = ""

        for palavra in palavras:
            if len(linha_atual + ' ' + palavra) <= 40:
                if linha_atual == "":
                    linha_atual = palavra
                else:
                    linha_atual += ' ' + palavra
            else:
                linhas.append(linha_atual)
                linha_atual = palavra
        if linha_atual:
            linhas.append(linha_atual)

        x = box_rect.left + padding
        y = box_rect.top + padding

        for linha in linhas:
            texto = fonte_texto.render(linha, True, cor_texto)
            surface.blit(texto, (x, y))
            y += texto.get_height() + 4
    def teste_dialogo():
        dialogo(screen, "batata", (200, 100), "imagens/personagens/caixa_dialogo.png")

    screen.blit(background_menu, (0, 0))
    execution = True
    while execution:
        if estado == "MENU":
            botao_rect, botao_func = button_create(screen, "imagens/botoes/jogar.png", (300, 250), (200, 100), start)
        elif estado == "JOGO":
            screen.blit(background_jogo, (0, 0))
            teste_dialogo()
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
        await asyncio.sleep(0)
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())