from substitutionAlgorithms import *

def run(processes, environment, substitution_algorithm):
    substitution_algorithm = {'fifo':Fifo, 'mru':MRU, 'nuf':NUF, 'otimo':Otimo}[substitution_algorithm] # Seleciona o tipo de algorito de substituição
    max_pages = [int(process.mem_qty * (environment.aloc_percentual/100) // environment.page_size) for process in processes] # Vetor com número máximo de páginas (em ordem de tempo de criação dos processos)
    counter = {} # Counter utilizado em MRU e NFU
    pages = [[None] * i for i in max_pages] # Vetor que armazena as páginas utilizadas atualmente

    index = 0 # Índice do processo a ser criado
    processes_index = [] # Armazena os índices dos processos em execução
    tick = 0 # Armazena o tick atual
    process_quantum = 0 # Armazena quantas vezes o processo atual já utilizou a CPU
    while index < len(processes) or len(processes_index) > 0: # Enquanto ainda há processos a serem criados ou executados
        for process in processes[index:]: # Avalia os processos a serem criados
            if process.creation_time == tick: # Caso esteja no tick atual de criação
                processes_index.append(index) # Adiciona no vetor de índices o índice do processo atual
                counter[index] = {}
                index += 1 # Incrementa o índice em 1
            else:
                break # Caso o tick de criação seja maior que o atual ou menor que 0 o laço é quebrado

        if len(processes_index) > 0: # Se há um processo sendo executado
            if processes[processes_index[0]].sequence[0] not in pages[processes_index[0]]: # Se a página atual não está na moldura
                if None in pages[processes_index[0]]: # Se ainda há espaço livre para páginas
                    pages[processes_index[0]].remove(None) # Remove um None do vetor
                    pages[processes_index[0]].append(processes[processes_index[0]].sequence[0]) # Adiciona a pagina atual
                else:
                    pages[processes_index[0]] = substitution_algorithm.substitute_page_local(pages=pages[processes_index[0]], new_page=processes[processes_index[0]].sequence[0], counter=counter[processes_index[0]], sequence=processes[processes_index[0]].sequence) # Chama a função de substituição de página
                    processes[processes_index[0]].times_page_changed += 1
            counter[processes_index[0]] = substitution_algorithm.increment_counter(counter[processes_index[0]], processes[processes_index[0]].sequence[0]) # Incrementa o contador

            processes[processes_index[0]].exec_time -= 1 # Decrementa o tempo de execução
            process_quantum += 1 # Incrementa o quantum do processo atual
            tick += 1 # Incrementa o tick
            processes[processes_index[0]].sequence.pop(0)

            if processes[processes_index[0]].exec_time == 0: # Se o processo atual finalizou
                process_quantum = 0 # Zera o quantum do processo
                processes[processes_index[0]].finalInfo(tick) # Atualiza o completion tick e ready state time
                processes_index.pop(0) # Retira o índice do processo da fila
            elif process_quantum == environment.quantum: # Se o processo atual usou o máximo permitido da CPU
                process_quantum = 0 # Zera o quantum do processo
                processes_index.append(processes_index[0]) # Manda ao final da fila o processo atual
                processes_index.pop(0) # -----------------------------------------------------------

        else: # Caso não exista processos sendo executados mas existam processos a serem criados
            tick += 1 # Incrementa o tick

    return processes