import threading
import logging
import time
import random

N = 5  # número de filósofos (e de hashis)

# Criação de 1 hashi (lock) entre cada par de filósofos
hashis = [threading.Lock() for _ in range(N)]

def filosofar(filosofo_id):
    esquerda = filosofo_id
    direita = (filosofo_id + 1) % N

    while True:
        logging.info("Filósofo %d está pensando", filosofo_id)
        time.sleep(random.uniform(0.5, 1.5))  # tempo para pensar

        logging.info("Filósofo %d tenta pegar o hashi esquerdo (%d)", filosofo_id, esquerda)
        acquired_left = hashis[esquerda].acquire(timeout=1)

        if not acquired_left:
            logging.info("Filósofo %d não conseguiu o hashi esquerdo. Voltando a pensar.", filosofo_id)
            continue

        logging.info("Filósofo %d pegou o hashi esquerdo (%d), tenta o direito (%d)", filosofo_id, esquerda, direita)
        acquired_right = hashis[direita].acquire(timeout=1)

        if not acquired_right:
            logging.info("Filósofo %d não conseguiu o hashi direito. Solta o esquerdo e volta a pensar.", filosofo_id)
            hashis[esquerda].release()
            continue

        # Se pegou os dois hashis
        logging.info("Filósofo %d está comendo", filosofo_id)
        time.sleep(random.uniform(0.5, 1.0))  # tempo para comer

        # Solta os hashis após comer
        hashis[esquerda].release()
        hashis[direita].release()
        logging.info("Filósofo %d terminou de comer e soltou os hashis", filosofo_id)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    threads = []

    for i in range(N):
        t = threading.Thread(target=filosofar, args=(i,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
