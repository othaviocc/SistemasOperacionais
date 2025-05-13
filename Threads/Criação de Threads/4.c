/*
Faça um programa que multiplique duas matrizes A e B, cujos dimensões são MxN e NxP, onde M pode ou não ser igual a P. 
O tamanho das matrizes e o número de threads devem ser informados pelo usuário. 
Os valores das matrizes devem ser gerados de forma aleatória pelo programa. 
O programa deverá imprimir na tela as matrizes A e B bem como o resultado da sua multiplicação.
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <pthread.h>
#define digits_number(x) ((int)log10(x) + 1)
#define random_randint(min, max) (min + rand() / (RAND_MAX / max - min + 1) + 1)

// matrix_a = mxn, matrix_b = nxp, matrix_c = mxp

typedef struct {
    int **matrix_a;
    int **matrix_b;
    int **matrix_c;
    unsigned n;
    unsigned p;
    unsigned start;
    unsigned end;
} Matrizes;

void *multiply(void *i) {
    Matrizes *ptr = (Matrizes *)i;

    for (unsigned i = ptr->start; i < ptr->end; i++) {
        for (unsigned j = 0; j < ptr->n; j++) {
            ptr->matrix_c[i/ptr->p][i%ptr->p] = (ptr->matrix_c[i/ptr->p][i%ptr->p] + (ptr->matrix_a[i/ptr->p][j] * ptr->matrix_b[j][i%ptr->p]));
        }
    }
}

void main() {
    srand(time(NULL));

    unsigned m, n, p, threads_number;
    printf("Insira o numero de linhas da matriz A: ");
    scanf("%u", &m);

    printf("Insira o numero de colunas da matriz A e linhas da matriz B: ");
    scanf("%u", &n);

    printf("Insira o numero de colunas da matriz B: ");
    scanf("%u", &p);

    printf("Insira o numero de threads: ");
    scanf("%u", &threads_number);


    int **matrix_a, **matrix_b, **matrix_c;
    matrix_a = malloc(sizeof(int *) * m);
    matrix_b = malloc(sizeof(int *) * n);
    matrix_c = malloc(sizeof(int *) * m);
    

    for (unsigned i = 0; i < m; i++) {
        matrix_a[i] = malloc(sizeof(int) * n);
        matrix_c[i] = malloc(sizeof(int) * p);
    }

    for (unsigned i = 0; i < n; i++) {
        matrix_b[i] = malloc(sizeof(int) * p);
    }

    for (unsigned i = 0; i < m; i++) {
        for (unsigned j = 0; j < n; j++) {
            matrix_a[i][j] = random_randint(0, 99);
        }
    }

    for (unsigned i = 0; i < n; i++) {
        for (unsigned j = 0; j < p; j++) {
            matrix_b[i][j] = random_randint(0, 99);
        }
    }

    pthread_t threads[threads_number];
    Matrizes *matrices;
    matrices = malloc(sizeof(Matrizes) * threads_number);

    unsigned start = 0;
    unsigned remainder = (m * p) % threads_number;
    for (unsigned i = 0; i < threads_number; i++) {
        matrices[i].matrix_a = &matrix_a[0];
        matrices[i].matrix_b = &matrix_b[0];
        matrices[i].matrix_c = &matrix_c[0];
        matrices[i].n = n;
        matrices[i].p = p;
        matrices[i].start = start;
        if (remainder > 0) {
            matrices[i].end = start + (m * p / threads_number) + 1;
            remainder--;
        }
        else {
            matrices[i].end = start + (m * p / threads_number);
        }
        start = matrices[i].end;

        pthread_create(&threads[i], NULL, &multiply, (void *)&matrices[i]);
    }

    for (unsigned i = 0; i < threads_number; i++) {
		pthread_join(threads[i], NULL);
	}

    int max_digits = digits_number(9801 * n);

    printf("Matriz A:\n");
    for (unsigned i = 0; i < m; i++) {
        for (unsigned j = 0; j < n; j++) { 
            printf("%*i ", max_digits, matrix_a[i][j]);
        }
        printf("\n");
    }

    printf("Matriz B:\n");
    for (unsigned i = 0; i < n; i++) {
        for (unsigned j = 0; j < p; j++) {
            printf("%*i ", max_digits, matrix_b[i][j]);
        }
        printf("\n");
    }

    printf("Matriz C:\n");
    for (unsigned i = 0; i < m; i++) {
        for (unsigned j = 0; j < p; j++) {
            printf("%*i ", max_digits, matrix_c[i][j]);
        }
        printf("\n");
    }
}
