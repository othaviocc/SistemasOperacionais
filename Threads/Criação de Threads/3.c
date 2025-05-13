/*
Faça um programa que receba como entrada uma matriz de inteiro A de tamanho MxN e realize a sua transposição. 
A saída deverá ser armazenada em uma matriz B de tamanho NxM. O tamanho da matriz e o número de threads devem ser informados pelo usuário. 
Os elementos da matriz devem ser gerados de forma aleatória pelo programa. O programa deverá imprimir na tela as matrizes de entrada e de saída.
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <pthread.h>
#define random_randint(min, max) (min + rand() / (RAND_MAX / max - min + 1) + 1)

typedef struct {
    int **matrix;
    int **matrix_t;
    unsigned columns;
    unsigned start;
    unsigned end;
} Matrizes;

void *transpose(void *i) {
    Matrizes *ptr = (Matrizes *)i;

    for (unsigned i = ptr->start; i < ptr->end; i++) {
        ptr->matrix_t[i%ptr->columns][i/ptr->columns] = ptr->matrix[i/ptr->columns][i%ptr->columns];
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

    int **matrix, **matrix_t;
    matrix = malloc(sizeof(int *) * rows);
    matrix_t = malloc(sizeof(int *) * columns);

    for (unsigned i = 0; i < rows; i++) {
        matrix[i] = malloc(sizeof(int) * columns);
    }

    for (unsigned i = 0; i < columns; i++) {
        matrix_t[i] = malloc(sizeof(int) * rows);
    }

    for (unsigned i = 0; i < rows; i++) {
        for (unsigned j = 0; j < columns; j++) {
            matrix[i][j] = random_randint(0, 99);
        }
    }
    

    pthread_t threads[threads_number];
    Matrizes *matrices;
    matrices = malloc(sizeof(Matrizes) * threads_number);

    unsigned start = 0;
    unsigned remainder = (rows * columns) % threads_number;
    for (unsigned i = 0; i < threads_number; i++) {
        matrices[i].matrix = &matrix[0];
        matrices[i].matrix_t = &matrix_t[0];
        matrices[i].columns = columns;
        matrices[i].start = start;
        if (remainder > 0) {
            matrices[i].end = start + ((rows * columns) / threads_number) + 1;
            remainder--;
        }
        else {
            matrices[i].end = start + ((rows * columns) / threads_number);
        }
        start = matrices[i].end;

        pthread_create(&threads[i], NULL, &transpose, (void *)&matrices[i]);
    }

    for (unsigned i = 0; i < threads_number; i++) {
		pthread_join(threads[i], NULL);
	}

    printf("Matriz N:\n");
    for (unsigned i = 0; i < rows; i++) {
        for (unsigned j = 0; j < columns; j++) {
            printf("%2i ", matrix[i][j]);
        }
        printf("\n");
    }

    printf("Matriz T:\n");
    for (unsigned i = 0; i < columns; i++) {
        for (unsigned j = 0; j < rows; j++) {
            printf("%2i ", matrix_t[i][j]);
        }
        printf("\n");
    }
}
