import random
import os
import time

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def mina(self):
    limpar_terminal()
    print("Cidadão: Rei! eu achei esta pequena quantia de ouro e gostaria de dividir com o reino!")
    print(" (+5 dinheiro)")
    self.dinheiro += 5
    time.sleep(3)
    print (f"Status de {self.nome}({self.pais}): ")
    print(f"Saude: {self.saude}")
    print(f"Satisfação da população: {self.satisfacao}")
    print(f"Dinheiro: {self.dinheiro}")
    time.sleep(5)

def furto(self):
    limpar_terminal()
    print("Guarda: Rei, identificamos um ladrão, mas não conseguimos impedir completamente o furto")
    print(" (-5 dinheiro)")
    self.dinheiro -= 5
    time.sleep(3)
    print (f"Status de {self.nome}({self.pais}): ")
    print(f"Saude: {self.saude}")
    print(f"Satisfação da população: {self.satisfacao}")
    print(f"Dinheiro: {self.dinheiro}")
    time.sleep(5)

eventos_obg = [mina, furto]

def pandemia(self):
    print ("Médico: Atenção, rei! Nosso reino está sofrendo uma pandemia, o senhor precisa investir mais na saúde! \n" \
    " (S/N)")
    while True:
        resposta = input().strip().upper()
        if resposta == "S":
            time.sleep(5)
            print("Médico: Muito obrigado, rei!")
            self.dinheiro -= 20
            self.saude += 10
            self.satisfacao += 20
            time.sleep(5)
            print (f"Status de {self.nome}({self.pais}): ")
            print(f"Saude: {self.saude}")
            print(f"Satisfação da população: {self.satisfacao}")
            print(f"Dinheiro: {self.dinheiro}")
            break
        elif resposta == "N":
            time.sleep(5)
            print("Médico: Pessoas poderão morrer com sua escolha.")
            self.saude -=10
            self.satisfacao -=20
            time.sleep(5)
            print (f"Status de {self.nome}({self.pais}): ")
            print(f"Saude: {self.saude}")
            print(f"Satisfação da população: {self.saude}")
            print(f"Dinheiro: {self.saude}")
            break
        else:
            print ("Por favor, digite apenas S ou N")
    
eventos_escolha = [pandemia]

def random_evento_obg(self):
    evento_escolhido = random.choice(eventos_obg)
    evento_escolhido(self)

def random_evento_escolha(self):
    evento_escolhido = random.choice(eventos_escolha)
    evento_escolhido(self)