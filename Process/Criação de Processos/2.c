/*
Faça um programa que crie um processo filho. Este processo filho executará uma tarefa dependendo do seu ID de processo e do ID do seu pai. 
Se ambos IDs foram pares, o processo filho deverá multiplicar dois vetores de dimensão N (informada pelo usuário) e com valores aleatoriamente gerados. 
Se ambos IDs forem ímpares, o processo filho deverá subtrair os vetores. Se o pai for ímpar e o filho par, deverá realizar a adição dos vetores. 
Se o pai for par e o filho ímpar, deverá realizar as três operações. Se o ID do filho for par, o processo pai deve esperar pelo seu encerramento. 
Se o ID for ímpar, não precisa esperar pelo filho.
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/wait.h>
#include <unistd.h>

int _printVetor(int *vetor, int size) {
    for (int i = 0; i < size; i++) {
        if (i < size - 1) {
            printf("%d - ", vetor[i]);
        }
        else {
            printf("%d", vetor[i]);
        }
    }
    return 0;
}

int _random(int min, int max) {
    return (min + rand() / (RAND_MAX / max - min + 1) + 1);
}

int _fillArray(int *vetor, int size) {
    for (int i = 0; i < size; i++) {
        vetor[i] = _random(-1, 9);
    }
    return 0;
}

int _multiplicarVetores(int *vetor1, int *vetor2, int *vetorR, int size) {
    for (int i = 0; i < size; i++) {
        vetorR[i] = vetor1[i] * vetor2[i];
    }
    return 0;
}

int _subtrairVetores(int *vetor1, int *vetor2, int *vetorR, int size) {
    for (int i = 0; i < size; i++) {
        vetorR[i] = vetor1[i] - vetor2[i];
    }
    return 0;
}

int _somarVetores(int *vetor1, int *vetor2, int *vetorR, int size) {
    for (int i = 0; i < size; i++) {
        vetorR[i] = vetor1[i] + vetor2[i];
    }
    return 0;
}

int main(void) {
    srand(time(NULL));
    int size, status;
    printf("Insira o tamanho N do vetor: ");
    scanf("%d", &size);

    int *vetor1 = malloc(size * sizeof(int));
    int *vetor2 = malloc(size * sizeof(int));
    int *vetorR = malloc(size * sizeof(int));

    _fillArray(vetor1, size);
    _fillArray(vetor2, size);

    pid_t newPid, me, parent, x;

    newPid = fork();
    me = getpid();
    parent = getppid();

    if (newPid != 0) {
        if (newPid % 2 == 0) {
            printf("Esperando...");
            x = waitpid(newPid, &status, 0);
        }
        else {
            printf("Terminou");
        }
        return 0;
    }
    else {
        printf("ID Filho: %d, ID Pai: %d", me, parent);
        sleep(2);

        if ((me % 2 == 0) && (parent % 2 == 0)) { // Ambos pares
            _multiplicarVetores(vetor1, vetor2, vetorR, size);
            printf("\nVetor 1: ");
            _printVetor(vetor1, size);
            printf("\nVetor 2: ");
            _printVetor(vetor2, size);
            printf("\nVetor R: ");
            _printVetor(vetorR, size);
        }
        else if ((me % 2 != 0) && (parent % 2 != 0)) { // Ambos impares
            _subtrairVetores(vetor1, vetor2, vetorR, size);
            printf("\nVetor 1: ");
            _printVetor(vetor1, size);
            printf("\nVetor 2: ");
            _printVetor(vetor2, size);
            printf("\nVetor R: ");
            _printVetor(vetorR, size);
        }
        else if ((me % 2 == 0) && (parent % 2 != 0)) { // Filho par Pai impar
            _somarVetores(vetor1, vetor2, vetorR, size);
            printf("\nVetor 1: ");
            _printVetor(vetor1, size);
            printf("\nVetor 2: ");
            _printVetor(vetor2, size);
            printf("\nVetor R: ");
            _printVetor(vetorR, size);
        }
        else if ((me % 2 != 0) && (parent % 2 == 0)) { // Filho impar Pai par
            _multiplicarVetores(vetor1, vetor2, vetorR, size);
            printf("\nVetor 1: ");
            _printVetor(vetor1, size);
            printf("\nVetor 2: ");
            _printVetor(vetor2, size);
            printf("\nVetor R: ");
            _printVetor(vetorR, size);
            _subtrairVetores(vetor1, vetor2, vetorR, size);
            printf("\nVetor 1: ");
            _printVetor(vetor1, size);
            printf("\nVetor 2: ");
            _printVetor(vetor2, size);
            printf("\nVetor R: ");
            _printVetor(vetorR, size);
            _somarVetores(vetor1, vetor2, vetorR, size);
            printf("\nVetor 1: ");
            _printVetor(vetor1, size);
            printf("\nVetor 2: ");
            _printVetor(vetor2, size);
            printf("\nVetor R: ");
            _printVetor(vetorR, size);
        }
    }
}