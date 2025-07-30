import threading
import time
import random

# lê número de cadeiras
N = int(input("Número de cadeiras de espera: "))

clientes_esperando = []
mutex = threading.Semaphore(1)
barbeiro_dorme = threading.Semaphore(0)

def barbeiro():
    while True:
        barbeiro_dorme.acquire()  # espera cliente
        cortar_cabelo()

def cortar_cabelo():
    global clientes_esperando
    mutex.acquire()
    if clientes_esperando:
        cliente = clientes_esperando.pop(0)
        print(f"Barbeiro cortando cabelo do cliente {cliente}")
    mutex.release()
    time.sleep(random.uniform(1, 2))  # tempo do corte
    print("Barbeiro terminou um corte")

def cliente(i):
    global clientes_esperando
    mutex.acquire()
    if len(clientes_esperando) < N:
        clientes_esperando.append(i)
        print(f"Cliente {i} esperando")
        barbeiro_dorme.release()  # acorda barbeiro
    else:
        print(f"Cliente {i} foi embora")
    mutex.release()

# inicia barbeiro
threading.Thread(target=barbeiro, daemon=True).start()

# gera clientes
for i in range(10):
    time.sleep(random.uniform(0.5, 1.5))
    threading.Thread(target=cliente, args=(i,)).start()