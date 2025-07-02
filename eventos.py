import random
import os
import time
import pygame
from recursos import itens_pendentes



###eventos jogaveis pelo terminal

def mina(jogador):
    print("Cidadão: Rei! eu achei esta pequena quantia de ouro e gostaria de dividir com o reino!")
    print(" (+5 dinheiro)")
    jogador.dinheiro += 5
    time.sleep(3)
    print (f"Status de {jogador.nome}({jogador.pais}): ")
    print(f"Saude: {jogador.saude}")
    print(f"Satisfação da população: {jogador.satisfacao}")
    print(f"Dinheiro: {jogador.dinheiro}")
    time.sleep(5)

def furto(jogador):
    print("Guarda: Rei, identificamos um ladrão, mas não conseguimos impedir completamente o furto")
    print(" (-5 dinheiro)")
    jogador.dinheiro -= 5
    time.sleep(3)
    print (f"Status de {jogador.nome}({jogador.pais}): ")
    print(f"Saude: {jogador.saude}")
    print(f"Satisfação da população: {jogador.satisfacao}")
    print(f"Dinheiro: {jogador.dinheiro}")
    time.sleep(5)


eventos_obg = [mina, furto]

def pandemia(jogador):
    print ("Médico: Atenção, rei! Nosso reino está sofrendo uma pandemia, o senhor precisa investir mais na saúde! \n" \
    " (S/N)")
    while True:
        resposta = input().strip().upper()
        if resposta == "S":
            time.sleep(5)
            print("Médico: Muito obrigado, rei!")
            jogador.dinheiro -= 20
            jogador.saude += 10
            jogador.satisfacao += 20
            time.sleep(5)
            print (f"Status de {jogador.nome}({jogador.pais}): ")
            print(f"Saude: {jogador.saude}")
            print(f"Satisfação da população: {jogador.satisfacao}")
            print(f"Dinheiro: {jogador.dinheiro}")
            break
        elif resposta == "N":
            time.sleep(5)
            print("Médico: Pessoas poderão morrer com sua escolha.")
            jogador.saude -=10
            jogador.satisfacao -=20
            time.sleep(5)
            print (f"Status de {jogador.nome}({jogador.pais}): ")
            print(f"Saude: {jogador.saude}")
            print(f"Satisfação da população: {jogador.satisfacao}")
            print(f"Dinheiro: {jogador.dinheiro}")
            break
        else:
            print ("Por favor, digite apenas S ou N")
    
def demonio(jogador):
    print("Demônio: HAHAHA, rei, seus dias de reinado estão contados!")
    time.sleep(1)
    print("Demônio: Lhe ofereço uma proposta, você pode rolar meu dado, mas números baixos contem coisas negativas, números altos podem te ajudar")
    time.sleep(1)
    print("Demônio: Iai, temos um acordo ou está tremendo demais? ")
    print("responda com S/N")
    while True:
        resposta = input().strip().upper()
        if resposta == "S":
            time.sleep(5)
            print ("Demônio: vejo que você tem muita coragem, não? Vamos ver o que o dado nos diz")
            dado = random.randint(1, 6)
            if dado == 1 or dado == 2:
                print(f"Demônio: Ora, um {dado}, você tem bastante azar, HAHAHAHA")
                if dado == 1:
                    valor_1 = random.randint(15, 20)
                    valor_2 = random.randint(15, 20)
                    jogador.saude -= valor_1
                    jogador.dinheiro -= valor_2
                    print (f"Você perdeu {valor_1} de saude e {valor_2} de dinheiro")
                    break
                else:
                    valor_1 = random.randint(10, 15)
                    valor_2 = random.randint(10, 15)
                    jogador.saude -= valor_1
                    jogador.dinheiro -= valor_2
                    print (f"Você perdeu {valor_1} de saude e {valor_2} de dinheiro")
                    break
            elif dado == 3 or dado ==4:
                print (f"Demônio Olha o que nós temos, {dado}, sua sorte e seu azar parece em equílibrio, nada mal")
                if dado == 3:
                    valor_1 = random.randint(5, 10)
                    valor_2 = random.randint(5, 10)
                    jogador.saude -= valor_1
                    jogador.dinheiro -= valor_2
                    print (f"Você perdeu {valor_1} de saude e {valor_2} de dinheiro")
                    break
                else:
                    valor_1 = random.randint(5, 10)
                    valor_2 = random.randint(5, 10)
                    jogador.saude += valor_1
                    jogador.dinheiro += valor_2
                    print (f"Você ganhou {valor_1} de saude e {valor_2} de dinheiro")
                    break
            else:
                print (f"Demônio: O QUE?? UM {dado}??? Você tem bastante sorte, mas eu voltarei, e isso não se repetirá!")
                if dado == 5:
                    valor_1 = random.randint(15, 20)
                    valor_2 = random.randint(15, 20)
                    jogador.saude += valor_1
                    jogador.dinheiro += valor_2
                    print (f"Você ganhou {valor_1} de saude e {valor_2} de dinheiro")
                    break
                else:
                    print ("Você ganhou um exército de uso único!")
                    print ("Na aba 'itens' você pode usá-lo para saquear seu inimigo, e então você perderá este item")
                    print ("Para usar, basta digitar 'exercito' sem acento")
                    itens_pendentes.append("exercito")
                    break
                    
        elif resposta == "N":
            time.sleep(5)
            print("Demônio: Frouxo como sempre, covardes tombam antes de erguer a espada, MWAHAHA")
            print(" (nenhum de seus status foi alterado)")
            time.sleep(5)
            break
        else:
            print ("Por favor, digite apenas S ou N")

eventos_escolha = [pandemia, demonio]

def random_evento_obg(jogador):
    evento_escolhido = random.choice(eventos_obg)
    evento_escolhido(jogador)
        
def random_evento_escolha(jogador):
    evento_escolhido = random.choice(eventos_escolha)
    evento_escolhido(jogador)

###eventos que rodam no pygame
