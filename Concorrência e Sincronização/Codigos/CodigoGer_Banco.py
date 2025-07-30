#4) Você foi contratado pelo C3 (Clube do Capitalismo Compulsivo) para desenvolver um sistema de gerenciamento de um banco. 
# Sua principal tarefa é desenvolver um sistema que evite que múltiplas operações sejam realizadas em uma mesma conta bancária de forma simultânea. 
# Assuma que, para cada conta corrente, você possui tanto o seu identificador como o saldo disponível.  
# Crie diversas threads para simular sequências de operações em paralelo e, aleatoriamente, defina qual conta receberá a operação, 
# o tipo de operação (crédito ou débito), e o valor da operação. Realize simulações com diferentes números de threads. 
# Após, assuma que existe uma nova operação que realiza a consulta do saldo. 
# A principal diferença para esta operação é que até 5 threads podem consultar o saldo de uma conta simultaneamente, 
# desde que nenhuma outra thread esteja realizando uma operação de crédito ou débito. 
# Operações de débito e crédito continuam precisando de acesso exclusivo aos registros da conta para executarem adequadamente.

import threading
import time
import random

NUM_CONTAS = 8
NUM_THREADS = 20

print_lock = threading.Lock() # Faz o lock do print para duas ou mais threads não utilizarem a mesma linha

class Account:
    def __init__(self, id, balance):
        self.id = id
        self.balance = balance
        self.readers = 0
        self.writing = False
        self.max_readers = threading.Semaphore(5) # Número máximo de leitores permitidos
        self.writer_mutex = threading.Lock() #Lock de escrita

accounts = [Account(i, random.randint(100, 2000)) for i in range(NUM_CONTAS)] # Cria as contas com saldo aleatório e id contínuo

def operation(thread_id):
    type = random.choice(['credito', 'debito', 'consulta']) # Seleciona uma das três operações
    account = random.choice(accounts) # Seleciona uma das contas
    value = random.randint(2000, 100000)/100 # Seleciona um valor entre 20.00 e 1000.00

    if type in ['credito', 'debito']: # Se for uma operação de escrita
        with account.writer_mutex: # Lock de escrita para não mexer na mesma conta simultaneamente
            account.writing = True # Transforma a variável "escrevendo" em True
            while account.readers > 0: # Enquanto ainda há leitores ativos espera
                pass

            with print_lock:
                print(f"Thread {thread_id:02d}: {type.capitalize()} de R$ {value:.2f} na conta {account.id}")
            time.sleep(3)

            if type == 'credito':
                account.balance += value

            elif type == 'debito':
                account.balance -= value

            account.writing = False # Transforma a variável "escrevendo" em False


    else: #type == 'consulta'
        while account.writing: # Enquanto a variável "escrevendo" for verdadeira a thread espera
            pass

        account.max_readers.acquire() # Acquire de uma thread (até 5)
        account.readers += 1 # Adiciona um leitor

        with print_lock:
            print(f"Thread {thread_id:02d}: Consultando saldo da conta {account.id}: R${account.balance:.2f}")
        time.sleep(3)

        account.max_readers.release() # Release da thread
        account.readers -= 1 # Remove o leitor

threads = []

for i in range(NUM_THREADS):
    t = threading.Thread(target=operation, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("\nSaldos finais:")
for acc in accounts:
    print(f"Saldo da conta {acc.id}: R$ {acc.balance:.2f}")