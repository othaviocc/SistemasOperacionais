/*
Faça um programa que crie um processo filho. Este processo filho deverá realizar a multiplicação de dois vetores de dimensão N (informada pelo usuário) 
e com valores aleatoriamente gerados. Garanta que o processo pai somente vai encerrar após o término dos cálculos pelo processo filho. 
Dica: utilize a função sleep() no processo filho para retardar a execução de cálculos e também mensagens de print no processo pai para 
indicar o que está acontecendo.
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/wait.h>
#include <unistd.h>

int returnRandom(int min, int max) {
    return (min + rand() / (RAND_MAX / max - min + 1) + 1);
}

int main()
{
    srand(time(NULL));

    pid_t newPid, me, parent, x;
    int status, vetorTam;

    printf("Insira o tamanho do vetor: ");
    scanf("%d", &vetorTam);

    int vetor1[vetorTam], vetor2[vetorTam];

    for (int i = 0; i < vetorTam; i++) {
        vetor1[i] = returnRandom(-1, 9);
        vetor2[i] = returnRandom(-1, 9);
    }

    fflush(stdout); // Sem isso o fork roda o for anterior

    newPid = fork();
    me = getpid();
    parent = getppid();

    if (newPid != 0) {
        x = waitpid(newPid, &status, 0);

        printf("\nVetor 1: ");

        for (int i = 0; i < vetorTam; i++) {
            if (i < vetorTam - 1) {
                printf("%d - ", vetor1[i]);
            }
            else {
                printf("%d", vetor1[i]);
            }
        }

        printf("\nVetor 2: ");

        for (int i = 0; i < vetorTam; i++) {
            if (i < vetorTam - 1) {
                printf("%d - ", vetor2[i]);
            }
            else {
                printf("%d", vetor2[i]);
            }
        }
        
        printf("\n");
    }
    else {
        int vetor3[vetorTam];

        for (int i = 0; i < vetorTam; i++) {
            vetor3[i] = vetor1[i] * vetor2[i];
        }

        printf("Vetor resultante: ");

        for (int i = 0; i < vetorTam; i++) {
            if (i < vetorTam - 1) {
                printf("%d - ", vetor3[i]);
            }
            else {
                printf("%d", vetor3[i]);
            }
        }
    }

    return 0;
}