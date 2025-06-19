#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <vector>
#include <queue>
#include <algorithm>
#include <set>

using namespace std;

typedef struct process {
    int creation_moment;
    int pid;
    int exec_time;
    int priority;
    int completion_time;
    int ready_state_time;
    int v_runtime;
    int original_exec_time;
} Process;

void round_robin_scheduler(vector<Process> *process_handler, int quantum) {
    queue<Process*> create_queue;
    for (Process &p : *process_handler) {
        create_queue.push(&p); // Cria uma fila auxiliar contendo todos os processos a serem criados em ordem de criação
    }

    int times = 0; // Usado em comparação com quantum, para saber se o processo atual ja utilizou o máximo de ticks da CPU
    int tick = 0; // Numero de tick (iterações)
    queue<Process*> process_queue; // Fila contendo os processos a serem executados
    while (!create_queue.empty() || !process_queue.empty()) { // Enquanto exisir processo em qualquer fila
        while (!create_queue.empty() && create_queue.front()->creation_moment == tick) { // Enquanto há um processo a ser iniciado
            process_queue.push(create_queue.front()); // Copia o processo da fila auxiliar para a fila de execucao
            create_queue.pop(); // Retira o processo da fila auxiliar
        }

        if (!process_queue.empty()) {
            cout << "PID : " << process_queue.front()->pid << " | Tempo restante : " << process_queue.front()->exec_time << endl;

            process_queue.front()->exec_time--;
            times++;
            tick++;

            if (process_queue.front()->exec_time == 0) { // Se tiver finalizado o processo
                times = 0;
                process_queue.front()->completion_time = tick - process_queue.front()->creation_moment; // Tempo de execução = tick atual - momento de criação
                process_queue.front()->ready_state_time += process_queue.front()->completion_time;
                process_queue.pop(); // Tira processo da frente
            }
            else if (times == quantum) { // Se tiver chegado ao limite de uso de ticks
                times = 0;
                process_queue.push(process_queue.front()); // Copia processo da frente para final
                process_queue.pop(); // Tira processo da frente
            }
        }
        else {tick++;} // Caso não haja nenhum processo na fila para executar
    }
}

void priority_scheduler(vector<Process> *process_handler, int quantum) {
    queue<Process*> fila_criacao; //fila_criacao é uma fila com todos os processos estão "esperando nascer".
    // ^ fila de ponteiros 

    for (Process &p : *process_handler) { //Ele passa por todos os processos que vieram do arquivo e coloca eles na fila de criação 
        fila_criacao.push(&p); 
    }

    vector<Process*> fila_prontos;  //Essa lista vai guardar os endereços dos processos que estão prontos
    Process* processo_atual = nullptr; // cria um ponteiro

    int tick = 0; // unidade de tempo

    // Enquanto ainda tiver processo pra criar, rodar ou terminar, continua o loop
    while (!fila_criacao.empty() || !fila_prontos.empty() || processo_atual != nullptr) {

        // Verifica se algum processo deve "nascer" neste tick
        while (!fila_criacao.empty() && fila_criacao.front()->creation_moment == tick) {
            // Coloca esse processo na fila de prontos para rodar
            fila_prontos.push_back(fila_criacao.front());
            fila_criacao.pop(); // Remove da fila de criação
        }

        // Se já tem um processo rodando, verifica se chegou algum mais prioritário
        if (processo_atual != nullptr) {
            for (Process* p : fila_prontos) {
                if (p->priority > processo_atual->priority) {
                    // Se achou um processo com prioridade maior, interrompe o atual
                    fila_prontos.push_back(processo_atual); // Volta pra fila de prontos
                    processo_atual = nullptr; // Libera CPU para o mais prioritário
                    break; // Só precisa interromper uma vez
                }
            }
        }

        // Se CPU estiver livre e houver processos prontos, escolhe o de maior prioridade
        if (processo_atual == nullptr && !fila_prontos.empty()) {
            // Ordena a fila dos prontos, do maior para o menor valor de prioridade
            sort(fila_prontos.begin(), fila_prontos.end(), [](Process* a, Process* b) {
                return a->priority > b->priority;
            });

            // Pega o primeiro (mais prioritário)
            processo_atual = fila_prontos.front();
            fila_prontos.erase(fila_prontos.begin()); // Remove da fila de prontos
        }

        // Se tem processo rodando, executa 1 unidade de tempo (1 tick)
        if (processo_atual != nullptr) {
            cout << "Tick: " << tick
                 << " | PID: " << processo_atual->pid
                 << " | Prioridade: " << processo_atual->priority
                 << " | Tempo restante: " << processo_atual->exec_time << endl;

            processo_atual->exec_time--; // Diminui o tempo restante

            // Se terminou a execução, registra o tempo e libera CPU
            if (processo_atual->exec_time == 0) {
                processo_atual->completion_time = tick + 1 - processo_atual->creation_moment;
                processo_atual->ready_state_time += processo_atual->completion_time;
                processo_atual = nullptr;
            }
        }

        tick++; // Avança o relógio do sistema (1 unidade de tempo)
    }
}

