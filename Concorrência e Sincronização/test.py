import threading
import time
import random

class Filosofo(threading.Thread):
    """
    Representa um filósofo na mesa de jantar.
    """
    def __init__(self, id, hashi_esquerda, hashi_direita, numero_total_filosofos):
        """
        Inicializa o filósofo.

        Args:
            id (int): Identificador do filósofo.
            hashi_esquerda (threading.Lock): O hashi à sua esquerda.
            hashi_direita (threading.Lock): O hashi à sua direita.
            numero_total_filosofos (int): O número total de filósofos na mesa.
        """
        threading.Thread.__init__(self)
        self.id = id
        self.hashi_esquerda = hashi_esquerda
        self.hashi_direita = hashi_direita
        # O último filósofo (com ID N-1) irá inverter a ordem de pegar os hashis
        # para prevenir o deadlock. Isso é uma implementação da solução de
        # ordenação de recursos (resource ordering).
        if self.id == numero_total_filosofos - 1:
            self.primeiro_hashi = self.hashi_direita
            self.segundo_hashi = self.hashi_esquerda
        else:
            self.primeiro_hashi = self.hashi_esquerda
            self.segundo_hashi = self.hashi_direita

    def pensar(self):
        """ Simula o filósofo pensando. """
        print(f"Filósofo {self.id} está pensando.")
        time.sleep(random.uniform(1, 3)) # Pensa por um tempo aleatório

    def comer(self):
        """ Simula o filósofo comendo. """
        print(f"--- Filósofo {self.id} está comendo. ---")
        time.sleep(random.uniform(1, 2)) # Come por um tempo aleatório
        print(f"Filósofo {self.id} terminou de comer e vai soltar os hashis.")

    def run(self):
        """
        O ciclo de vida do filósofo: pensar e depois tentar comer.
        """
        while True:
            self.pensar()

            print(f"Filósofo {self.id} está com fome e vai tentar pegar os hashis.")

            # O uso do 'with' garante que o lock será liberado automaticamente.
            # A lógica de ordenação (pegar sempre o hashi de menor índice primeiro,
            # que é implementada pela inversão no último filósofo) previne o deadlock.
            with self.primeiro_hashi:
                print(f"Filósofo {self.id} pegou o primeiro hashi.")
                time.sleep(0.1) # Pausa para aumentar a chance de disputa e demonstrar a solução
                with self.segundo_hashi:
                    print(f"Filósofo {self.id} pegou o segundo hashi.")
                    self.comer()
            
            # Os locks são liberados automaticamente ao sair dos blocos 'with'

def main():
    """
    Função principal que configura e inicia a simulação.
    """
    try:
        N = int(input("Digite o número de filósofos (e hashis): "))
        if N < 2:
            print("A simulação requer pelo menos 2 filósofos.")
            return
    except ValueError:
        print("Por favor, digite um número inteiro.")
        return

    # Cria uma lista de locks (hashis)
    hashis = [threading.Lock() for _ in range(N)]
    
    # Cria e inicia os filósofos
    filosofos = []
    for i in range(N):
        # O hashi da esquerda é o de mesmo índice que o filósofo.
        # O hashi da direita é o do próximo índice, com wrap-around (módulo N).
        hashi_esquerda = hashis[i]
        hashi_direita = hashis[(i + 1) % N]
        
        f = Filosofo(i, hashi_esquerda, hashi_direita, N)
        filosofos.append(f)
        f.start()
        
    # A thread principal espera que todas as threads de filósofos terminem
    # (neste caso, elas rodam em um loop infinito, então a thread principal
    # ficaria bloqueada aqui. Em um programa real, pode haver uma condição de parada).
    for f in filosofos:
        f.join()

if __name__ == "__main__":
    main()