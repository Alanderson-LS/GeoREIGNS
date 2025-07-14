import pygame
import asyncio
import random
import math
import sys
from recursos import itens_pendentes 

CATALOGO_PAISES = {
    "Guiana Brasileira": {
        "dinheiro": 70,
        "satisfacao": 65,
        "saude": 55,
        "exercito": 50,
        "tecnologia": 60,
        "religiosidade": 50
    },
    "Velha Zelândia": {
        "dinheiro": 50,
        "satisfacao": 50,
        "saude": 60,
        "exercito": 70,
        "tecnologia": 75,
        "religiosidade": 45
    },
    "Basilicio": {
        "dinheiro": 50,
        "satisfacao": 60,
        "saude": 70,
        "exercito": 50,
        "tecnologia": 70,
        "religiosidade": 50
    },
    "Nananá": {
        "dinheiro": 45,
        "satisfacao": 75,
        "saude": 60,
        "exercito": 50,
        "tecnologia": 50,
        "religiosidade": 70
    },
    "Arabia Maldita": {
        "dinheiro": 65,
        "satisfacao": 55,
        "saude": 50,
        "exercito": 70,
        "tecnologia": 30,
        "religiosidade": 80
    },
    
}

class Jogador:
    def __init__(self, nome, pais):
        ficha = CATALOGO_PAISES[pais]
        self.nome = nome
        self.pais = pais
        self.dinheiro = ficha["dinheiro"]
        self.saude = ficha["saude"]
        self.satisfacao = ficha["satisfacao"]
        self.exercito = ficha["exercito"]
        self.tecnologia = ficha["tecnologia"]
        self.religiosidade = ficha["religiosidade"]
        self.esta_derrotado = False


WIDTH, HEIGHT = 800, 600
FPS = 60
WINDOW_NAME = "Teste GeoREIGNS"
FUNDO_MENU = "imagens/bg/fundo_base_intro.jpeg"
FUNDO_JOGO = "imagens/bg/castelo_interno.png"
MAX_ROUNDS_LIMIT = 20

EST_MENU = "MENU"
EST_JOGO = "JOGO"
EST_CONFIG = "CONFIG"
EST_FIM_JOGO = "FIM_JOGO"
estado_tela = EST_MENU

players = [
    Jogador("Jogador 1", "Guiana Brasileira"), 
    Jogador("Jogador 2", "Velha Zelândia"),
]
player_index = 0
rodada_atual = 1

evento_opcional_executado = False 
turno_em_andamento = False 

movimento_vertical = 10
movimento_horizontal = 5
arco = 0

FONT = None
bg_menu = None
bg_jogo = None
botao_jogar = None
botao_jogar_rect = None

input_boxes = []
active_box = None
textos_jogadores = ["jogador 1", "jogador 2"]
botao_confirmar = None
botao_confirmar_rect = None

def carregar_imagem(caminho: str, tam: tuple[int, int]):
    img = pygame.image.load(caminho).convert_alpha()
    return pygame.transform.scale(img, tam)

