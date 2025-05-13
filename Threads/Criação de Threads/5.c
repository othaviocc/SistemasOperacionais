/*
Faça um programa que, dado um diretório com arquivos de texto no formato .txt, calcule as seguintes estatísticas para cada arquivo. 
Número de palavras, número de vogais, número de consoantes, palavra que apareceu mais vezes no arquivo, vogal mais frequente, consoante mais frequente. 
Além disso, para cada arquivo do diretório, o programa deverá gerar um novo arquivo, contendo o conteúdo do arquivo original escrito em letras maiúsculas.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <glob.h>

#define HASH_K_SIZE 53

struct node {
    char *word;
    unsigned times;
    struct node *next;
};

struct ArchiveStats {
    char *archive_path;
    struct node *words;
    unsigned *letters;
    char *word;
    unsigned word_times;
    char vowel;
    unsigned vowel_times;
    char consonant;
    unsigned consonant_times;
};

int hash_key(char *str) {
    unsigned hash = 0;
    for (unsigned i = 0; i < strlen(str); i++) {
        hash = hash * 31 + (int)str[i];
    }
    return hash % HASH_K_SIZE;
}

void string_uppercase(char *str) {
    for (unsigned i = 0; i < strlen(str); i++) {
        if ((str[i] >= 'a') && (str[i] <= 'z')) {
            str[i] = str[i] - 32;
        }
    }
}

void most_common_word(struct ArchiveStats *archive_info) {
    for (int i = 0; i < HASH_K_SIZE; i++) {
        struct node *node = &archive_info->words[i];
        while (node != NULL && node->word != NULL) {
            if (node->times > archive_info->word_times) {
                strcpy(archive_info->word, node->word);
                archive_info->word_times = node->times;
            }
            node = node->next;
        }
    }
}

void most_common_letters(struct ArchiveStats *archive_info) {
    for (int i = 0; i < 26; i++) {
        if (i == ('A' - 'A') || i == ('E' - 'A') || i == ('I' - 'A') || i == ('O' - 'A') || i == ('U' - 'A')) {
            if (archive_info->letters[i] > archive_info->vowel_times) {
                archive_info->vowel = (char)(i + 'A');
                archive_info->vowel_times = archive_info->letters[i];
            }
        } else {
            if (archive_info->letters[i] > archive_info->consonant_times) {
                archive_info->consonant = (char)(i + 'A');
                archive_info->consonant_times = archive_info->letters[i];
            }
        }
    }
}

void save_txt(struct ArchiveStats *archive_info, char *buffer) {
    FILE *archive;
    char *save_path = malloc(sizeof(char) * (strlen(archive_info->archive_path) + 11));
    save_path = strcpy(save_path, archive_info->archive_path);
    save_path[strlen(save_path) - 4] = 0;
    save_path = strcat(save_path, "_uppercase.txt");
    archive = fopen(save_path, "a");

    fprintf(archive, buffer);

    fclose(archive);

    free(save_path);
}

void *archive_stats(void *i) {
    struct ArchiveStats *archive_info = (struct ArchiveStats *)i;

    archive_info->words = malloc(sizeof(struct node) * HASH_K_SIZE);
    archive_info->letters = calloc(26, sizeof(unsigned));
    archive_info->word = calloc(100, sizeof(char));
    archive_info->word_times = 0;
    archive_info->vowel = '\0';
    archive_info->vowel_times = 0;
    archive_info->consonant = '\0';
    archive_info->consonant_times = 0;

    for (int i = 0; i < HASH_K_SIZE; i++) {
        archive_info->words[i].word = NULL;
        archive_info->words[i].times = 0;
        archive_info->words[i].next = NULL;
    }

    FILE *archive = fopen(archive_info->archive_path, "r");
    if (!archive) {
        perror("Erro ao abrir arquivo");
        return NULL;
    }

    char buffer[1024];
    while (fgets(buffer, sizeof(buffer), archive)) {
        string_uppercase(buffer);

        save_txt(archive_info, buffer);

        for (int i = 0; i < strlen(buffer); i++) {
            if (buffer[i] >= 'A' && buffer[i] <= 'Z') {
                archive_info->letters[buffer[i] - 'A']++;
            }
        }

        char *token = strtok(buffer, " ,.!?:;\n");
        while (token != NULL) {
            int key = hash_key(token);
            struct node *node = &archive_info->words[key];

            while (node != NULL && node->word != NULL) {
                if (strcmp(token, node->word) == 0) {
                    node->times++;
                    break;
                }
                if (node->next == NULL) {
                    node->next = malloc(sizeof(struct node));
                    node = node->next;
                    node->word = NULL;
                    node->next = NULL;
                } else {
                    node = node->next;
                }
            }

            if (node->word == NULL) {
                node->word = malloc(strlen(token) + 1);
                strcpy(node->word, token);
                node->times = 1;
                node->next = NULL;
            }

            token = strtok(NULL, " ,.!?:;\n");
        }
    }

    fclose(archive);
    most_common_word(archive_info);
    most_common_letters(archive_info);

    return NULL;
}

int main() {
    char *dir = malloc(sizeof(char) * 200);
    printf("Insira o diretorio: ");
    fgets(dir, 200, stdin);
    dir[strcspn(dir, "\n")] = 0;
    strcat(dir, "/*");

    glob_t glob_data;
    if (glob(dir, GLOB_NOSORT, NULL, &glob_data) != 0) {
        perror("Erro ao ler diretório");
        return 1;
    }

    int n_archives = glob_data.gl_pathc;
    pthread_t threads[n_archives];
    struct ArchiveStats *archive_info = malloc(sizeof(struct ArchiveStats) * n_archives);

    for (int i = 0; i < n_archives; i++) {
        archive_info[i].archive_path = malloc(strlen(glob_data.gl_pathv[i]) + 1);
        strcpy(archive_info[i].archive_path, glob_data.gl_pathv[i]);
        pthread_create(&threads[i], NULL, archive_stats, &archive_info[i]);
    }

    for (int i = 0; i < n_archives; i++) {
        pthread_join(threads[i], NULL);
    }

    for (int i = 0; i < n_archives; i++) {
        printf("Arquivo: %s\n", archive_info[i].archive_path);
        printf("Palavra mais frequente: %s (%u vezes)\n", archive_info[i].word, archive_info[i].word_times);
        printf("Vogal mais frequente: %c (%u vezes)\n", archive_info[i].vowel, archive_info[i].vowel_times);
        printf("Consoante mais frequente: %c (%u vezes)\n", archive_info[i].consonant, archive_info[i].consonant_times);
        printf("------------------------------------------------------\n");
    }

    globfree(&glob_data);
    return 0;
}
