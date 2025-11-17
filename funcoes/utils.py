import os
import time

def limpar_ecra():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar(segundos=1):
    time.sleep(segundos)

def input_enter():
    input("\nPrima Enter voltar.")