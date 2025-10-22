from Classes import *
from copy import deepcopy
import alternanciaCircular
import prioridade
import loteria
import cfs
import dispositivos

if __name__ == '__main__':
    with open('entrada.txt', 'r') as entry: # Abre o arquivo de entrada
        algorithm, quantum, mem_policy, mem_size, page_size, aloc_percentual, n_dev = entry.readline().strip('\n').split('|') # Salva as variáveis da primeira linha
        algorithm = {"alternanciaCircular":alternanciaCircular, "prioridade":prioridade, "loteria":loteria, "cfs":cfs}[algorithm] # Substitui a string pela classe
        environment = Environment(algorithm, int(quantum), mem_policy, int(mem_size), int(page_size), int(aloc_percentual)) # Armazena as informações da página/moldura, memória etc

        devices = []
        for _ in range(int(n_dev)):
            id_dev, s_u_l, op_t = entry.readline().strip('\n').split('|')
            device = dispositivos.Dispositivo(id_dev, int(s_u_l), int(op_t))
            devices.append(device)

        processes = [] # Vetor para armazenar os processos
        for line in entry.readlines():
            creation_time, pid, exec_time, priority, mem_qty, sequence, io_chance = line.strip('\n').split('|') # Salva as variáveis do processo
            sequence = list(map(int, sequence.strip().split())) # Transforma a sequencia em um vetor
            processes.append(Process(int(creation_time), int(pid), int(exec_time), int(priority), int(mem_qty), sequence, int(io_chance))) # Adiciona os processos no vetor

    processes.sort(key=lambda x: x.creation_time) # Ordena o vetor com base no momento de criação

    esc_fifo = algorithm.run(deepcopy(processes), environment, 'fifo', devices) # Chama o algoritmo escalonador com o algoritmo de substituição de página
    esc_mru = algorithm.run(deepcopy(processes), environment, 'mru', devices)
    esc_nuf = algorithm.run(deepcopy(processes), environment, 'nuf', devices)
    esc_otimo = algorithm.run(deepcopy(processes), environment, 'otimo', devices)

    times_page_changed_fifo = sum([process.times_page_changed for process in esc_fifo])
    times_page_changed_mru = sum([process.times_page_changed for process in esc_mru])
    times_page_changed_nuf = sum([process.times_page_changed for process in esc_nuf])
    times_page_changed_otimo = sum([process.times_page_changed for process in esc_otimo])

    print(f'O algoritmo FIFO precisou trocar {times_page_changed_fifo} vezes as páginas\nO algoritmo MRU precisou trocar {times_page_changed_mru} vezes as páginas\nO algoritmo NUF precisou trocar {times_page_changed_nuf} vezes as páginas\nO algoritmo OTIMO precisou trocar {times_page_changed_otimo} vezes as páginas \n')

    for process in esc_fifo:
        print(f'{process.repr()}')
