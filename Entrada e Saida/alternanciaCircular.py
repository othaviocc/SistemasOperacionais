from substitutionAlgorithms import *
import random

def run_io(chance): # Verificar se irá rodar dispositivo
    number = random.randint(1, 100)
    if number <= chance:
        return True
    return False

def run(processes, environment, substitution_algorithm, devices):
    substitution_algorithm = {'fifo':Fifo, 'mru':MRU, 'nuf':NUF, 'otimo':Otimo}[substitution_algorithm] # Seleciona o tipo de algorito de substituição
    max_pages = [int(process.mem_qty * (environment.aloc_percentual/100) // environment.page_size) for process in processes] # Vetor com número máximo de páginas (em ordem de tempo de criação dos processos)
    pages = [[None] * i for i in max_pages] # Vetor que armazena as páginas utilizadas atualmente
    counter = {} # Counter utilizado em MRU e NFU

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
        
        while processes[processes_index[0]].io_device == 'waiting': # Se topo da fila esta esperando um dispositivo e/s
            processes_index.append(processes_index[0]) # Manda ao final da fila o processo atual, pois a CPU nao pode executar no momento
            processes_index.pop(0) # -----------------------------------------------------------

        if len(processes_index) > 0: # Se há um processo sendo executado

            if processes[processes_index[0]].io_device == None and process_quantum == 0: # Executa no primeiro tick do quantum

                #AQUI
                if run_io(processes[processes_index[0]].io_chance): # Verifica se irá substituir processo por IO
                    device = random.choice(devices) # Seleciona dispositivo aleatório
                    if device.simultaneous_use > device.simultaneous_use_limit: # Caso o dispositivo já esteja no seu limite de processos
                        device.add_process_queue(processes_index[0]) # Adiciona processo na fila do dispositivo
                        processes[processes_index[0]].state = 'waiting' # Caso entre na fila, processo salvará device como waiting
                    else:
                        processes[processes_index[0]].state = 'blocked' # Muda estado do processo para bloqueado


                    processes[processes_index[0]].io_device = device # Salva dispositivo no processo
                    device.increment_simultaneous_use() # Incrementa número de processos usando dispositivo
                    processes[processes_index[0]].io_remain = device.op_time # io_remain vai receber o tempo total de execução do dispositivo
                    processes[processes_index[0]].blocked_state_time -= tick # Subtrai valor de blocked_state_time

            if processes[processes_index[0]].io_device != None: # Se há dispositivos no processo, executará o dispositivo
                processes[processes_index[0]].io_remain -= 1 # Decrementa Op. Time
                process_quantum += 1

                
                if processes[processes_index[0]].io_remain == 0: # Se finalizou  
                    
                    #AQUI IMPORTANTE
                    if len(processes[processes_index[0]].io_device.queue) > 0: 
                        processes[processes[processes_index[0]].io_device.queue[0]].state = 'blocked'
                        processes[processes_index[0]].io_device.queue.pop(0)
                    processes[processes_index[0]].io_device.decrement_simultaneous_use()
                    processes[processes_index[0]].io_device = None
                    processes[processes_index[0]].state = 'ready'
                    processes[processes_index[0]].blocked_state_time += tick + 1# Adiciona valor de blocked_state_time

            else: # Se não há dispositivos no processo, executará o processo em si
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
                processes[processes_index[0]].sequence.pop(0)

            if process_quantum == environment.quantum and processes[processes_index[0]].exec_time > 0:
                print(f'\nProcessos:')
                for process in processes_index[:index + 1]:
                    print(f'PID : {processes[process].pid} | Remaining Time : {processes[process].exec_time} | Device : {processes[process].io_device.id if processes[process].io_device else None} | State : {'executing' if process == processes_index[0] else processes[process].state}')
                print(f'Dispositivos')
                for device in devices:
                    print(f'Name : {device.id} | State : {"In Use" if device.simultaneous_use > 0 else "Ocious"}')
                processes_index.append(processes_index[0]) # Manda ao final da fila o processo atual
                process_quantum = 0 # Zera o quantum do processo
                processes_index.pop(0) # -----------------------------------------------------------

            if processes[processes_index[0]].exec_time == 0:
                print(f'\nProcessos:')
                for process in processes_index[:index + 1]:
                    print(f'PID : {processes[process].pid} | Remaining Time : {processes[process].exec_time} | Device : {processes[process].io_device.id if processes[process].io_device else None} | State : {'executing' if process == processes_index[0] else processes[process].state}')
                print(f'Dispositivos')
                for device in devices:
                    print(f'Name : {device.id} | State : {"In Use" if device.simultaneous_use > 0 else "Ocious"}')
                processes[processes_index[0]].finalInfo(tick) # Atualiza o completion tick e ready state time
                process_quantum = 0 # Zera o quantum do processo
                processes_index.pop(0) # -----------------------------------------------------------

        tick += 1 # Incrementa o tick
    
    return processes