void lottery_scheduler(vector<Process> *process_handler, int quantum) {
    queue<Process*> create_queue;
    for (Process &p : *process_handler) {
        create_queue.push(&p);
    }

    vector<Process*> ready_list;
    int tick = 0;
    int current_quantum = 0;
    Process* current_process = nullptr;

    while (!create_queue.empty() || !ready_list.empty() || current_process) {
        while (!create_queue.empty() && create_queue.front()->creation_moment == tick) {
            ready_list.push_back(create_queue.front());
            create_queue.pop();
        }

        for (Process* p : ready_list)
            if (p != current_process) p->ready_state_time++;

        if (!current_process && !ready_list.empty()) {
            vector<Process*> tickets;
            for (Process* p : ready_list)
                tickets.insert(tickets.end(), p->priority, p);
            current_process = tickets[rand() % tickets.size()];
            current_quantum = 0;
        }

        if (current_process) {
            cout << "PID : " << current_process->pid << " | Tempo restante : " << current_process->exec_time << endl;
            current_process->exec_time--;
            current_quantum++;

            if (current_process->exec_time == 0) {
                current_process->completion_time = tick + 1 - current_process->creation_moment;
                ready_list.erase(remove(ready_list.begin(), ready_list.end(), current_process), ready_list.end());
                current_process = nullptr;
            } else if (current_quantum == quantum) {
                current_process = nullptr;
            }
        }

        tick++;
    }
}

void cfs_scheduler(vector<Process> *process_handler){
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
            current_process->ready_state_time = (current_process->completion_time - current_process->creation_moment) - current_process->original_exec_time;
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
}

int main() {
    string entry;
    cout << "Insira o caminho para o arquivo: ";
    getline(cin, entry);
    ifstream archive(entry);

    string line, token, algorithm, temp_quantum;
    int quantum;
    getline(archive, line);
    istringstream iss(line);
    
    getline(iss, algorithm, '|');
    getline(iss, temp_quantum);
    quantum = stoi(temp_quantum);
    temp_quantum.clear();

    vector<Process> process_handler; //Cria vetor para armazenar os processos (momentoDeCriacao, PID, tempoDeExecucao, prioridade)

    if (archive.is_open()) {
        while (!archive.eof()) { //Enquanto houver linhas para serem lidas
            getline(archive, line);

            if (line.compare("") == 0) { //Se não houver nada na ultima linha, significa que chegou ao final
                break;
            }

            Process p;
            istringstream iss(line); //Cria variavel iss para tokenizar a linha

            getline(iss, token, '|');
            p.creation_moment = stoi(token);
            getline(iss, token, '|');
            p.pid = stoi(token);
            getline(iss, token, '|');
            p.exec_time = stoi(token);
            getline(iss, token, '|');
            p.priority = stoi(token);
            
            p.completion_time = 0;
            p.ready_state_time = -p.exec_time;
            p.v_runtime = 0.0; 
            p.original_exec_time = p.exec_time;
            
            process_handler.push_back(p);
        }
    }
    sort(process_handler.begin(), process_handler.end(), [](const Process &a, const Process &b) {
        return a.creation_moment < b.creation_moment;
    }); // Ordena o vetor utilizando o momento de criação como base

    archive.close();

    if (algorithm.compare("alternanciaCircular") == 0) {
        round_robin_scheduler(&process_handler, quantum);
    } else if (algorithm.compare("prioridade") == 0) {
        priority_scheduler(&process_handler, quantum);
    } else if (algorithm.compare("loteria") == 0) {
        lottery_scheduler(&process_handler, quantum);
    } else if (algorithm.compare("CFS") == 0) {
        cfs_scheduler(&process_handler);
    } else {
        cout << "Erro. Algoritmo nao listado!" << endl;
        exit(1);
    }

    cout << "----------------------------" << endl;
    for (Process p : process_handler) {
        cout << "PID : " << p.pid << " | Completion Time : " << p.completion_time << " | Ready State : " << p.ready_state_time << endl;
    }

    return 0;
}