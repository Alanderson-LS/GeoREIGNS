import pygame
import random
import time 
from recursos import itens_pendentes

FONT = None

def init(font_path="fonte/MedievalSharp.ttf", font_size=16):
    global FONT
    pygame.font.init()
    FONT = pygame.font.Font(font_path, font_size)

def dialogo(
    surface,
    mensagem,
    pos=(200, 25),
    caixa_path="imagens/personagens/caixa_dialogo.png",
    cor_texto=(0, 0, 0),
    max_chars=40,
):
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

def mina(jogador):
    print(
        "Cidadão: Rei! eu achei esta pequena quantia de ouro e gostaria de dividir com o reino!"
    )
    print(" (+5 dinheiro)")
    jogador.dinheiro += 5
    time.sleep(3)
    print(f"Status de {jogador.nome}({jogador.pais}): ")
    print(f"Saude: {jogador.saude}")
    print(f"Satisfação da população: {jogador.satisfacao}")
    print(f"Dinheiro: {jogador.dinheiro}")
    time.sleep(5)


def furto(jogador):
    print(
        "Guarda: Rei, identificamos um ladrão, mas não conseguimos impedir completamente o furto"
    )
    print(" (-5 dinheiro)")
    jogador.dinheiro -= 5
    time.sleep(3)
    print(f"Status de {jogador.nome}({jogador.pais}): ")
    print(f"Saude: {jogador.saude}")
    print(f"Satisfação da população: {jogador.satisfacao}")
    print(f"Dinheiro: {jogador.dinheiro}")
    time.sleep(5)


eventos_obg = [mina, furto]


def pandemia(jogador):
    print(
        "Médico: Atenção, rei! Nosso reino está sofrendo uma pandemia, o senhor precisa investir mais na saúde! (S/N)"
    )
    while True:
        resp = input().strip().upper()
        if resp == "S":
            time.sleep(5)
            print("Médico: Muito obrigado, rei!")
            jogador.dinheiro -= 20
            jogador.saude += 10
            jogador.satisfacao += 20
            time.sleep(5)
            print(f"Status de {jogador.nome}({jogador.pais}): ")
            print(f"Saude: {jogador.saude}")
            print(f"Satisfação da população: {jogador.satisfacao}")
            print(f"Dinheiro: {jogador.dinheiro}")
            break
        elif resp == "N":
            time.sleep(5)
            print("Médico: Pessoas poderão morrer com sua escolha.")
            jogador.saude -= 10
            jogador.satisfacao -= 20
            time.sleep(5)
            print(f"Status de {jogador.nome}({jogador.pais}): ")
            print(f"Saude: {jogador.saude}")
            print(f"Satisfação da população: {jogador.satisfacao}")
            print(f"Dinheiro: {jogador.dinheiro}")
            break
        else:
            print("Por favor, digite apenas S ou N")


def demonio(jogador):
    print("Demônio: HAHAHA, rei, seus dias de reinado estão contados!")
    time.sleep(1)
    print(
        "Demônio: Lhe ofereço uma proposta, você pode rolar meu dado, mas números baixos contem coisas negativas, números altos podem te ajudar"
    )
    time.sleep(1)
    print("Demônio: Iai, temos um acordo ou está tremendo demais? ")
    print("responda com S/N")
    while True:
        resp = input().strip().upper()
        if resp == "S":
            time.sleep(2)
            print("Demônio: Vejo que você tem muita coragem, não? Vamos ver o que o dado nos diz")
            dado = random.randint(1, 6)
            if dado in (1, 2):
                print(f"Demônio: Ora, um {dado}, você tem bastante azar, HAHAHAHA")
                val1 = random.randint(15, 20) if dado == 1 else random.randint(10, 15)
                val2 = random.randint(15, 20) if dado == 1 else random.randint(10, 15)
                jogador.saude -= val1
                jogador.dinheiro -= val2
                print(f"Você perdeu {val1} de saúde e {val2} de dinheiro")
            elif dado in (3, 4):
                print(f"Demônio: Olha o que nós temos, {dado}, sorte e azar em equilíbrio.")
                val1 = random.randint(5, 10)
                val2 = random.randint(5, 10)
                if dado == 3:
                    jogador.saude -= val1
                    jogador.dinheiro -= val2
                    print(f"Você perdeu {val1} de saúde e {val2} de dinheiro")
                else:
                    jogador.saude += val1
                    jogador.dinheiro += val2
                    print(f"Você ganhou {val1} de saúde e {val2} de dinheiro")
            else:
                print(
                    f"Demônio: O QUE?? UM {dado}??? Você tem muita sorte, mas eu voltarei!"
                )
                if dado == 5:
                    val1 = random.randint(15, 20)
                    val2 = random.randint(15, 20)
                    jogador.saude += val1
                    jogador.dinheiro += val2
                    print(f"Você ganhou {val1} de saúde e {val2} de dinheiro")
                else:
                    print("Você ganhou um exército de uso único!")
                    print(
                        "Na aba 'itens' você pode usá-lo para saquear seu inimigo, e então você perderá este item"
                    )
                    itens_pendentes.append("exercito")
            break
        elif resp == "N":
            time.sleep(2)
            print("Demônio: Covarde! Nenhum status foi alterado.")
            break
        else:
            print("Por favor, digite apenas S ou N")


eventos_escolha = [pandemia, demonio]


def random_evento_obg(jogador):
    random.choice(eventos_obg)(jogador)


def random_evento_escolha(jogador):
    random.choice(eventos_escolha)(jogador)

def mina_visual(jogador, personagem="Cidadão"):
    """Altera status e DEVOLVE a fala para o pygame exibir."""
    jogador.dinheiro += 5
    return f"{personagem}: Rei! Encontrei ouro e desejo dividir com o reino (+5 dinheiro)"

def furto_visual(jogador, personagem="Guarda"):
    jogador.dinheiro -= 5
    return f"{personagem}: Rei, houve um furto no tesouro! (-5 dinheiro)"

def pandemia_visual(surface, jogador, personagem="Médico", callback=None):
    mensagem = f"{personagem}: Atenção, rei! Nosso reino sofre uma pandemia, precisa investir na saúde! (Clique SIM ou NÃO)"
    dialogo(surface, mensagem)

    pandemia_visual.callback = callback


def demonio_visual(surface, jogador, personagem="Demônio", callback=None):
    mensagem = f"{personagem}: HAHAHA, rei, seus dias estão contados! Aceita meu desafio? (Clique SIM ou NÃO)"
    dialogo(surface, mensagem)
    demonio_visual.callback = callback


def resposta_pandemia(jogador, resposta):
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
    else:
        pass

eventos_escolha_visuais = [
    (pandemia_visual, resposta_pandemia),
    (demonio_visual, resposta_demonio),
]

