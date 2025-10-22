"""void cfs_scheduler(vector<Process> *process_handler){
    //comparador para usar no set, ele vai organizar o set com o primeiro valor sendo o v_runtime mínimo 
    auto cmp = [](Process* a, Process* b) { //comparador para usar no set
        if (a->v_runtime == b->v_runtime){
            return a->pid < b->pid; // desempate por pid
        } 
        return a->v_runtime < b->v_runtime;
    };

    set<Process*, decltype(cmp)> process_rbtree(cmp); //set para ordenar os processos por menor v_runtime

    queue<Process*> not_create_process; // fila para armazenar os processos ainda não iniciados

    for (Process &p:*process_handler){
        not_create_process.push(&p); // preencher a fila de processos ainda não iniciados
    }

    Process* current_process = nullptr; // Ponteiro para o processo atualmente em execução
    int tick = 0; // Nro de ticks 

    while(!process_rbtree.empty() || !not_create_process.empty() || current_process != nullptr){ //while principal
        //while a seguir é para ver quais processos iniciam naquele tick e os adicionar na rbtree
        while (!not_create_process.empty() && not_create_process.front()->creation_moment <= tick) { 
            //a condição acima basicamente diz: se a fila de processos nao criados, não estiver vazia 
            //e o momento de criação do proximo processo dessa fila for menor ou igual ao tick atual entra

            if(process_rbtree.empty()){
                not_create_process.front()->v_runtime = 0; //para o primeiro processo adicionado a rbtree
            }else{
                not_create_process.front()->v_runtime = (*process_rbtree.begin())->v_runtime; 
                //o novo processo é adicionado com o valor minimo atual da rbtree para não cortar a frente do processo antigo
            }
            process_rbtree.insert(not_create_process.front()); //adiciona o processo na rbtree
            not_create_process.pop(); //retira o primeiro elemento da fila
        }

        //esse if calcula o tempo em pronto 
        if (current_process != nullptr && current_process->exec_time == 0) {
            current_process->completion_time = tick; // O tick atual é o momento de conclusão
            current_process->ready_state_time = (current_process->completion_time - current_process->creation_moment) + current_process->ready_state_time;
            // tempo em pronto = (tempo que completou - o momento de criação) - o tempo de execução do processo
            current_process = nullptr; // libera o ponteiro
        }

        //logica para escolher o proximo processo a ser executado
        if (!process_rbtree.empty() && (current_process == nullptr || ((*process_rbtree.begin())->v_runtime < current_process->v_runtime))){
            // se a CPU estiver sem processo atual, ou se o v_runtime de algum processo for menor que o do processo atual
            
            if (current_process != nullptr) {
                process_rbtree.insert(current_process);//se o processo atual ainda não concluiu ele reinsere ele na rbtree, mas com seu valor atualizado
            }
            if (process_rbtree.empty()) {
                current_process = nullptr; //deixa vazio para mostrar q acabou os processos
            } else {
                current_process = *process_rbtree.begin(); //pega o menor valor da arvore
                process_rbtree.erase(process_rbtree.begin()); //apaga da arvore o valor que foi pego
            }
        }
        if (current_process != nullptr) {
            cout << "Tick: " << tick << " | PID: " << current_process->pid << " | Tempo restante: " << current_process->exec_time << " | v_runtime: " << current_process->v_runtime << endl;
            //printa as informações
            current_process->exec_time--; // Decrementa o tempo restante de execução
            current_process->v_runtime += 100/ (current_process->priority); //incrementa o v_runtime com base na prioridade 
            //quanto maior a prioridade menor sera o v_runtime e assim antes será executado.

        } else {
            cout << "Tick: " << tick << " | CPU Ociosa" << endl; // mostra a cpu ociosa em tal momento
        }
        tick++; // caso não haja processo

    }
}"""
import heapq
from collections import deque

def run(processes, environment):
    quantum = environment.quantum #tempo minimo que um processo fica na cpu
    process_quantum = 0
    #Fila de processos ainda não criados (ordenados pelo tempo de criação)
    not_created_process = deque(sorted(processes, key=lambda p: p.creation_time))

    #Heap para simular árvore balanceada ordenada por v_runtime (tupla: (v_runtime, pid, processo))
    process_rbtree = []
    current_process = None #processo atual
    tick = 0 #tick da simulação

    # Adiciona atributo dinâmico v_runtime
    for process in processes:
        process.v_runtime = 0 

    while process_rbtree or not_created_process or current_process != None:
        # Verifica se novos processos devem ser criados neste tick
        while not_created_process and not_created_process[0].creation_time <= tick:
            process = not_created_process.popleft() #recebeu o processo com tick de criação atual
            if not process_rbtree: #se rbtree vazia, v_runtime = 0
                process.v_runtime = 0
            else:
                process.v_runtime = process_rbtree[0][0] #se tiver elemento, v_runtime = menor valor
            heapq.heappush(process_rbtree, (process.v_runtime, process.pid, process)) #puxa o processo para a tree

        #verifica se o processo atual terminou
        if current_process and current_process.exec_time == 0:
            current_process.finalInfo(tick) #printa as infos
            current_process = None 
            process_quantum = 0

        #seleciona novo processo se necessário
        if process_rbtree and (current_process is None or (process_rbtree[0][0] < current_process.v_runtime and process_quantum >= quantum)):
            #Basicamente se o processo atual tiver um runtime > q o da tree e o quantum tiver acabado, troca pro first da tree
            if current_process:
                heapq.heappush(process_rbtree, (current_process.v_runtime, current_process.pid, current_process))
            _, _, current_process = heapq.heappop(process_rbtree)
            process_quantum = 0

        # Executa processo atual
        if current_process:
            print(f"Tick: {tick} | PID: {current_process.pid} | Tempo restante: {current_process.exec_time} | v_runtime: {current_process.v_runtime}")
            current_process.exec_time -= 1
            if current_process.priority == 0:
                current_process.priority = 1
            current_process.v_runtime += 100 // current_process.priority
            process_quantum += 1
        else:
            print(f"Tick: {tick} | CPU Ociosa")

        tick += 1