import random
import time
from eventos import random_evento_obg, random_evento_escolha
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

j1 = Jogador("j1", "Brasil")
j2 = Jogador("j2", "Franca")

rodadas = 1
vez = 1

def acessar_itens(jogador):
    if not jogador.itens:
        print ("Você não possui itens")
    else:
        for i in range(len(jogador.itens)):
            print(jogador.itens[i - 1])
        print ("Deseja usar algum deles? Se sim, digite o nome do item, se não, digite sair")


def rodada(jogador):
    time.sleep(5)
    random_evento_obg(jogador)
    time.sleep(5)
    random_evento_escolha(jogador)
    jogador.itens.append(itens_pendentes)
    itens_pendentes.clear()

def turno():
    global vez, rodadas
    if vez == 1:
        player_atual = j1
        print (f"Vez de {player_atual.nome}")
        time.sleep(2.5)
        rodada(player_atual)
        vez +=1
    elif vez ==2:
        print(f"Vez de {player_atual.nome}")
        time.sleep(2.5)
        rodada(player_atual)
        vez -=1
        rodadas += 1

if __name__ == "__main__":
    while True:
        turno()
        time.sleep(5)
    