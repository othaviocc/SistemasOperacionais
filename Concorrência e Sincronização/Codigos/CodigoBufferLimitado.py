import threading
import time
import random

BUFFER_TAM = 5
N_PROD = 2
N_CONSU = 2

buffer = []

espacos = threading.Semaphore(BUFFER_TAM) #produtor verifica para inserir produtos
itens = threading.Semaphore(0) #consumidor verifica para consumir
mutex = threading.Lock() #mutex que permite q apenas uma thread altere o conteúdo por vez

def produtor(id):
    while True:
        item = random.randint(1, 50) #produz um número aleatório

        if not espacos.acquire(blocking=False): #se não tiver espaços
            print(f"| Produtor {id} | Esperando espaço no buffer para produzir...")

            espacos.acquire()  #bloqueia produtor até conseguir espaço

        with mutex: #entra no mutex
            buffer.append(item) #adiciona o item no buffer
            print(f"| Produtor {id} | Produziu {item} | Buffer: {buffer} |")

        itens.release()#atualiza o semaphoro dos itens

        time.sleep(random.uniform(0.5, 4))#adiciona um tempo random para simular o tempo de produção

def consumidor(id):
    while True:
        if not itens.acquire(blocking=False): #se não tiver itens...
            print(f"| Consumidor {id} | Esperando item no buffer para consumir...")
            itens.acquire()  #bloqueia até ter itens disponiveis 

        with mutex: #entra no mutex
            item = buffer.pop(0) #retira o item do buffer
            print(f"| Consumidor {id} | Consumiu {item} | Buffer: {buffer} |")
        espacos.release() #atualiza o número de espacos

        time.sleep(random.uniform(0.5, 4))

for i in range(N_PROD): #inicializa as threads produtores
    threading.Thread(target=produtor, args=(i,), daemon=True).start()

for i in range(N_CONSU): #inicializa as threads consumidores
    threading.Thread(target=consumidor, args=(i,), daemon=True).start()

while True:
    time.sleep(1)