class InputBox:
    def __init__(self, x, y, w, h, texto=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.text = texto
        self.txt_surface = FONT.render(texto, True, pygame.Color('black'))
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = pygame.time.get_ticks()

    def handle_event(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
            if self.active:
                self.cursor_visible = True
                self.cursor_timer = pygame.time.get_ticks()
            return False

        if evento.type == pygame.KEYDOWN:
            if self.active:
                if evento.key == pygame.K_RETURN:
                    return True
                elif evento.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += evento.unicode 
                self.txt_surface = FONT.render(self.text, True, pygame.Color('black'))
                self.update_cursor()
                return False
        return False

    def update(self):   
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width
        self.update_cursor()

    def update_cursor(self):
        current_time = pygame.time.get_ticks()
        if self.active and current_time - self.cursor_timer > 500:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = current_time 

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 5 + self.txt_surface.get_width()
            pygame.draw.line(screen, pygame.Color('black'),
                             (cursor_x, self.rect.y + 5),
                             (cursor_x, self.rect.y + self.rect.h - 5), 2)
        pygame.draw.rect(screen, self.color, self.rect, 2)

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

def config_screen():
    global input_boxes, active_box, botao_confirmar, botao_confirmar_rect

    input_boxes = [
        InputBox(WIDTH//2 - 100, HEIGHT//2 - 60, 200, 32, textos_jogadores[0]),
        InputBox(WIDTH//2 - 100, HEIGHT//2, 200, 32, textos_jogadores[1])
    ]
    active_box = None

    try:
        botao_confirmar = carregar_imagem("imagens/botoes/confirmar.png", (200, 50))
    except:
        botao_confirmar = pygame.Surface((200, 50), pygame.SRCALPHA)
        pygame.draw.rect(botao_confirmar, (100, 200, 100), (0, 0, 200, 50))
        pygame.draw.rect(botao_confirmar, (0, 0, 0), (0, 0, 200, 50), 2)
        texto = FONT.render("CONFIRMAR", True, (0, 0, 0))
        botao_confirmar.blit(texto, (100 - texto.get_width()//2, 25 - texto.get_height()//2))
    
    botao_confirmar_rect = botao_confirmar.get_rect(center=(WIDTH//2, HEIGHT//2 + 80))

def player_update():
    global players
    for i, box in enumerate(input_boxes):
        if i < len(players):
            players[i].nome = box.text if box.text else f"jogador {i+1}"

def config_draw(screen):
    screen.fill((240, 240, 240))

    titulo = FONT.render("digite os nomes dos jogadores: ", True, (0, 0, 0))
    screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, HEIGHT//2 - 120))

    for box in input_boxes:
        box.draw(screen)

    screen.blit(botao_confirmar, botao_confirmar_rect)

    instrucoes = FONT.render("Clique nas caixas para editar, [ENTER] para confirmar", True, (100, 100, 100))
    screen.blit(instrucoes, (WIDTH//2 - instrucoes.get_width()//2, HEIGHT//2 + 120))

def dialogo(surface, mensagem, pos=None, caixa_img=None, cor_texto=(0, 0, 0), max_chars=40):
    if caixa_img is None:
        try:
            caixa_img = pygame.image.load("imagens/personagens/caixa_dialogo.png").convert_alpha()
        except:
            caixa_img = pygame.Surface((400, 200), pygame.SRCALPHA)
            pygame.draw.rect(caixa_img, (240, 240, 200), (0, 0, 400, 200))
            pygame.draw.rect(caixa_img, (0, 0, 0), (0, 0, 400, 200), 2)

    w_caixa = surface.get_width() // 2
    h_caixa = surface.get_height() // 2
    caixa_img_redimensionada = pygame.transform.scale(caixa_img, (w_caixa, h_caixa))
    
    if pos is None: 
        rect = caixa_img_redimensionada.get_rect(center=(400, 170))
    else: 
        rect = caixa_img_redimensionada.get_rect(topleft=pos)

    surface.blit(caixa_img_redimensionada, rect)

    palavras = mensagem.split()
    linhas, atual = [], ""
    for p in palavras:
        if FONT.size(atual + " " + p)[0] <= w_caixa - 80: 
            atual = (atual + " " + p).strip()
        else:
            linhas.append(atual)
            atual = p
    if atual:
        linhas.append(atual)

    x_texto = rect.left + 40
    y_texto = rect.top + 60
    for linha in linhas:
        img = FONT.render(linha, True, cor_texto)
        surface.blit(img, (x_texto, y_texto))
        y_texto += img.get_height() + 4

async def mostrar_dialogo_completo(surface, jogador, mensagens: list[str], fundo, status_callback, personagem_img=None, personagem_pos=(120, 300)):
    for msg in mensagens:
        waiting_for_space = True
        while waiting_for_space:
            surface.blit(fundo, (0, 0))
            if status_callback:
                status_callback(surface)
            if personagem_img:
                surface.blit(personagem_img, personagem_pos)
            dialogo(surface, msg)
            
            dica = FONT.render("[ESPAÇO] para continuar", True, (255, 255, 0))
            dialogo_rect = pygame.image.load("imagens/personagens/caixa_dialogo.png").get_rect()
            dialogo_rect.center = (surface.get_width() // 2, surface.get_height() - dialogo_rect.height // 2)
            
            surface.blit(dica, (WIDTH // 2 - dica.get_width() // 2, dialogo_rect.bottom + 5))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting_for_space = False
                    elif event.key == pygame.K_ESCAPE: 
                        pygame.quit()
                        sys.exit()
            await asyncio.sleep(0.01) 

async def mostrar_evento_com_cartas(surface, jogador, mensagens: list[str], personagem_img, callback_sim, callback_nao, fundo, status_callback):
    global arco
    
    await mostrar_dialogo_completo(surface, jogador, mensagens, fundo, status_callback, personagem_img)

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
    resultado_mensagem = "" 
    
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
                    resultado_mensagem = callback_sim() 
                    esperando_resposta = False
                elif carta_nao.is_clicked(event.pos):
                    resultado_mensagem = callback_nao()
                    esperando_resposta = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                esperando_resposta = False
        
        surface.blit(fundo, (0, 0))
        status_callback(surface)
        
        dialogo(surface, mensagens[-1]) 
        surface.blit(personagem_img, (120, 300))
        carta_sim.desenhar(surface)
        carta_nao.desenhar(surface)
        
        pygame.display.flip()
        await asyncio.sleep(0.01) 
   
    if resultado_mensagem:
        await mostrar_dialogo_completo(surface, jogador, [resultado_mensagem], fundo, status_callback, personagem_img)

async def mina_visual(surface, jogador, fundo=None, status=None):
    personagem = "Minerador"
    ganho = random.randint(3, 7)
    mensagens = [
        f"{personagem}: Rei, encontrei esta pequena quantia de ouro enquanto minerava!",
        "Como agradicmento pelo seu reinado, decidi contribuir para o reino.",
        f"(+{ganho} dinheiro)"
    ]
    jogador.dinheiro += ganho
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/minerador.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.Surface((100, 200), pygame.SRCALPHA)
        pygame.draw.rect(img_personagem, (200, 200, 150), (0, 0, 100, 200))

    await mostrar_dialogo_completo(surface, jogador, mensagens, fundo, status, img_personagem)

async def furto_visual(surface, jogador, fundo=None, status=None):
    personagem = "Guarda"
    dinheiro = random.randint(3, 7)
    mensagens = [
        f"{personagem}: Rei, lamento informar, mas houve um pequeno furto no tesouro.",
        "Perdemos algumas moedas importantes.",
        f"(-{dinheiro} dinheiro)"
    ]
    jogador.dinheiro -= dinheiro
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/guerreiro.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.Surface((100, 200), pygame.SRCALPHA)
        pygame.draw.rect(img_personagem, (150, 150, 150), (0, 0, 100, 200))

    await mostrar_dialogo_completo(surface, jogador, mensagens, fundo, status, img_personagem)

async def boa_colheita_visual(surface, jogador, fundo=None, status=None):
    personagem = "Camponês Feliz"
    dinheiro_ganho = random.randint(7, 12)
    satisfacao_ganha = random.randint(5, 10)
    mensagens = [
        f"{personagem}: Ótima notícia, Majestade! Tivemos uma colheita abundante este ano!",
        "Isso significa mais riquezas e felicidade para o povo!",
        f"Seu dinheiro aumentou em {dinheiro_ganho} unidades! (+{dinheiro_ganho} dinheiro)",
        f"A alegria do povo aumentou em {satisfacao_ganha} pontos! (+{satisfacao_ganha} satisfação)"
    ]
    jogador.dinheiro += dinheiro_ganho
    jogador.satisfacao += satisfacao_ganha
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/campones_feliz.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.Surface((100, 200), pygame.SRCALPHA)
        pygame.draw.rect(img_personagem, (100, 200, 100), (0, 0, 100, 200))

    await mostrar_dialogo_completo(surface, jogador, mensagens, fundo, status, img_personagem)

async def praga_na_colheita_visual(surface, jogador, fundo=None, status=None):
    personagem = ("Camponês Desesperado")
    dinheiro_perdido = random.randint(6, 11)
    satisfacao_perdida = random.randint(7, 12)
    mensagens = [
        f"{personagem}: Perdão, Majestade, mas uma praga atingiu nossas plantações!",
        "A colheita foi terrível, e o povo está faminto.",
        f"Seu dinheiro diminuiu em {dinheiro_perdido} unidades! (-{dinheiro_perdido} dinheiro)",
        f"A satisfação do povo diminuiu em {satisfacao_perdida} pontos! (-{satisfacao_perdida} satisfação)"
    ]
    jogador.dinheiro -= dinheiro_perdido
    jogador.satisfacao -= satisfacao_perdida
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/campones_preocupado.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.image.load("imagens/personagens/campones1.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))

    await mostrar_dialogo_completo(surface, jogador, mensagens, fundo, status, img_personagem)

async def nova_mina_visual(surface, jogador, fundo=None, status=None):  
    personagem = "Mestre de Minas"
    dinheiro_ganho = random.randint(10, 20)
    mensagens = [
        f"{personagem}: Meu rei, descobrimos uma nova jazida de minério!",
        "Isso trará grandes riquezas para o nosso reino!",
        f"Seu dinheiro aumentou em {dinheiro_ganho} unidades! (+{dinheiro_ganho} dinheiro)",
        f"A tecnologia aumentou em 5 pontos! (+5 tecnologia)"
    ]
    jogador.dinheiro += dinheiro_ganho
    jogador.tecnologia += 5
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/mestre_mina.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.image.load("imagens/personagens/minerador.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))

    await mostrar_dialogo_completo(surface, jogador, mensagens, fundo, status, img_personagem)

async def desabamento_mina_visual(surface, jogador, fundo=None, status=None):
    personagem = "Minerador Ferido"
    dinheiro_perdido = random.randint(5, 10)
    saude_perdida = random.randint(5, 10)
    mensagens = [
        f"{personagem}: Majestade, houve um desabamento em uma de nossas minas!",
        "Alguns trabalhadores se feriram e a produção será afetada.",
        f"Seu dinheiro diminuiu em {dinheiro_perdido} unidades! (-{dinheiro_perdido} dinheiro)",
        f"A saúde do povo diminuiu em {saude_perdida} pontos! (-{saude_perdida} saúde)"
    ]
    jogador.dinheiro -= dinheiro_perdido
    jogador.saude -= saude_perdida
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/minerador_ferido.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.image.load("imagens/personagens/minerador.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))

    await mostrar_dialogo_completo(surface, jogador, mensagens, fundo, status, img_personagem)

async def peregrinacao_religiosa_visual(surface, jogador, fundo=None, status=None):
    personagem = "Sacerdote"
    religiosidade_ganha = random.randint(10, 15)
    satisfacao_ganha = random.randint(5, 10)
    mensagens = [
        f"{personagem}: Meu Rei, uma grande peregrinação religiosa passou por nossas terras.",
        "A fé do povo foi fortalecida e trouxe bênçãos ao reino.",
        f"A religiosidade aumentou em {religiosidade_ganha} pontos! (+{religiosidade_ganha} religiosidade)",
        f"A satisfação do povo aumentou em {satisfacao_ganha} pontos! (+{satisfacao_ganha} satisfação)"
    ]
    jogador.religiosidade += religiosidade_ganha
    jogador.satisfacao += satisfacao_ganha
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/sacerdote.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.image.load("imagens/personagens/campones1.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))

    await mostrar_dialogo_completo(surface, jogador, mensagens, fundo, status, img_personagem)

async def fanatismo_religioso_visual(surface, jogador, fundo=None, status=None):
    personagem = "Fanático Religioso"
    satisfacao_perdida = random.randint(10, 15)
    dinheiro_perdido = random.randint(5, 10)
    mensagens = [
        f"{personagem}: REI! A heresia deve ser purificada!",
        "Alguns grupos religiosos estão causando discórdia e instabilidade.",
        f"A satisfação do povo diminuiu em {satisfacao_perdida} pontos! (-{satisfacao_perdida} satisfação)",
        f"Seu dinheiro diminuiu em {dinheiro_perdido} unidades devido a conflitos! (-{dinheiro_perdido} dinheiro)"
    ]
    jogador.satisfacao -= satisfacao_perdida
    jogador.dinheiro -= dinheiro_perdido
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/campones1.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.Surface((100, 200), pygame.SRCALPHA)
        pygame.draw.rect(img_personagem, (180, 100, 100), (0, 0, 100, 200))

    await mostrar_dialogo_completo(surface, jogador, mensagens, fundo, status, img_personagem)

async def avanco_tecnologico_visual(surface, jogador, fundo=None, status=None):
    personagem = "Inventor Curioso"
    tecnologia_ganha = random.randint(10, 15)
    dinheiro_gasto = random.randint(5, 10)
    mensagens = [
        f"{personagem}: Majestade, eu desenvolvi uma nova ferramenta que pode revolucionar nossa produção!",
        "Haverá um pequeno custo para implementá-la, mas o retorno será grande.",
        f"A tecnologia aumentou em {tecnologia_ganha} pontos! (+{tecnologia_ganha} tecnologia)",
        f"Seu dinheiro diminuiu em {dinheiro_gasto} unidades! (-{dinheiro_gasto} dinheiro)"
    ]
    jogador.tecnologia += tecnologia_ganha
    jogador.dinheiro -= dinheiro_gasto
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/inventor.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.image.load("imagens/personagens/campones1.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))

    await mostrar_dialogo_completo(surface, jogador, mensagens, fundo, status, img_personagem)

async def falha_infraestrutura_visual(surface, jogador, fundo=None, status=None):
    personagem = "Engenheiro Frustrado"
    saude_perdida = random.randint(8, 15)
    dinheiro_perdido = random.randint(10, 20)
    mensagens = [
        f"{personagem}: Infelizmente, meu Rei, uma ponte importante colapsou e uma estrada está intransitável.",
        "Isso afetará o comércio e o acesso à saúde.",
        f"A saúde do povo diminuiu em {saude_perdida} pontos! (-{saude_perdida} saúde)",
        f"Seu dinheiro diminuiu em {dinheiro_perdido} unidades para reparos! (-{dinheiro_perdido} dinheiro)"
    ]
    jogador.saude -= saude_perdida
    jogador.dinheiro -= dinheiro_perdido
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/inventor.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.image.load("imagens/personagens/campones1.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))

    await mostrar_dialogo_completo(surface, jogador, mensagens, fundo, status, img_personagem)

async def recrutamento_exercito_visual(surface, jogador, fundo=None, status=None):
    personagem = "Recrutador"
    exercito_ganho = random.randint(10, 15)
    satisfacao_perdida = random.randint(5, 10)
    mensagens = [
        f"{personagem}: Majestade, precisamos de mais homens para a guarda do reino!",
        "Começaremos um novo recrutamento para fortalecer nossas fronteiras.",
        f"Seu exército aumentou em {exercito_ganho} pontos! (+{exercito_ganho} exército)",
        f"A satisfação do povo diminuiu em {satisfacao_perdida} pontos (serviço obrigatório)! (-{satisfacao_perdida} satisfação)"
    ]
    jogador.exercito += exercito_ganho
    jogador.satisfacao -= satisfacao_perdida
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/guerreiro.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.image.load("imagens/personagens/campones1.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))

    await mostrar_dialogo_completo(surface, jogador, mensagens, fundo, status, img_personagem)

async def desercoes_exercito_visual(surface, jogador, fundo=None, status=None):
    personagem = "Capitão Preocupado"
    exercito_perdido = random.randint(8, 15)
    mensagens = [
        f"{personagem}: Lamento informar, Majestade, mas alguns soldados desertaram.",
        "Eles não suportaram a disciplina e fugiram durante a noite.",
        f"Seu exército diminuiu em {exercito_perdido} pontos! (-{exercito_perdido} exército)"
    ]
    jogador.exercito -= exercito_perdido
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/guarda.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.image.load("imagens/personagens/campones1.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))

    await mostrar_dialogo_completo(surface, jogador, mensagens, fundo, status, img_personagem)

def resposta_epidemia(jogador, resposta):
    if resposta:
        dinheiro = random.randint(15, 20)
        saude = random.randint(15, 20)
        satisfacao = random.randint(10, 15)
        jogador.dinheiro -= dinheiro
        jogador.saude += saude
        jogador.satisfacao += satisfacao
        return f"Você investiu na saúde! Epidemia controlada. (-{dinheiro} dinheiro, +{saude} saúde, +{satisfacao} satisfação)" 
    else:
        saude = random.randint(5, 10)
        satisfacao = random.randint(10, 15)
        jogador.saude -= saude
        jogador.satisfacao -= satisfacao
        return f"Você ignorou a epidemia. Saúde do reino piorou. (-{saude} saúde, -{satisfacao} satisfação)" 

async def epidemia_visual(surface, jogador, fundo=None, status=None):
    personagem = "Médico"
    mensagens = [
        f"{personagem}: Atenção, rei! Nosso reino sofre uma epidemia.",
        "Precisamos investir recursos na saúde para contê-la.",
        "Você poderia investir parte das riquezas para combater a epidemia?"
    ]
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/medico2.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.Surface((100, 200), pygame.SRCALPHA)
        pygame.draw.rect(img_personagem, (150, 150, 255), (0, 0, 130, 200))
    
    await mostrar_evento_com_cartas(
        surface, jogador, mensagens, img_personagem,
        lambda: resposta_epidemia(jogador, True),
        lambda: resposta_epidemia(jogador, False),
        fundo,
        status
    )

def resposta_demonio(jogador, resposta):
    religiosidade = random.randint(7, 13)
    if resposta:
        dado = random.randint(1, 6)
        saude = random.randint(3, 7)
        dinheiro = random.randint(3, 7)
        
        if dado <= 3:
            perda_saude = saude * (4 - dado)
            perda_dinheiro = dinheiro * (4 - dado)
            jogador.saude -= perda_saude
            jogador.dinheiro -= perda_dinheiro
            return f"Saiu um número {dado}, a sorte não caminha ao seu lado! (-{perda_saude} saúde, -{perda_dinheiro} dinheiro)" 
        else:
            ganho_saude = saude * (dado - 3)
            ganho_dinheiro = dinheiro * (dado - 3)
            jogador.saude += ganho_saude
            jogador.dinheiro += ganho_dinheiro
            return f"Um {dado}, até que sua sorte não anda mal! (+{ganho_saude} saúde, +{ganho_dinheiro} dinheiro)" 
    else:
        return "Você recusou a proposta do demônio. O reino segue seu curso normal." 

async def demonio_visual(surface, jogador, fundo=None, status=None):
    personagem = "Demônio"
    mensagens = [
        f"{personagem}: HAHAHA, rei, seus dias estão contados!",
        "Lhe trago uma proposta que pode mudar seu destino...",
        "Comigo trago um dado regular de 6 lados, quanto maior o número sorteado, melhor pra você.",
        "Agora, caso tire um número baixo, sinto muito... Encantador, não acha? ",
        "Você aceita fazer esse pacto comigo em troca de poder e riquezas, ou desgraça e pesadelos?"
    ]
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/demonio.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.Surface((100, 200), pygame.SRCALPHA)
        pygame.draw.rect(img_personagem, (255, 150, 150), (0, 0, 100, 200))

async def comerciante_viajante_visual(surface, jogador, fundo=None, status=None):
    personagem = "Comerciante Viajante"
    mensagens = [
        f"{personagem}: Salve, Majestade! Chegou um comerciante com mercadorias raras e exóticas.",
        "Ele oferece itens únicos que poderiam impulsionar a economia do reino,",
        "mas o custo é considerável. Deseja investir nas mercadorias dele?"
    ]
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/comerciante.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.image.load(random.choice(["imagens/personagens/campones1.png", "imagens/personagens/campones2.png"]))
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))

    def resposta_comerciante(jogador, resposta):
        if resposta:
            custo = random.randint(15, 25)
            ganho_dinheiro = random.randint(20, 35)
            ganho_satisfacao = random.randint(5, 10)
            jogador.dinheiro -= custo
            jogador.dinheiro += ganho_dinheiro
            jogador.satisfacao += ganho_satisfacao
            return f"Você investiu! O comércio floresceu. (-{custo} dinheiro, +{ganho_dinheiro} dinheiro, +{ganho_satisfacao} satisfação)"
        else:
            return "Você recusou a oferta. O reino segue sem mudanças significativas."

    await mostrar_evento_com_cartas(
        surface, jogador, mensagens, img_personagem,
        lambda: resposta_comerciante(jogador, True),
        lambda: resposta_comerciante(jogador, False),
        fundo,
        status
    )

async def festival_reino_visual(surface, jogador, fundo=None, status=None):
    personagem = random.choice(["Povo Alegre", "Organizador de Festas"])
    mensagens = [
        f"{personagem}: Majestade, o povo pede um grande festival para celebrar as últimas vitórias!",
        "Seria uma ótima maneira de levantar o moral, mas exigirá recursos.",
        "Você autoriza a realização do festival?"
    ]
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/campones_feliz.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.Surface((100, 200), pygame.SRCALPHA)
        pygame.draw.rect(img_personagem, (200, 150, 100), (0, 0, 100, 200))

    def resposta_festival(jogador, resposta):
        if resposta:
            custo = random.randint(10, 20)
            ganho_satisfacao = random.randint(20, 30)
            jogador.dinheiro -= custo
            jogador.satisfacao += ganho_satisfacao
            return f"O festival foi um sucesso! (-{custo} dinheiro, +{ganho_satisfacao} satisfação)"
        else:
            perda_satisfacao = random.randint(5, 10)
            jogador.satisfacao -= perda_satisfacao
            return f"Você negou o festival. O povo ficou desapontado. (-{perda_satisfacao} satisfação)"

    await mostrar_evento_com_cartas(
        surface, jogador, mensagens, img_personagem,
        lambda: resposta_festival(jogador, True),
        lambda: resposta_festival(jogador, False),
        fundo,
        status
    )

async def pedido_construcao_visual(surface, jogador, fundo=None, status=None):
    personagem = "Mestre de Obras"
    mensagens = [
        f"{personagem}: Rei, poderíamos construir uma nova ponte/torre de guarda para o reino.",
        "Isso melhoraria a infraestrutura e a segurança, mas requer mão de obra e materiais.",
        "Deseja iniciar esta grande obra?"
    ]
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/mestre_mina.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.image.load("imagens/personagens/campones1.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))

    def resposta_construcao(jogador, resposta):
        if resposta:
            custo = random.randint(10, 20)
            ganho_saude = random.randint(5, 10)
            ganho_tecnologia = random.randint(5, 10)
            jogador.dinheiro -= custo
            jogador.saude += ganho_saude
            jogador.tecnologia += ganho_tecnologia
            return f"A construção foi iniciada! (-{custo} dinheiro, +{ganho_saude} saúde, +{ganho_tecnologia} tecnologia)"
        else:
            return "Você decidiu não construir. As condições atuais persistem."

    await mostrar_evento_com_cartas(
        surface, jogador, mensagens, img_personagem,
        lambda: resposta_construcao(jogador, True),
        lambda: resposta_construcao(jogador, False),
        fundo,
        status
    )

async def disputa_fronteira_visual(surface, jogador, fundo=None, status=None):
    personagem = "General"
    mensagens = [
        f"{personagem}: Majestade, há uma disputa de terras na fronteira com um reino vizinho.",
        "Queremos enviar tropas para mostrar soberania, mas caso não seja de sua vontade, buscaremos um acordo de paz.",
        "Devemos enviar nossas tropas?"
    ]
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/guerreiro.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.image.load("imagens/personagens/campones1.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))

    def resposta_fronteira(jogador, resposta):
        if resposta:
            perda_exercito = random.randint(5, 10)
            ganho_dinheiro = random.randint(5, 15) if random.random() > 0.5 else 0
            perda_dinheiro = random.randint(5, 10) if ganho_dinheiro == 0 else 0
            if random.random() < 0.6:
                jogador.exercito -= perda_exercito
                jogador.dinheiro += ganho_dinheiro
                return f"Nossas tropas afirmaram a fronteira! (-{perda_exercito} exército, +{ganho_dinheiro} dinheiro)" if ganho_dinheiro > 0 else f"Nossas tropas afirmaram a fronteira, mas com perdas. (-{perda_exercito} exército, -{perda_dinheiro} dinheiro)"
            else:
                jogador.exercito -= perda_exercito * 2
                return f"A campanha militar falhou! Perdemos mais tropas. (-{perda_exercito * 2} exército, ao menos o conflito abaixou.)"
        else:
            ganho_satisfacao = random.randint(5, 10)
            if random.random() < 0.7:
                jogador.satisfacao += ganho_satisfacao
                return f"A negociação foi um sucesso! A paz prevalece. (+{ganho_satisfacao} satisfação)"
            else:
                perda_satisfacao = random.randint(5, 10)
                jogador.satisfacao -= perda_satisfacao
                return f"A negociação falhou. A tensão na fronteira aumentou. (-{perda_satisfacao} satisfação)"

    await mostrar_evento_com_cartas(
        surface, jogador, mensagens, img_personagem,
        lambda: resposta_fronteira(jogador, True),
        lambda: resposta_fronteira(jogador, False),
        fundo,
        status
    )

async def oferta_mago_visual(surface, jogador, fundo=None, status=None):
    personagem = "Mago Erudito"
    mensagens = [
        f"{personagem}: Saudações, Majestade! Vim de uma montanha distante oferecer-lhe um conhecimento arcano em troca de apoio.",
        "Isso pode impulsionar sua tecnologia, mas exigirá fundos e a tolerância de minha magia...",
        "Você aceita a ajuda do mago?"
    ]
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/mago.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.image.load("imagens/personagens/campones1.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))

    def resposta_mago(jogador, resposta):
        if resposta:
            custo = random.randint(10, 15)
            ganho_tecnologia = random.randint(15, 25)
            perda_religiosidade = random.randint(5, 10)
            jogador.dinheiro -= custo
            jogador.tecnologia += ganho_tecnologia
            jogador.religiosidade -= perda_religiosidade
            return f"Você aceitou a oferta! (+{ganho_tecnologia} tecnologia, -{custo} dinheiro, -{perda_religiosidade} religiosidade)"
        else:
            return "Você recusou a oferta do mago. O reino mantém suas tradições."

    await mostrar_evento_com_cartas(
        surface, jogador, mensagens, img_personagem,
        lambda: resposta_mago(jogador, True),
        lambda: resposta_mago(jogador, False),
        fundo,
        status
    )

async def crise_moral_visual(surface, jogador, fundo=None, status=None):
    personagem = "Sacerdote Preocupado"
    mensagens = [
        f"{personagem}: Meu Rei, a fé do povo está abalada. Há um crescente descontentamento.",
        "Podemos investir em templos e rituais para restaurar a fé, ou ignorar e focar em outras áreas.",
        "Qual sua decisão?"
    ]
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/sacerdote.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.image.load("imagens/personagens/campones1.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))

    def resposta_moral(jogador, resposta):
        if resposta:
            custo = random.randint(8, 15)
            ganho_religiosidade = random.randint(15, 20)
            ganho_satisfacao = random.randint(5, 10)
            jogador.dinheiro -= custo
            jogador.religiosidade += ganho_religiosidade
            jogador.satisfacao += ganho_satisfacao
            return f"Você investiu na fé! (+{ganho_religiosidade} religiosidade, +{ganho_satisfacao} satisfação, -{custo} dinheiro)"
        else:
            perda_religiosidade = random.randint(10, 15)
            perda_satisfacao = random.randint(8, 12)
            poupa_dinheiro = random.randint(8, 15)
            jogador.religiosidade -= perda_religiosidade
            jogador.satisfacao -= perda_satisfacao
            jogador.dinheiro += poupa_dinheiro
            return f"Você ignorou o problema. A moral do povo caiu. (-{perda_religiosidade} religiosidade, -{perda_satisfacao} satisfação, +{poupa_dinheiro} dinheiro economizado)"

    await mostrar_evento_com_cartas(
        surface, jogador, mensagens, img_personagem,
        lambda: resposta_moral(jogador, True),
        lambda: resposta_moral(jogador, False),
        fundo,
        status
    )

async def descoberta_cientifica_visual(surface, jogador, fundo=None, status=None):
    personagem = "Cientista Entusiasmado"
    mensagens = [
        f"{personagem}: Majestade, fizemos uma descoberta notável nos estudos!",
        "Poderíamos financiar mais pesquisas para avançar a ciência, ou focar em aplicações imediatas.",
        "Qual o seu comando?"
    ]
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/cientista.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.image.load("imagens/personagens/campones1.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))

    def resposta_cientifica(jogador, resposta):
        if resposta:
            custo = random.randint(12, 18)
            ganho_tecnologia = random.randint(18, 25)
            jogador.dinheiro -= custo
            jogador.tecnologia += ganho_tecnologia
            return f"Você financiou a pesquisa! (+{ganho_tecnologia} tecnologia, -{custo} dinheiro)"
        else:
            ganho_tecnologia = random.randint(5, 10)
            ganho_dinheiro = random.randint(5, 10)
            jogador.tecnologia += ganho_tecnologia
            jogador.dinheiro += ganho_dinheiro
            return f"Você focou na aplicação imediata. (+{ganho_tecnologia} tecnologia, +{ganho_dinheiro} dinheiro)"

    await mostrar_evento_com_cartas(
        surface, jogador, mensagens, img_personagem,
        lambda: resposta_cientifica(jogador, True),
        lambda: resposta_cientifica(jogador, False),
        fundo,
        status
    )

async def bandidos_nas_estradas_visual(surface, jogador, fundo=None, status=None):
    personagem = "Caminhante Assustado"
    mensagens = [
        f"{personagem}: Ajuda, Majestade! Bandidos estão atacando caravanas nas estradas!",
        "Precisamos de investimento em segurança com emergência!",
        "Qual a sua resposta? "
    ]
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/campones_preocupado.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.image.load("imagens/personagens/campones1.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))

    def resposta_bandidos(jogador, resposta):
        if resposta:
            custo = random.randint(10, 15)
            ganho_satisfacao = random.randint(5, 10)
            jogador.dinheiro -= custo
            jogador.satisfacao += ganho_satisfacao
            return f"Você fortaleceu a segurança (-{custo} dinheiro, +{ganho_satisfacao} satisfação)"
        else:
            perda_satisfacao = random.randint(8, 12)
            poupa_dinheiro = random.randint(5, 10)
            jogador.dinheiro += poupa_dinheiro
            jogador.satisfacao -= perda_satisfacao
            return f"Seu povo corre risco. (+{poupa_dinheiro} dinheiro poupado, -{perda_satisfacao} satisfação de sua população)"

    await mostrar_evento_com_cartas(
        surface, jogador, mensagens, img_personagem,
        lambda: resposta_bandidos(jogador, True),
        lambda: resposta_bandidos(jogador, False),
        fundo,
        status
    )

async def seca_prolongada_visual(surface, jogador, fundo=None, status=None):
    personagem = "Agricultor Idoso"
    mensagens = [
        f"{personagem}: Oh, Majestade, a seca está castigando nossas terras!",
        "As colheitas estão em risco, e o povo sofre com a falta de água.",
        "Devemos usar reservas de emergência para irrigação? "
    ]
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/anciao.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.image.load("imagens/personagens/campones1.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    def resposta_seca(jogador, resposta):
        if resposta:
            custo = random.randint(15, 25)
            ganho_saude = random.randint(10, 15)
            ganho_satisfacao = random.randint(10, 15)
            jogador.dinheiro -= custo
            jogador.saude += ganho_saude
            jogador.satisfacao += ganho_satisfacao
            return f"Você usou as reservas! A saúde e a moral do povo melhoraram. (-{custo} dinheiro, +{ganho_saude} saúde, +{ganho_satisfacao} satisfação)"
        else: 
            perda_saude = random.randint(10, 20)
            perda_satisfacao = random.randint(15, 25)
            poupa_dinheiro = random.randint(15, 25) 
            jogador.saude -= perda_saude
            jogador.satisfacao -= perda_satisfacao
            return f"A seca persiste. A saúde e a satisfação do povo pioraram. (-{perda_saude} saúde, -{perda_satisfacao} satisfação, ={poupa_dinheiro} dinheiro poupado)"

    await mostrar_evento_com_cartas(
        surface, jogador, mensagens, img_personagem,
        lambda: resposta_seca(jogador, True),
        lambda: resposta_seca(jogador, False),
        fundo,
        status
    )

async def refugiados_guerra_visual(surface, jogador, fundo=None, status=None):
    personagem = "Pai de Família Desabrigado"
    mensagens = [
        f"{personagem}: Por favor, Majestade, permita-nos entrar! Fugimos da guerra no reino vizinho.",
        "Ajudaremos com nossa mão de obra, mas precisamos de um lar e alimentação!",
        "Você abrirá as fronteiras do reino?"
    ]
    try:
        img_personagem = pygame.image.load("imagens/personagens/campones_preocupado.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.image.load("imagens/personagens/campones1.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))

    def resposta_refugiados(jogador, resposta):
        if resposta: 
            custo = random.randint(10, 20)
            ganho_satisfacao = random.randint(5, 10)
            jogador.dinheiro -= custo
            jogador.satisfacao += ganho_satisfacao
            return f"Você acolheu os refugiados! (-{custo} dinheiro, +{ganho_satisfacao} satisfação)"
        else:
            perda_satisfacao = random.randint(5, 10)
            perda_religiosidade = random.randint(3, 7)
            jogador.satisfacao -= perda_satisfacao
            jogador.religiosidade -= perda_religiosidade
            return f"Você recusou os refugiados. (-{perda_satisfacao} satisfação, -{perda_religiosidade} religiosidade)"

    await mostrar_evento_com_cartas(
        surface, jogador, mensagens, img_personagem,
        lambda: resposta_refugiados(jogador, True),
        lambda: resposta_refugiados(jogador, False),
        fundo,
        status
    )

async def torneio_reino_visual(surface, jogador, fundo=None, status=None):
    personagem = "Arauto Real"
    mensagens = [
        f"{personagem}: Majestade, o povo deseja um grandioso torneio para mostrar a força do reino!",
        "Seria uma exibição de poder e habilidade, elevando o moral, mas o custo seria alto.",
        "Deseja patrocinar o Torneio Real?"
    ]
    
    try:
        img_personagem = pygame.image.load("imagens/personagens/guerreiro.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.image.load("imagens/personagens/campones1.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    def resposta_torneio(jogador, resposta):
        if resposta: 
            custo = random.randint(10, 20)
            ganho_exercito = random.randint(5, 10) 
            ganho_satisfacao = random.randint(15, 25)
            jogador.dinheiro -= custo
            jogador.exercito += ganho_exercito
            jogador.satisfacao += ganho_satisfacao
            return f"O torneio foi espetacular, o povo ficou alegre, e os nossos soldados se fortaleceram! (-{custo} dinheiro, +{ganho_exercito} exército, +{ganho_satisfacao} satisfação)"
        else:
            perda_satisfacao = random.randint(5, 10)
            jogador.satisfacao -= perda_satisfacao
            return f"Você recusou o torneio. O povo ficou um pouco desanimado. (-{perda_satisfacao} satisfação)"

    await mostrar_evento_com_cartas(
        surface, jogador, mensagens, img_personagem,
        lambda: resposta_torneio(jogador, True),
        lambda: resposta_torneio(jogador, False),
        fundo,
        status
    )

async def game_over_visual(surface, jogador, mensagem_final, fundo=None, status=None):
    personagem = "Arauto Real"
    mensagens = [
        f"{personagem}: Atenção, Majestade! O destino do reino foi selado!",
        mensagem_final,
        "Pressione [ESC] para sair ou [ESPAÇO] se ainda tiver algum jogador sobrando."
    ]

    try:
        img_personagem = pygame.image.load("imagens/personagens/guerreiro.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))
    except:
        img_personagem = pygame.image.load("imagens/personagens/campones1.png")
        img_personagem = pygame.transform.scale(img_personagem, (100, 200))

    await mostrar_dialogo_completo(surface, jogador, mensagens, fundo, None, img_personagem)

async def checar_condicoes_fim_jogo(surface, jogador_checado, fundo, status):
    global estado_tela, turno_em_andamento, players, rodada_atual

    mensagem_derrota_individual = ""
    
    if jogador_checado.dinheiro <= 0:
        mensagem_derrota_individual = f"O dinheiro de {jogador_checado.nome} zerou! Sem grana, a população não prevalece."
    elif jogador_checado.saude <= 0:
        mensagem_derrota_individual = f"A saúde do povo de {jogador_checado.nome} zerou! Uma grande calamidade se abateu."
    elif jogador_checado.satisfacao <= 0:
        mensagem_derrota_individual = f"A satisfação do povo de {jogador_checado.nome} zerou! Uma revolução te tirou do poder e colocou um vendedor de bobbie goods no seu lugar."
    elif jogador_checado.exercito <= 0:
        mensagem_derrota_individual = f"O exército de {jogador_checado.nome} zerou! Após perceberem a fraqueza, um reino vizinho invadiu sua terra."
    elif jogador_checado.tecnologia <= 0:
        mensagem_derrota_individual = f"A tecnologia de {jogador_checado.nome} zerou! Seu povo foi tomado por um país com maiores avanços."
    elif jogador_checado.religiosidade <= 0:
        mensagem_derrota_individual = f"A religiosidade de {jogador_checado.nome} zerou! Sem fé, grande parte da população se encontrou sem razão para continuar ali."
    

    elif jogador_checado.dinheiro >= 100:
        mensagem_derrota_individual = f"O dinheiro de {jogador_checado.nome} atingiu o máximo! Mas a ganância consumiu o reino, e em seguida foi bombardeado pelos Estragos Unidos"
    elif jogador_checado.exercito >= 100:
        mensagem_derrota_individual = f"O exército de {jogador_checado.nome} atingiu o máximo! Mas a tirania militar dominou."
    elif jogador_checado.tecnologia >= 100:
        mensagem_derrota_individual = f"A tecnologia de {jogador_checado.nome} atingiu o máximo! Mas a ciência sem controle trouxe o caos."
    elif jogador_checado.religiosidade >= 100:
        mensagem_derrota_individual = f"A religiosidade de {jogador_checado.nome} atingiu o máximo! Mas o fanatismo destruiu a razão."

    if mensagem_derrota_individual:
        jogador_checado.esta_derrotado = True
        await game_over_visual(surface, jogador_checado, mensagem_derrota_individual, fundo, status)


    todos_derrotados = all(p.esta_derrotado for p in players)
    if todos_derrotados:
        turno_em_andamento = False
        estado_tela = EST_FIM_JOGO
        return True 
    if rodada_atual > MAX_ROUNDS_LIMIT and player_index == 0:
        turno_em_andamento = False
        estado_tela = EST_FIM_JOGO
        await game_over_visual(surface, players[0], f"O reino atingiu {MAX_ROUNDS_LIMIT} rodadas! O tempo se esgotou.", fundo, status)
        return True 

    return False 

eventos_obrigatorios = [
    mina_visual, furto_visual,
    boa_colheita_visual, praga_na_colheita_visual,
    nova_mina_visual, desabamento_mina_visual,
    peregrinacao_religiosa_visual, fanatismo_religioso_visual,
    avanco_tecnologico_visual, falha_infraestrutura_visual,
    recrutamento_exercito_visual, desercoes_exercito_visual
]
eventos_opcionais = [
    epidemia_visual, demonio_visual,
    comerciante_viajante_visual, festival_reino_visual,
    pedido_construcao_visual, disputa_fronteira_visual,
    oferta_mago_visual, crise_moral_visual,
    descoberta_cientifica_visual, bandidos_nas_estradas_visual,
    seca_prolongada_visual, refugiados_guerra_visual,
    torneio_reino_visual
]

async def proximo_turno():
    global player_index, turno_em_andamento, rodada_atual, estado_tela

    if all(p.esta_derrotado for p in players) or rodada_atual > MAX_ROUNDS_LIMIT:
        turno_em_andamento = False
        estado_tela = EST_FIM_JOGO
        return

    jogador_atual = None
    jogadores_tentados = 0
    while jogadores_tentados < len(players):
        temp_jogador = players[player_index]
        if not temp_jogador.esta_derrotado:
            jogador_atual = temp_jogador
            break
        alternar_jogador()
        jogadores_tentados += 1

    if jogador_atual is None:
        turno_em_andamento = False
        estado_tela = EST_FIM_JOGO
        return
    
    turno_em_andamento = True

    evento_obg = random.choice(eventos_obrigatorios)
    await evento_obg(screen, jogador_atual, fundo=bg_jogo, status=desenhar_status)

    if await checar_condicoes_fim_jogo(screen, jogador_atual, bg_jogo, desenhar_status):

        if estado_tela == EST_FIM_JOGO:
            turno_em_andamento = False
            return

        turno_em_andamento = False
        alternar_jogador()
        return

    if not jogador_atual.esta_derrotado:
        evento_opc = random.choice(eventos_opcionais)
        await evento_opc(screen, jogador_atual, fundo=bg_jogo, status=desenhar_status)
        dialogo(screen, "(Fim do turno, passe para o próximo jogador)")
        pygame.display.flip()
        await asyncio.sleep(5)

        if await checar_condicoes_fim_jogo(screen, jogador_atual, bg_jogo, desenhar_status):
            if estado_tela == EST_FIM_JOGO:
                turno_em_andamento = False
                return

    alternar_jogador()
    turno_em_andamento = False

def alternar_jogador():
    global player_index, rodada_atual
    player_index ^= 1
    if player_index == 0:
        rodada_atual += 1

def desenhar_status(surface):
    fonte = FONT
    jog = players[player_index]
    linhas = [
        f"Rodada: {rodada_atual}",
        f"Vez de: {jog.nome}",
        f"País: {jog.pais}",
        f"Dinheiro: {jog.dinheiro}",
        f"Saúde: {jog.saude}",
        f"Satisfação: {jog.satisfacao}",
        f"Exército: {jog.exercito}",
        f"Tecnologia: {jog.tecnologia}",
        f"Religiosidade: {jog.religiosidade}",
    ]
    y = 8
    for texto in linhas:
        img = fonte.render(texto, True, (255, 255, 255))
        surface.blit(img, (10, y))
        y += img.get_height() + 2

async def main():
    global estado_tela
    global bg_menu, bg_jogo, botao_jogar, botao_jogar_rect, screen, FONT
    global botao_confirmar, botao_confirmar_rect, turno_em_andamento
    global players, rodada_atual, player_index

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_NAME)
    clock = pygame.time.Clock()
    pygame.key.set_repeat(500, 50)


    init("fonte/MedievalSharp.ttf", 16)
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
        botao_jogar = carregar_imagem("imagens/botoes/jogar.png", (200, 70))
    except:
        botao_jogar = pygame.Surface((200, 100), pygame.SRCALPHA)
        pygame.draw.rect(botao_jogar, (100, 200, 100), (0, 0, 200, 100))
        pygame.draw.rect(botao_jogar, (0, 0, 0), (0, 0, 200, 100), 3)
        texto = FONT.render("JOGAR", True, (0, 0, 0))
        botao_jogar.blit(texto, (100 - texto.get_width()//2, 50 - texto.get_height()//2))

    botao_jogar_rect = botao_jogar.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    config_screen()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            if estado_tela == EST_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if botao_jogar_rect.collidepoint(event.pos):
                        
                        player_index = 0
                        rodada_atual = 1
                        turno_em_andamento = False
                        estado_tela = EST_CONFIG
            
            elif estado_tela == EST_CONFIG:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if botao_confirmar_rect.collidepoint(event.pos):
                        player_update()
                        estado_tela = EST_JOGO
                    else:
                        for box in input_boxes:
                            box.handle_event(event)

                elif event.type == pygame.KEYDOWN:
                    for box in input_boxes:
                        if box.handle_event(event):
                            if event.key == pygame.K_RETURN:
                                
                                player_update() 
                                estado_tela = EST_JOGO
                                break          
      
        if estado_tela == EST_MENU:
            screen.blit(bg_menu, (0, 0))
            screen.blit(botao_jogar, botao_jogar_rect)

        elif estado_tela == EST_CONFIG:
            config_draw(screen)
            for box in input_boxes:
                box.update()
                box.draw(screen)

        elif estado_tela == EST_JOGO:
            if not turno_em_andamento:
                if all(p.esta_derrotado for p in players):
                    estado_tela = EST_FIM_JOGO
                    jogador_para_exibir_fim = players[0] if players else None
                    await game_over_visual(screen, jogador_para_exibir_fim, "Todos os líderes foram derrotados! O jogo terminou.", bg_jogo, desenhar_status)

                elif rodada_atual > MAX_ROUNDS_LIMIT:
                    estado_tela = EST_FIM_JOGO
                    jogador_para_exibir_fim = players[0] if players else None
                    await game_over_visual(screen, jogador_para_exibir_fim, f"O reino atingiu {MAX_ROUNDS_LIMIT} rodadas! O tempo se esgotou.", bg_jogo, desenhar_status)
                else:
                    await proximo_turno()

            if estado_tela == EST_JOGO:
                screen.blit(bg_jogo, (0, 0))
                desenhar_status(screen)

        elif estado_tela == EST_FIM_JOGO:
            pass 

        pygame.display.flip()

        await asyncio.sleep(0.01)
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())