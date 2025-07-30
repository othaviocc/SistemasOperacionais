import threading
import time
import logging

class Filosofo(threading.Thread):
    def __init__(self, id, hashi_esquerda, hashi_direita):
        threading.Thread.__init__(self)
        self.id = id
        self.hashi_esquerda = hashi_esquerda
        self.hashi_direita = hashi_direita

    def pensar(self): #filosofo pensa por um instante
        logging.info("Filósofo %s está pensando.", self.id)
        time.sleep(1)

    def comer(self): #quando pega os dois hashis ele come por 1s
        logging.info("Filósofo %s está comendo.", self.id)
        time.sleep(1)
        logging.info("Filósofo %s terminou de comer.", self.id) #terminou de comer

    def run(self):
        while True: #while onde o filosofo nunca para de tentar comer e pensar
            self.pensar()

            pegou_hashi_esquerda = self.hashi_esquerda.acquire(timeout=1)
            if not pegou_hashi_esquerda: #se nao pegou o hashi volta a pensar
                continue

            pegou_hashi_direita = self.hashi_direita.acquire(timeout=1)
            if not pegou_hashi_direita: #se nao pegou o da direita, libera o da esuerda e volta a pensar
                self.hashi_esquerda.release()
                continue
            #se conseguiu pegar os dois, come e depois libera os hashis
            self.comer()
            self.hashi_direita.release()
            self.hashi_esquerda.release()

def main():
    N = int(input("Número de filósofos: ")) #pergunta o n. de filosofos
    hashis = [threading.Lock() for _ in range(N)] #cria uma lista de Locks, um para cada hashi
    filosofos = []

    format = "%(asctime)s: %(message)s" #formato logs
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    logging.info("Main: iniciando threads dos filósofos")

    for i in range(N): #Criação threads
        f = Filosofo(i, hashis[(i + 1) % N], hashis[i])  #recebe hashi a esquerda e direita
        filosofos.append(f)
        logging.info("Main: iniciando filósofo %s", i)
        f.start() #inicia a thread, vai pro run

    for f in filosofos: #espera pelas threads, como roda em whike true, nunca terminam
        f.join()

if __name__ == "__main__":
    main()
