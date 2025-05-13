/*
Faça um programa que receba como entrada dois vetores de inteiros A e B de tamanho N e realize o seu produto vetorial. 
A saída deverá ser armazenada em um vetor C. O tamanho do vetor e o número de threads devem ser informados pelo usuário. 
Os elementos do vetor devem ser gerados de forma aleatória pelo programa. O programa deverá imprimir na tela os vetores de entrada e o vetor de saída.
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <pthread.h>
#define random_randint(min, max) (min + rand() / (RAND_MAX / max - min + 1) + 1)

typedef struct {
    int *vetor_a;
    int *vetor_b;
    int *vetor_c;
    unsigned start;
    unsigned end;
} Vetores;

void *multiplicacao(void *i) {
    Vetores *ptr = (Vetores *)i;

    for (unsigned i = ptr->start; i < ptr->end; i++) {
        ptr->vetor_c[i] = ptr->vetor_a[i] * ptr->vetor_b[i];
    }
}

void main() {
    srand(time(NULL));

    unsigned vetor_size;
    printf("Insira o tamanho do vetor: ");
    scanf("%u", &vetor_size);

    unsigned threads_number;
    printf("Insira o numero de threads: ");
    scanf("%u", &threads_number);

    int *vetor_a, *vetor_b, *vetor_c;
    vetor_a = malloc(sizeof(int) * vetor_size);
    vetor_b = malloc(sizeof(int) * vetor_size);
    vetor_c = malloc(sizeof(int) * vetor_size);

    for (unsigned i = 0; i < vetor_size; i++) {
        vetor_a[i] = random_randint(0, 99);
        vetor_b[i] = random_randint(0, 99);
    }

    pthread_t threads[threads_number];
    Vetores *vetores;
    vetores = malloc(sizeof(Vetores) * threads_number);

    unsigned start = 0;
    unsigned remainder = vetor_size % threads_number;
    for (unsigned i = 0; i < threads_number; i++) {
        vetores[i].vetor_a = &vetor_a[0];
        vetores[i].vetor_b = &vetor_b[0];
        vetores[i].vetor_c = &vetor_c[0];
        vetores[i].start = start;
        if (remainder > 0) {
            vetores[i].end = start + (vetor_size / threads_number) + 1;
            remainder--;
        }
        else {
            vetores[i].end = start + (vetor_size / threads_number);
        }
        start = vetores[i].end;

        pthread_create(&threads[i], NULL, &multiplicacao, (void *)&vetores[i]);
    }

    for (unsigned i = 0; i < threads_number; i++) {
		pthread_join(threads[i], NULL);
	}

    printf("Vetor 1: ");
    for (unsigned i = 0; i < vetor_size; i++) {
        printf("%4i | ", vetor_a[i]);
    }
    
    printf("\nVetor 2: ");
    for (unsigned i = 0; i < vetor_size; i++) {
        printf("%4i | ", vetor_b[i]);
    }

    printf("\nVetor 3: ");
    for (unsigned i = 0; i < vetor_size; i++) {
        printf("%4i | ", vetor_c[i]);
    }
}