import pygame, asyncio, random
import eventos                    
import backend                   

WIDTH, HEIGHT = 800, 600
FPS = 60
WINDOW_NAME = "Teste GeoREIGNS"
FUNDO_MENU = "imagens/bg/fundo_base_intro.jpeg"
FUNDO_JOGO = "imagens/bg/castelo_interno.png"

EST_MENU = "MENU"
EST_JOGO = "JOGO"
estado_tela = EST_MENU

players = [
    backend.Jogador("Jogador 1", "Brasil"),
    backend.Jogador("Jogador 2", "Franca"),
]
player_index = 0         
rodada_atual = 1

mensagem_atual = ""        
esperando_espaco = False   
evento_opcional_executado = False

def carregar_imagem(caminho: str, tam: tuple[int, int]):
    img = pygame.image.load(caminho).convert_alpha()
    return pygame.transform.scale(img, tam)

def proximo_turno():
    global mensagem_atual, esperando_espaco, evento_opcional_executado
    jogador = players[player_index]
    
    evento_opcional_executado = False
    evento_obg = random.choice(eventos.eventos_obrigatorios)
    
    if evento_obg in [eventos.epidemia_visual, eventos.demonio_visual]:
        evento_obg(pygame.display.get_surface(), jogador, fundo=bg_jogo)
    else:
        mensagem_atual = evento_obg(jogador)    
    esperando_espaco = True

def alternar_jogador():
    global player_index, rodada_atual
    player_index ^= 1               
    if player_index == 0:            
        rodada_atual += 1
    proximo_turno()

def desenhar_status(surface):
    fonte = eventos.FONT
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
    global bg_menu, bg_jogo, bot_rect, screen

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_NAME)
    clock = pygame.time.Clock()

    bg_menu = carregar_imagem(FUNDO_MENU, (WIDTH, HEIGHT))
    bg_jogo = carregar_imagem(FUNDO_JOGO, (WIDTH, HEIGHT))
    botao_jogar = carregar_imagem("imagens/botoes/jogar.png", (200, 100))
    bot_rect = botao_jogar.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    eventos.init("fonte/MedievalSharp.ttf", 16)

    iniciou_jogo = False

    running = True
    while running:
        if estado_tela == EST_MENU:
            screen.blit(bg_menu, (0, 0))
            screen.blit(botao_jogar, bot_rect)

        elif estado_tela == EST_JOGO:
            screen.blit(bg_jogo, (0, 0))
            desenhar_status(screen)

            if esperando_espaco and isinstance(mensagem_atual, str):
                eventos.dialogo(screen, mensagem_atual)
                dica = eventos.FONT.render("[ESPAÇO] para continuar", True, (255, 255, 0))
                screen.blit(dica, (WIDTH // 2 - dica.get_width() // 2, HEIGHT - 40))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            elif e.type == pygame.MOUSEBUTTONDOWN and estado_tela == EST_MENU:
                if bot_rect.collidepoint(e.pos):
                    estado_tela = EST_JOGO

            elif e.type == pygame.KEYDOWN and estado_tela == EST_JOGO:
                if e.key == pygame.K_SPACE and esperando_espaco:
                    if not evento_opcional_executado:
                        evento_opcional_executado = True
                        evento_opc = random.choice(eventos.eventos_opcionais)
                        evento_opc(screen, players[player_index], fundo=bg_jogo, status = desenhar_status)
                    else:
                        esperando_espaco = False
                        alternar_jogador()

        if estado_tela == EST_JOGO and not iniciou_jogo:
            proximo_turno()
            iniciou_jogo = True

        await asyncio.sleep(0)
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())