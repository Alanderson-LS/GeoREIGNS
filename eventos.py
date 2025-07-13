import pygame
import random
import math
import sys
from recursos import itens_pendentes

FONT = None

movimento_vertical = 10
movimento_horizontal = 5
arco = 0

class Carta:
    def __init__(self, x, y, imagem, callback):
        self.image = imagem
        self.rect = self.image.get_rect(center=(x, y))
        self.callback = callback
        self.original_image = imagem.copy()
    
    def desenhar(self, surface):
        surface.blit(self.image, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def atualizar_posicao(self, x, y):
        self.rect.center = (x, y)

def init(font_path="fonte/MedievalSharp.ttf", font_size=16):
    global FONT
    pygame.font.init()
    FONT = pygame.font.Font(font_path, font_size)

def dialogo(surface, mensagem, pos=(200, 25), caixa_path="imagens/personagens/caixa_dialogo.png", cor_texto=(0, 0, 0), max_chars=40):
    caixa_img = pygame.image.load(caixa_path).convert_alpha()
    w, h = surface.get_size()
    caixa_img = pygame.transform.scale(caixa_img, (w // 2, h // 2))
    rect = caixa_img.get_rect(topleft=pos)
    surface.blit(caixa_img, rect)

    palavras = mensagem.split()
    linhas, atual = [], ""
    for p in palavras:
        if len(atual + " " + p) <= max_chars:
            atual = (atual + " " + p).strip()
        else:
            linhas.append(atual)
            atual = p
    if atual:
        linhas.append(atual)

    x = rect.left + 40
    y = rect.top + 60
    for linha in linhas:
        img = FONT.render(linha, True, cor_texto)
        surface.blit(img, (x, y))
        y += img.get_height() + 4

def mina_visual(jogador, personagem="Cidadão"):
    jogador.dinheiro += 5
    return {
        "mensagem": f"{personagem}: Rei! Encontrei ouro e desejo dividir com o reino (+5 dinheiro)",
        "imagem": "imagens/personagens/campones1.png"
    }

def furto_visual(jogador, personagem="Guarda"):
    jogador.dinheiro -= 5
    return {
        "mensagem": f"{personagem}: Rei, houve um furto no tesouro! (-5 dinheiro)",
        "imagem": "imagens/personagens/campones2.png"
    }

def mostrar_evento_com_cartas(surface, jogador, mensagem, personagem_img, callback_sim, callback_nao, fundo, status):
    global arco
    img_sim = pygame.image.load("imagens/cartas/carta_sim.png")
    img_nao = pygame.image.load("imagens/cartas/carta_nao.png")
    tamanho = (100, 150)
    img_sim = pygame.transform.scale(img_sim, tamanho)
    img_nao = pygame.transform.scale(img_nao, tamanho)
    
    base_x_sim = 70
    base_y_sim = 400
    base_x_nao = 730
    base_y_nao = 450
    
    carta_sim = Carta(base_x_sim, base_y_sim, img_sim, callback_sim)
    carta_nao = Carta(base_x_nao, base_y_nao, img_nao, callback_nao)
    
    clock = pygame.time.Clock()
    esperando_resposta = True
    
    while esperando_resposta:
        arco += 0.05
        
        offset_y = math.sin(arco) * movimento_vertical
        offset_x = math.cos(arco) * movimento_horizontal
        
        carta_sim.atualizar_posicao(base_x_sim + offset_x, base_y_sim + offset_y)
        carta_nao.atualizar_posicao(base_x_nao - offset_x, base_y_nao - offset_y)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if carta_sim.is_clicked(event.pos):
                    carta_sim.callback()
                    esperando_resposta = False
                elif carta_nao.is_clicked(event.pos):
                    carta_nao.callback()
                    esperando_resposta = False
        
        surface.blit(fundo, (0, 0))
        status(surface)
        
        dialogo(surface, mensagem)
        surface.blit(personagem_img, (120, 300))
        carta_sim.desenhar(surface)
        carta_nao.desenhar(surface)
        
        pygame.display.flip()
        clock.tick(60)

def epidemia_visual(surface, jogador, personagem="Médico", callback=None, fundo=None, status=None):
    mensagem = f"{personagem}: Atenção, rei! Nosso reino sofre uma epidemia, precisa investir na saúde!"
    img_personagem = pygame.image.load("imagens/personagens/campones1.png")
    mostrar_evento_com_cartas(
        surface, jogador, mensagem, img_personagem,
        lambda: resposta_epidemia(jogador, True),
        lambda: resposta_epidemia(jogador, False),
        fundo,
        status
    )
    if callback:
        callback()

def demonio_visual(surface, jogador, personagem="Demônio", callback=None, fundo=None, status = None):
    mensagem = f"{personagem}: HAHAHA, rei, seus dias estão contados! Lhe trago uma proposta:"
    img_personagem = pygame.image.load("imagens/personagens/campones1.png")
    mostrar_evento_com_cartas(
        surface, jogador, mensagem, img_personagem,
        lambda: resposta_demonio(jogador, True),
        lambda: resposta_demonio(jogador, False),
        fundo,
        status
    )
    if callback:
        callback()

def resposta_epidemia(jogador, resposta):
    if resposta:
        jogador.dinheiro -= 20
        jogador.saude += 10
        jogador.satisfacao += 20
    else:
        jogador.saude -= 10
        jogador.satisfacao -= 20

def resposta_demonio(jogador, resposta):
    if resposta:
        dado = random.randint(1, 6)
        if dado <= 2:
            jogador.saude -= 15
            jogador.dinheiro -= 15
        elif dado <= 4:
            jogador.saude -= 5
            jogador.dinheiro -= 5
        else:
            jogador.saude += 15
            jogador.dinheiro += 15

eventos_obrigatorios = [mina_visual, furto_visual]
eventos_opcionais = [epidemia_visual, demonio_visual]