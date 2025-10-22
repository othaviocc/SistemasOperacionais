from substitutionAlgorithms import *
import random

def run(processes, environment, substitution_algorithm):
    #preparação dos processos e memoria
    substitution_algorithm = {'fifo':Fifo, 'mru':MRU, 'nuf':NUF, 'otimo':Otimo}[substitution_algorithm]
    max_pages = [int(process.mem_qty * (environment.aloc_percentual/100) // environment.page_size) for process in processes] #maximo de paginas alocadas por processo
    counter = {} #cria para cada processo
    pages = [[None] * i for i in max_pages] #estrutura de paginas de cada processo
    #variaveis de controle
    tick = 0 
    creation_index = 0
    ready_processes_indices = []
    # executado se ainda tiver processo a ser criado ou pronto
    while creation_index < len(processes) or len(ready_processes_indices) > 0:
        #libera os processos que o tempo de criação ja foi
        while creation_index < len(processes) and processes[creation_index].creation_time <= tick:
            ready_processes_indices.append(creation_index)
            counter[creation_index] = {}
            creation_index += 1
        #se nao tem processo pronto, avança o tempo ate o processo ficar pronto
        if not ready_processes_indices:
            if creation_index < len(processes):
                tick = processes[creation_index].creation_time
            else:
                break
            continue
        #LOTERIA:
        current_process_index = None
        total_tickets = sum(processes[i].priority for i in ready_processes_indices)
        
        if total_tickets > 0:
            winning_ticket = random.randint(1, total_tickets)
            ticket_sum = 0
            for i in ready_processes_indices:
                ticket_sum += processes[i].priority
                if winning_ticket <= ticket_sum:
                    current_process_index = i
                    break
        else:
            current_process_index = ready_processes_indices[0]

        #seleciona o processo escolhido e começa a executar a sua sequancia de paginas
        if current_process_index is not None:
            current_process = processes[current_process_index]
            #executa o processo ate quantum ou ate esvaziar a sequencia de paginas
            for _ in range(environment.quantum):
                print(f"Tick: {tick} | PID: {current_process.pid} | Tempo restante: {current_process.exec_time}")
                if not current_process.sequence:
                    break
                #se a pagina n esta presente so add, se nao aplica o algoritmo de substituiçao
                #conta a troca de pagina se houver subst. real
                page_to_access = current_process.sequence[0]
                if page_to_access not in pages[current_process_index]:
                    if None in pages[current_process_index]:
                        pages[current_process_index].remove(None)
                        pages[current_process_index].append(page_to_access)
                    else:
                        pages[current_process_index] = substitution_algorithm.substitute_page_local(
                            pages=pages[current_process_index], 
                            new_page=page_to_access, 
                            counter=counter[current_process_index], 
                            sequence=current_process.sequence
                        )
                        current_process.times_page_changed += 1
                #atualiza o contador e avança
                counter[current_process_index] = substitution_algorithm.increment_counter(
                    counter[current_process_index], page_to_access
                )
                
                current_process.sequence.pop(0)
                current_process.exec_time -= 1
                tick += 1
            #finaliza o processo se terminou
            if not current_process.sequence:
                current_process.finalInfo(tick)
                ready_processes_indices.remove(current_process_index)

    return processes