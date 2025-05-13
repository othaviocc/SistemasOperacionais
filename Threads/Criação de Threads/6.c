/*
Faça um programa que produza uma versão em escala de cinza de uma imagem colorida.
*/

#define STB_IMAGE_IMPLEMENTATION 
#include "include/stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "include/stb_image_write.h"
#include <stdio.h> 
#include <stdlib.h>
#include <math.h>
#include <pthread.h>

struct auxiliar {
    unsigned char *image_data;
    int channels;
    unsigned start;
    unsigned end;
};
 
void saveImage(const char *filename, unsigned char *image_data, int width, int height, int channels) {
    char extension[10];
    strcpy(extension, &filename[strcspn(filename, ".")]);
    char *path = malloc(sizeof(char) * (strlen(filename) + 6));
    strcpy(path, filename);
    path[strcspn(path, ".")] = 0;
    strcat(path, "_gray");
    strcat(path, extension);
    int success = stbi_write_jpg(path, width, height, channels, image_data, 100);
    if (!success) {
        printf("Erro ao salvar a imagem!\n");
        exit(1);
    }
    printf("Imagem salva com sucesso: %s\n", path);
}

void *change_pixels(void *i) {
    struct auxiliar *aux;
    aux = (struct auxiliar *)i;
    for (unsigned i = aux->start; i < aux->end; i++) {
        int idx = i * aux->channels;
        int pixel_color = round(aux->image_data[idx] * 0.299 + aux->image_data[idx + 1] * 0.587 + aux->image_data[idx + 2] * 0.114);
        aux->image_data[idx] = aux->image_data[idx + 1] = aux->image_data[idx + 2] = pixel_color;
    }
}

void main() { 
    char *filename = malloc(sizeof(char) * 200);
    printf("Insira o caminho para a imagem: ");
    fgets(filename, 200, stdin);
    filename[strcspn(filename, "\n")] = 0;
    unsigned char *image_data;
    int width, height, channels; 

    image_data = stbi_load(filename, &width, &height, &channels, 0);

    if (image_data == NULL) {
        printf("Erro ao carregar a imagem: %s\n", filename);
        exit(1);
    }
    
    unsigned threads_number = ((width * height) / 100) + 1;
    unsigned start = 0;
    unsigned remainder = (width * height) % threads_number;
    pthread_t threads[threads_number];
    struct auxiliar aux[threads_number];

    if (channels >= 3) { 
        for (unsigned i = 0; i < threads_number; i++) {
            aux[i].channels = channels;
            aux[i].image_data = image_data;
            aux[i].start = start;
            if (remainder > 0) {
                aux[i].end = start + (width * height / threads_number) + 1;
                remainder--;
            }
            else {
                aux[i].end = start + (width * height / threads_number);
            }
            start = aux[i].end;

            pthread_create(&threads[i], NULL, &change_pixels, (void *)&aux[i]);
        }

        for (unsigned i = 0; i < threads_number; i++) {
            pthread_join(threads[i], NULL);
        }
    } 
    else {
        perror("Imagem não possui 3 ou mais canais!");
        exit(1);
    }

    saveImage(filename, image_data, width, height, channels);

    stbi_image_free(image_data);
} 