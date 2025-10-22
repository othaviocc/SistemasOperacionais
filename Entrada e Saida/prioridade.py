from substitutionAlgorithms import Fifo, MRU, NUF, Otimo

def run(processes, environment, substitution_algorithm):
    # Seleciona a classe de substituição de páginas correta
    substitution_algorithm = {
        'fifo': Fifo,
        'mru': MRU,
        'nuf': NUF,
        'otimo': Otimo
    }[substitution_algorithm]

    # Calcula o número máximo de molduras/páginas para cada processo
    max_pages = [
        max(1, int(process.mem_qty * (environment.aloc_percentual / 100) // environment.page_size))
        for process in processes
    ]

    counter = {}  # Para NFU/MRU
    pages = [[None] * n for n in max_pages]  # Molduras para cada processo

    index = 0
    processes_index = []
    tick = 0
    
    # Tempo já consumido pelo processo atual (para contar o quantum)
    current_quantum = 0

    while index < len(processes) or processes_index: ##laço principal, continua ate todos processos terminarem
        # Adiciona processos novos em tal tick
        for process in processes[index:]:
            if process.creation_time == tick:
                processes_index.append(index)
                counter[index] = {}
                index += 1
            else:
                break

        if processes_index:#Há algum processo pronto para ser executado agora?
            # Ordena a fila pela prioridade decrescente e menor tempo de criação
            processes_index.sort(key=lambda idx: (-processes[idx].priority, processes[idx].creation_time)) # se tiver dois processos com prioridade, escolhemos o mais antigo
            current_idx = processes_index[0]
            process = processes[current_idx]

            if process.sequence: #verifica se o processo ainda tem paginas a acessar
                page_request = process.sequence[0]

                if page_request not in pages[current_idx]: #Verifica se essa página já está carregada nas molduras 
                    if None in pages[current_idx]: #Verifica se ainda existe algum espaço livre nas molduras desse processo
                        pages[current_idx].remove(None)
                        pages[current_idx].append(page_request)
                    else: #quando todas molduras estiverem cheias vamos chamar o algoritmo de substituição(fifo,mru,nfu,otimo)
                        pages[current_idx] = substitution_algorithm.substitute_page_local(
                            pages=pages[current_idx],
                            new_page=page_request,
                            counter=counter[current_idx],
                            sequence=process.sequence
                        )
                        process.times_page_changed += 1

                counter[current_idx] = substitution_algorithm.increment_counter(
                    counter[current_idx], page_request
                )

                process.exec_time = max(0, process.exec_time - 1)
                tick += 1
                current_quantum += 1
                process.sequence.pop(0)

                if process.exec_time == 0: #Esse if é um teste para saber se o processo já terminou a execução.
                    process.finalInfo(tick)
                    processes_index.pop(0)
                    current_quantum = 0  # reinicia quantum para o próximo

                elif current_quantum == environment.quantum: #é usado para verificar se o processo atingiu o limite de tempo permitido no processador (quantum).
                    # Quantum expirou, reencaixa o processo e zera o quantum
                    current_quantum = 0
                    processes_index.append(processes_index.pop(0))  # manda para o fim da fila
            else:
                # Caso não tenha mais páginas para acessar
                process.exec_time = max(0, process.exec_time - 1)
                tick += 1
                current_quantum += 1
                if process.exec_time == 0:
                    process.finalInfo(tick)
                    processes_index.pop(0)
                    current_quantum = 0
                elif current_quantum == environment.quantum:
                    current_quantum = 0
                    processes_index.append(processes_index.pop(0))
        else:
            tick += 1

    return processes