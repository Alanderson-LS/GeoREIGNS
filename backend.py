import os
import time
import random
from recursos import itens_pendentes, limpar_terminal

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
                    