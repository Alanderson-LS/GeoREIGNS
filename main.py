import random
import time
from eventos import random_evento_obg, random_evento_escolha, limpar_terminal
from recursos import itens_pendentes
CATALOGO_PAISES = {
    "Brasil": {
        "dinheiro": 60,
        "satisfacao": 45,
        "saude": 55
    },
    "Franca": {
        "dinheiro": 55,
        "satisfacao": 60,
        "saude": 45
    }
}
class Jogador:
    def __init__(self, nome, pais):
        ficha = CATALOGO_PAISES[pais]
        self.nome = nome
        self.pais = pais
        self.dinheiro = ficha["dinheiro"]
        self.saude = ficha["saude"]
        self.satisfacao = ficha["satisfacao"]
        self.itens = []

    def ad_item(self, item):
        self.itens.append(item)

    def rem_item(self, item):
        if item in self.itens:
            self.itens.remove(item)
        else:
            print ("O jogador não possui o item a ser removido.")

    def acessar_itens(self):
        if len(self.itens) == 0:
            print ("Você não possui itens, faça outra escolha agora")
        else:
            for i in range(len(self.itens)):
                print(f"{i+ 1}. {self.itens[i]}")
            print ("Deseja usar algum deles? Se sim, digite o nome do item, se não, digite sair")
            while True:
                resposta = input().strip().upper()
                if resposta == "EXERCITO" or resposta == "EXÉRCITO":
                    self.itens.remove("exercito")
                if resposta == "SAIR":
                    break
                else:
                    print ("Insira uma resposta válida")

j1 = Jogador("j1", "Brasil")
j2 = Jogador("j2", "Franca")

rodadas = 1
vez = 1


def rodada(jogador):
    time.sleep(5)
    random_evento_obg(jogador)
    time.sleep(5)
    random_evento_escolha(jogador)
    jogador.itens.extend(itens_pendentes)
    itens_pendentes.clear()

def turno():
    global vez, rodadas
    limpar_terminal()
    if vez == 1:        
        player_atual = j1
        print (f"Vez de {player_atual.nome}")
        time.sleep(2.5)
        rodada(player_atual)
        time.sleep(2.5)
        while True:
            print (""" Escolha uma das alternativas:
                1. Itens
                2. terminar rodada""")
            escolha = input()
            if escolha == "1":
                player_atual.acessar_itens()
            elif escolha == "2":
                break
            else:
                print ("Digite uma alternativa válida")

        vez +=1
    elif vez ==2:
        player_atual = j2
        print(f"Vez de {player_atual.nome}")
        time.sleep(2.5)
        rodada(player_atual)
        while True:
            print (""" Escolha uma das alternativas:
                1. Itens
                2. terminar rodada""")
            escolha = input()
            if escolha == "1":
                player_atual.acessar_itens()
            elif escolha == "2":
                break
            else:
                print ("Digite uma alternativa válida")
                while True:
                    escolha = input()
                    if escolha == "1":
                        player_atual.acessar_itens()
                    elif escolha == "2":
                        break
            break
        vez -=1
        rodadas += 1

if __name__ == "__main__":
    while True:
        turno()
        time.sleep(5)
    