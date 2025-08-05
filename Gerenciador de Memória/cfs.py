from substitutionAlgorithms import *
import heapq
from collections import deque

def run(processes, environment, substitution_algorithm):
    # seleciona algoritmo de substituição
    substitution_algorithm = {'fifo': Fifo,'mru': MRU,'nuf': NUF,'otimo': Otimo}[substitution_algorithm]

    if environment.mem_policy == 'global':
        total_molduras = environment.mem_size // environment.page_size #quantidade global de molduras
        molduras_global = [None] * total_molduras  # estrutura da RAM global / espaços todas as molduras
        owner_map = [None] * total_molduras #dono de cada page
    else:
        # calcula quantas molduras cada processo pode usar
        molduras_por_processo = [int((process.mem_qty * environment.aloc_percentual / 100) // environment.page_size) for process in processes]  # vetor com as molduras (frames) alocadas para cada processo
        # RAM local por processo (molduras inicialmente vazias)
        molduras_local = [[None] * molduras for molduras in molduras_por_processo]

    # mapeia PID para índice na lista
    pid_to_index = {process.pid: idx for idx, process in enumerate(processes)}
    #0: 0, 1: 1 ....

    # contador de uso por processo (usado por MRU e NFU)
    counter = {process.pid: {} for process in processes}
    #armazena as paginas ja utilizadas por um processo e quantas vezes foi utilizada

    quantum = environment.quantum  # quantidade mínima do processo na CPU
    process_quantum = 0  # começa com 0

    # fila de processos a serem criados
    not_created_process = deque(sorted(processes, key=lambda p: p.creation_time))  # ordenados pelo tempo de criação
    process_rbtree = []  # árvore para armazenar os processos por v_runtime
    current_process = None
    tick = 0 

    while process_rbtree or not_created_process or current_process is not None:
        # cria os processos novos
        while not_created_process and not_created_process[0].creation_time <= tick:
            # compara o tempo do processo com o tick
            process = not_created_process.popleft()  # tira o processo da fila
            if process_rbtree:
                process.v_runtime = process_rbtree[0][0]  # recebe o menor v_runtime da árvore
            else:
                process.v_runtime = 0  # recebe zero se árvore vazia
            heapq.heappush(process_rbtree, (process.v_runtime, process.pid, process))
            # coloca os processos prontos na árvore

        # finaliza processo
        if current_process and current_process.exec_time == 0:
            current_process.finalInfo(tick)
            current_process = None
            process_quantum = 0

        # troca de processo
        if process_rbtree and (current_process is None or (
            process_rbtree[0][0] < current_process.v_runtime and process_quantum >= quantum)):
            if current_process:
                heapq.heappush(process_rbtree, (current_process.v_runtime, current_process.pid, current_process))
            _, _, current_process = heapq.heappop(process_rbtree)  # novo processo é o menor da árvore
            process_quantum = 0  # quantum é zerado porque um novo processo entrou

        if current_process:
            print(f"Tick: {tick} | PID: {current_process.pid} | Tempo restante: {current_process.exec_time} | v_runtime: {current_process.v_runtime}")
            pid = current_process.pid
            idx = pid_to_index[pid]  # índice no array de pages

            if current_process.sequence:  # se tiver algo na sequência ainda
                current_page = current_process.sequence.pop(0)  # pega a página atual e tira da sequência

                if environment.mem_policy == 'global':
                    if current_page not in molduras_global: #se pagina atual nao estiver nas molduras globais
                        if None in molduras_global: #se tiver alguma moldura livre
                            i = molduras_global.index(None) #pega o indice em que a moldura esta livre
                            molduras_global[i] = current_page #adiciona a page atual no indice encontrado
                            owner_map[i] = pid #atualiza para mostrar o process dono daquela moldura
                        else: # se sem espaço chama algoritmo para trocar a pagina
                            molduras_global, owner_map = substitution_algorithm.substitute_page_global(pages=molduras_global,new_page=current_page,counter=counter,sequence=current_process.sequence,owner_map=owner_map)
                            current_process.times_page_changed += 1
                else: #logica local
                    if current_page not in molduras_local[idx]:
                        if None in molduras_local[idx]: #se tiver espaço aloca page na moldura
                            molduras_local[idx][molduras_local[idx].index(None)] = current_page
                        else:
                            molduras_local[idx] = substitution_algorithm.substitute_page_local(pages=molduras_local[idx],new_page=current_page,counter=counter[pid],sequence=current_process.sequence)
                            current_process.times_page_changed += 1 #se nao tiver espaço chama algoritmo
                            
                # atualiza contador (usado por MRU/NUF)
                counter[pid] = substitution_algorithm.increment_counter(counter[pid], current_page)

            # atualiza execução
            current_process.exec_time -= 1
            if current_process.priority == 0:
                current_process.priority = 1  # segurança apenas
            current_process.v_runtime += 100 // current_process.priority  # calcula o novo runtime do processo
            process_quantum += 1
        else:
            print(f"Tick: {tick} | CPU Ociosa")

        tick += 1
    return processes
