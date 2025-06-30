import random
import time
from eventos import random_evento_obg, random_evento_escolha
from recursos import itens_pendentes
from backend import *

j1 = Jogador("j1", "Brasil")
j2 = Jogador("j2", "Franca")


if __name__ == "__main__":
    while True:
        turno(j1, j2)
        time.sleep(5)
    