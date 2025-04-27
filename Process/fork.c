#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

int main()
{

    pid_t newPid, me, parent, x;
    int status;

    newPid = fork();

    me = getpid();
    parent = getppid();

    printf("%d, %d, %d\n", me, parent, newPid);

    if (newPid != 0)
    {
        printf("Esperando filho pid %d\n", newPid);
        x = waitpid(newPid, &status, 0);
        printf("Filho %d terminou\n", x);
    }
    else
    {
        printf("Sou o filho\n");
        sleep(5);
    }

    return 0;
}