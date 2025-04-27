/*
Faça um programa que crie um processo filho. Este processo filho, ao invés de executar o 
mesmo código definido pelo pai, deve executar um processo informado pelo usuário. Para isso 
sugere-se utilizar a função execl() (em C).
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

char *returnArchiveName(char *str) {
    int x;
    for (int i = 0; i < strlen(str); i++) {
        if (str[i] == '/') {
            x = i;
        }
    }
    char *ptr = &str[x + 1];
    return ptr;
}

int main() {
    pid_t newPid, me, parent;
    char path[100];
    int status;

    printf("Insira o caminho do arquivo: ");
    fgets(path, 100, stdin);
    path[strcspn(path, "\n")] = 0;
   
    char *archiveName = malloc(sizeof(char) * strlen(path));
    archiveName = returnArchiveName(path);

    newPid = fork();
    me = getpid();
    parent = getppid();
   
    if (newPid != 0) {
        waitpid(newPid, &status, 0);
        printf("\nPrograma finalizado!\n");
    }
    else {
        newPid = fork();
        if (newPid != 0) {
            waitpid(newPid, &status, 0);
            printf("Processo filho e execucao finalizados");
        }
        else {
            execl(path, archiveName, NULL);
        }
    }
   
    return 0;
}