import random
import time
from eventos import random_evento_obg, random_evento_escolha

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

j1 = Jogador("j1", "Brasil")
j2 = Jogador("j2", "Franca")

vez = 1
def rodada(jogador):
    time.sleep(5)
    random_evento_obg(jogador)
    time.sleep(5)
    random_evento_escolha(jogador)

def turno():
    global vez
    if vez == 1:
        print (f"Vez de {j1.nome}")
        time.sleep(2.5)
        rodada(j1)
        vez +=1
    elif vez ==2:
        print(f"Vez de {j2.nome}")
        time.sleep(2.5)
        rodada(j2)
        vez -=1

if __name__ == "__main__":
    while True:
        turno()
        time.sleep(5)
    