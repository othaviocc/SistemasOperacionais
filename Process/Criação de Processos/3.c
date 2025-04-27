/*
Faça um programa que crie N processos, onde N é um número fornecido pelo usuário. 
Cada processo criado deverá gerar uma sequência de números seguindo a conjectura de Collatz (definida abaixo). 
O número x utilizado por cada processo será indicado pelos dígitos da centena e da dezena do seu ID (ex: ID 12345, a entrada será 34). 
A conjectura de Collatz diz que, dado um número inteiro X positivo, se a seguinte regra for aplicada, a sequência eventualmente chegará até o valor 1. 
Garanta que o processo pai somente vai encerrar após o término dos cálculos por TODOS os processos filho.
Definição: x = x/2, se x for par ou 3*x+1 se x for ímpar.
Exemplo considerando x = 35: 35, 106, 53, 160, 80, 40, 20, 10, 5, 16, 8, 4, 2, 1
*/

#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

int _centenaEDezena(int num) {
    return (((num % 1000) - (num % 10)) / 10);
}

int _collatz(int pid) {
    int x = _centenaEDezena(pid);
    int *vetor = malloc(sizeof(int));
    for (int i = 0;; i++) {
        vetor = realloc(vetor, (i + 1) * sizeof(int));
        vetor[i] = x;
        if ((x == 1) || (x == 0)) {
            printf("Processo %d - Vetor: ", pid);
            for (int z = 0; z <= i; z++) {
                if (z <= i - 1) {
                    printf("%d - ", vetor[z]);
                }
                else {
                    printf("%d\n", vetor[z]);
                    free(vetor);
                    return 0;
                }
            }
        }
        if (x % 2 == 0) {
            x = x / 2;
        }
        else {
            x = 3 * x + 1;
        }
    }
}

int main(void) {
    pid_t newPid, me, parent, x, parentProcess;
    int status, nProcess;
    parentProcess = getpid();

    printf("Insira o número de processos: ");
    scanf("%d", &nProcess);

    int *vetorProcessos = malloc(nProcess * sizeof(int));

    for (int i = 0; i < nProcess; i++) {
        vetorProcessos[i] = fork();
        if (vetorProcessos[i] == 0) {
            break;
        }
    }

    me = getpid();
    parent = getppid();

    if (me == parentProcess) {
        x = waitpid(-1, &status, 0);
        printf("Finalizado!\n");
    }
    else {
        _collatz(me);
    }

    return 0;
}