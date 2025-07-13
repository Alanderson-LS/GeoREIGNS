import pygame
import asyncio
import random
import math
import sys
import backend
from recursos import itens_pendentes

WIDTH, HEIGHT = 800, 600
FPS = 60
WINDOW_NAME = "Teste GeoREIGNS"
FUNDO_MENU = "imagens/bg/fundo_base_intro.jpeg"
FUNDO_JOGO = "imagens/bg/castelo_interno.png"

EST_MENU = "MENU"
EST_JOGO = "JOGO"
estado_tela = EST_MENU

players = [
    backend.Jogador("Jogador 1", "Brasil"),
    backend.Jogador("Jogador 2", "Franca"),
]
player_index = 0
rodada_atual = 1

mensagem_atual = ""
esperando_espaco = False
evento_opcional_executado = False

movimento_vertical = 10
movimento_horizontal = 5
arco = 0

FONT = None
bg_menu = None
bg_jogo = None
botao_jogar = None
bot_rect = None

def carregar_imagem(caminho: str, tam: tuple[int, int]):
    img = pygame.image.load(caminho).convert_alpha()
    return pygame.transform.scale(img, tam)

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
    try:
        FONT = pygame.font.Font(font_path, font_size)
    except:
        FONT = pygame.font.SysFont(None, font_size)

def dialogo(surface, mensagem, pos=(200, 25), caixa_img=None, cor_texto=(0, 0, 0), max_chars=40):
    if caixa_img is None:
        try:
            caixa_img = pygame.image.load("imagens/personagens/caixa_dialogo.png").convert_alpha()
        except:
            caixa_img = pygame.Surface((400, 200), pygame.SRCALPHA)
            pygame.draw.rect(caixa_img, (240, 240, 200), (0, 0, 400, 200))
            pygame.draw.rect(caixa_img, (0, 0, 0), (0, 0, 400, 200), 2)

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

def mina_visual(surface, jogador, personagem="Cidadão"):
    global mensagem_atual
    jogador.dinheiro += 5
    mensagem_atual = f"{personagem}: Rei, encontrei esta pequena quantia de ouro, e decidi contribuir para o reino. (+5 dinheiro)"

def furto_visual(surface, jogador, personagem="Guarda"):
    global mensagem_atual
    jogador.dinheiro -= 5
    mensagem_atual = f"{personagem}: Rei, houve um furto no tesouro. (-5 dinheiro)"

