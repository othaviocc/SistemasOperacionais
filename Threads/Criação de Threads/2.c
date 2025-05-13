/*
Faça um programa que receba como entrada duas matrizes de inteiros A e B de tamanho MxN e realize a sua soma. 
A saída deverá ser armazenada em uma matriz C. O tamanho da matriz e o número de threads devem ser informados pelo usuário. 
Os elementos da matriz devem ser gerados de forma aleatória pelo programa. 
O programa deverá imprimir na tela as matrizes de entrada e a matriz de saída.
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <pthread.h>
#define random_randint(min, max) (min + rand() / (RAND_MAX / max - min + 1) + 1)

typedef struct {
    int **matrix_a;
    int **matrix_b;
    int **matrix_c;
    unsigned columns;
    unsigned start;
    unsigned end;
} Matrizes;

void *soma(void *i) {
    Matrizes *ptr = (Matrizes *)i;

    for (unsigned i = ptr->start; i < ptr->end; i++) {
        ptr->matrix_c[i/ptr->columns][i%ptr->columns] = ptr->matrix_a[i/ptr->columns][i%ptr->columns] + ptr->matrix_b[i/ptr->columns][i%ptr->columns];
    }
}

void main() {
    srand(time(NULL));

    unsigned rows, columns, threads_number;
    printf("Insira o numero de linhas da matriz: ");
    scanf("%u", &rows);

    printf("Insira o numero de colunas da matriz: ");
    scanf("%u", &columns);

    printf("Insira o numero de threads: ");
    scanf("%u", &threads_number);

    int **matrix_a, **matrix_b, **matrix_c;
    matrix_a = malloc(sizeof(int *) * rows);
    matrix_b = malloc(sizeof(int *) * rows);
    matrix_c = malloc(sizeof(int *) * rows);

    for (unsigned i = 0; i < rows; i++) {
        matrix_a[i] = malloc(sizeof(int) * columns);
        matrix_b[i] = malloc(sizeof(int) * columns);
        matrix_c[i] = malloc(sizeof(int) * columns);
    }

    for (unsigned i = 0; i < rows; i++) {
        for (unsigned j = 0; j < columns; j++) {
            matrix_a[i][j] = random_randint(0, 99);
            matrix_b[i][j] = random_randint(0, 99);
        }
    }

    pthread_t threads[threads_number];
    Matrizes *matrix;
    matrix = malloc(sizeof(Matrizes) * threads_number);

    unsigned start = 0;
    unsigned remainder = (rows * columns) % threads_number;
    for (unsigned i = 0; i < threads_number; i++) {
        matrix[i].matrix_a = &matrix_a[0];
        matrix[i].matrix_b = &matrix_b[0];
        matrix[i].matrix_c = &matrix_c[0];
        matrix[i].columns = columns;
        matrix[i].start = start;
        if (remainder > 0) {
            matrix[i].end = start + ((rows * columns) / threads_number) + 1;
            remainder--;
        }
        else {
            matrix[i].end = start + ((rows * columns) / threads_number);
        }
        start = matrix[i].end;

        pthread_create(&threads[i], NULL, &soma, (void *)&matrix[i]);
    }

    for (unsigned i = 0; i < threads_number; i++) {
		pthread_join(threads[i], NULL);
	}

    printf("Matriz 1:\n");
    for (unsigned i = 0; i < rows; i++) {
        for (unsigned j = 0; j < columns; j++) {
            printf("%3i ", matrix_a[i][j]);
        }
        printf("\n");
    }
    
    printf("Matriz 2:\n");
    for (unsigned i = 0; i < rows; i++) {
        for (unsigned j = 0; j < columns; j++) {
            printf("%3i ", matrix_b[i][j]);
        }
        printf("\n");
    }

    printf("Matriz 3:\n");
    for (unsigned i = 0; i < rows; i++) {
        for (unsigned j = 0; j < columns; j++) {
            printf("%3i ", matrix_c[i][j]);
        }
        printf("\n");
    }
}
