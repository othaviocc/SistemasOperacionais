import threading
import time

class Filosofo(threading.Thread):
    def __init__(self, id, hashi_esquerda, hashi_direita, refeicoes_totais):
        threading.Thread.__init__(self)
        self.id = id
        self.hashi_esquerda = hashi_esquerda
        self.hashi_direita = hashi_direita
        self.refeicoes_totais = refeicoes_totais
        self.numero_refeicoes = 0

    def pensar(self):
        print(f"Filósofo {self.id} está pensando.")
        time.sleep(1)

    def comer(self):
        print(f"Filósofo {self.id} está comendo.")
        time.sleep(1)
        print(f"Filósofo {self.id} terminou de comer.")

    def run(self):
        while self.numero_refeicoes < self.refeicoes_totais:
            self.pensar()

            pegou_hashi_esquerda = self.hashi_esquerda.acquire(timeout=1)
            if not pegou_hashi_esquerda:
                continue

            pegou_hashi_direita = self.hashi_direita.acquire(timeout=1)
            if not pegou_hashi_direita:
                self.hashi_esquerda.release()
                continue

            self.comer()
            self.numero_refeicoes += 1

            self.hashi_direita.release()
            self.hashi_esquerda.release()

        print(f"Filósofo {self.id} terminou todas as refeições.")

def main():
    N = int(input("Numero de filosofos: "))

    hashis = [threading.Lock() for _ in range(N)]
    filosofos = []

    for i in range(N):
        f = Filosofo(i, hashis[i], hashis[(i + 1) % N], N)
        filosofos.append(f)
        f.start()

    for f in filosofos:
        f.join()

    print("Todos os filosofos terminaram de comer.")

if __name__ == "__main__":
    main()