async def mostrar_evento_com_cartas(surface, jogador, mensagem, personagem_img, callback_sim, callback_nao, fundo, status):
    global arco, esperando_espaco
    
    try:
        img_sim = pygame.image.load("imagens/cartas/carta_sim.png")
        img_nao = pygame.image.load("imagens/cartas/carta_nao.png")
    except:
        img_sim = pygame.Surface((100, 150), pygame.SRCALPHA)
        pygame.draw.rect(img_sim, (200, 255, 200), (0, 0, 100, 150))
        pygame.draw.rect(img_sim, (0, 100, 0), (0, 0, 100, 150), 3)
        texto_sim = FONT.render("SIM", True, (0, 0, 0))
        img_sim.blit(texto_sim, (50 - texto_sim.get_width()//2, 75 - texto_sim.get_height()//2))
        
        img_nao = pygame.Surface((100, 150), pygame.SRCALPHA)
        pygame.draw.rect(img_nao, (255, 200, 200), (0, 0, 100, 150))
        pygame.draw.rect(img_nao, (100, 0, 0), (0, 0, 100, 150), 3)
        texto_nao = FONT.render("NÃO", True, (0, 0, 0))
        img_nao.blit(texto_nao, (50 - texto_nao.get_width()//2, 75 - texto_nao.get_height()//2))
    
    tamanho = (100, 150)
    img_sim = pygame.transform.scale(img_sim, tamanho)
    img_nao = pygame.transform.scale(img_nao, tamanho)
    
    base_x_sim = 70
    base_y_sim = 400
    base_x_nao = 730
    base_y_nao = 450
    
    carta_sim = Carta(base_x_sim, base_y_sim, img_sim, callback_sim)
    carta_nao = Carta(base_x_nao, base_y_nao, img_nao, callback_nao)
    
    esperando_resposta = True
    
    while esperando_resposta:
        arco += 0.005
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
                    return True
                elif carta_nao.is_clicked(event.pos):
                    carta_nao.callback()
                    esperando_resposta = False
                    return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                esperando_resposta = False
                return False
        
        surface.blit(fundo, (0, 0))
        status(surface)
        
        dialogo(surface, mensagem)
        surface.blit(personagem_img, (120, 300))
        carta_sim.desenhar(surface)
        carta_nao.desenhar(surface)
        
        pygame.display.flip()
        await asyncio.sleep(0)

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

async def epidemia_visual(surface, jogador, personagem="Médico", callback=None, fundo=None, status=None):
    
    global mensagem_atual
    mensagem_atual = f"{personagem}: Atenção, rei! Nosso reino sofre uma epidemia, precisa investir na saúde!"
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/campones1.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.Surface((100, 200), pygame.SRCALPHA)
        pygame.draw.rect(img_personagem, (150, 150, 255), (0, 0, 100, 200))
    
    await mostrar_evento_com_cartas(
        surface, jogador, mensagem_atual, img_personagem,
        lambda: resposta_epidemia(jogador, True),
        lambda: resposta_epidemia(jogador, False),
        fundo,
        status
    )
    if callback:
        callback()

async def demonio_visual(surface, jogador, personagem="Demônio", callback=None, fundo=None, status=None):
    """Evento opcional: demônio"""
    global mensagem_atual
    mensagem_atual = f"{personagem}: HAHAHA, rei, seus dias estão contados! Lhe trago uma proposta:"
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/campones1.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.Surface((100, 200), pygame.SRCALPHA)
        pygame.draw.rect(img_personagem, (255, 150, 150), (0, 0, 100, 200))
    
    await mostrar_evento_com_cartas(
        surface, jogador, mensagem_atual, img_personagem,
        lambda: resposta_demonio(jogador, True),
        lambda: resposta_demonio(jogador, False),
        fundo,
        status
    )
    if callback:
        callback()


eventos_obrigatorios = [mina_visual, furto_visual]
eventos_opcionais = [epidemia_visual, demonio_visual]

def proximo_turno():

    global mensagem_atual, esperando_espaco, evento_opcional_executado
    jogador = players[player_index]
    
    evento_opcional_executado = False
    evento_obg = random.choice(eventos_obrigatorios)
    
    evento_obg(screen, jogador)
    esperando_espaco = True

def alternar_jogador():
    global player_index, rodada_atual
    player_index ^= 1
    if player_index == 0:
        rodada_atual += 1
    proximo_turno()

def desenhar_status(surface):
    fonte = FONT
    jog = players[player_index]
    linhas = [
        f"Rodada: {rodada_atual}",
        f"Vez de: {jog.nome}",
        f"Dinheiro: {jog.dinheiro}",
        f"Saúde: {jog.saude}",
        f"Satisfação: {jog.satisfacao}",
    ]
    y = 8
    for texto in linhas:
        img = fonte.render(texto, True, (255, 255, 255))
        surface.blit(img, (10, y))
        y += img.get_height() + 2

async def main():
    global estado_tela, esperando_espaco, evento_opcional_executado
    global bg_menu, bg_jogo, botao_jogar, bot_rect, screen, FONT

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_NAME)
    clock = pygame.time.Clock()

    try:
        bg_menu = carregar_imagem(FUNDO_MENU, (WIDTH, HEIGHT))
    except:
        bg_menu = pygame.Surface((WIDTH, HEIGHT))
        bg_menu.fill((50, 50, 100))
    
    try:
        bg_jogo = carregar_imagem(FUNDO_JOGO, (WIDTH, HEIGHT))
    except:
        bg_jogo = pygame.Surface((WIDTH, HEIGHT))
        bg_jogo.fill((100, 80, 60))
    
    try:
        botao_jogar = carregar_imagem("imagens/botoes/jogar.png", (200, 100))
    except:
        botao_jogar = pygame.Surface((200, 100), pygame.SRCALPHA)
        pygame.draw.rect(botao_jogar, (100, 200, 100), (0, 0, 200, 100))
        pygame.draw.rect(botao_jogar, (0, 0, 0), (0, 0, 200, 100), 3)
        texto = FONT.render("JOGAR", True, (0, 0, 0))
        botao_jogar.blit(texto, (100 - texto.get_width()//2, 50 - texto.get_height()//2))
    
    bot_rect = botao_jogar.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    init("fonte/MedievalSharp.ttf", 16)
    iniciou_jogo = False
    running = True

    while running:
        if estado_tela == EST_MENU:
            screen.blit(bg_menu, (0, 0))
            screen.blit(botao_jogar, bot_rect)

        elif estado_tela == EST_JOGO:
            screen.blit(bg_jogo, (0, 0))
            desenhar_status(screen)

            if esperando_espaco and mensagem_atual:
                dialogo(screen, mensagem_atual)
                dica = FONT.render("[ESPAÇO] para continuar", True, (255, 255, 0))
                screen.blit(dica, (WIDTH // 2 - dica.get_width() // 2, HEIGHT - 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and estado_tela == EST_MENU:
                if bot_rect.collidepoint(event.pos):
                    estado_tela = EST_JOGO

            elif event.type == pygame.KEYDOWN and estado_tela == EST_JOGO:
                if event.key == pygame.K_SPACE and esperando_espaco:
                    if not evento_opcional_executado:
                        evento_opcional_executado = True
                        evento_opc = random.choice(eventos_opcionais)
                        await evento_opc(screen, players[player_index], fundo=bg_jogo, status=desenhar_status)
                    else:
                        esperando_espaco = False
                        alternar_jogador()
                elif event.key == pygame.K_ESCAPE:
                    running = False

        if estado_tela == EST_JOGO and not iniciou_jogo:
            proximo_turno()
            iniciou_jogo = True

        await asyncio.sleep(0)
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())