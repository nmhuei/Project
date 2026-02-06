#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main() {
    int p[2];
    pipe(p);

    int pid = fork();
    // Child Process
    if (pid == 0) {
        dup2(p[0], 0);
        close(p[1]);
        close(p[0]);

        execlp("./print", "print", NULL);
    }

    // Parent Process
    dup2(p[1], 1);
    close(p[0]);
    close(p[1]);
    execlp("./gendoc", "gendoc", NULL);
}