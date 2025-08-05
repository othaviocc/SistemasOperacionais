def run(processes, environment):
    index = 0 # Índice do processo a ser criado
    processes_index = [] # Armazena os índices dos processos em execução
    tick = 0 # Armazena o tick atual
    process_quantum = 0 # Armazena quantas vezes o processo atual já utilizou a CPU
    while index < len(processes) or len(processes_index) > 0: # Enquanto ainda há processos a serem criados ou executados
        for process in processes[index:]: # Avalia os processos a serem criados
            if process.creation_time == tick: # Caso esteja no tick atual de criação
                processes_index.append(index) # Adiciona no vetor de índices o índice do processo atual
                index += 1 # Incrementa o índice em 1
            else:
                break # Caso o tick de criação seja maior que o atual ou menor que 0 o laço é quebrado

        if len(processes_index) > 0: # Se há um processo sendo executado
            print(f'PID : {processes[processes_index[0]].pid} | Tempo restante : {processes[processes_index[0]].exec_time}') # Print das informações

            processes[processes_index[0]].exec_time -= 1 # Decrementa o tempo de execução
            process_quantum += 1 # Incrementa o quantum do processo atual
            tick += 1 # Incrementa o tick

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