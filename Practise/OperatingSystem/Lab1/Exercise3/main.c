#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main() {
    int pipe1[2]; // ps -> grep
    int pipe2[2]; // grep -> wc

    if (pipe(pipe1) == -1) {
        perror("pipe1");
        exit(1);
    }

    if (pipe(pipe2) == -1) {
        perror("pipe2");
        exit(1);
    }

    // ===== Process 1: ps -ef =====
    if (fork() == 0) {
        // stdout -> pipe1 write end
        dup2(pipe1[1], STDOUT_FILENO);

        close(pipe1[0]);
        close(pipe1[1]);
        close(pipe2[0]);
        close(pipe2[1]);

        execlp("ps", "ps", "-ef", NULL);
        perror("execlp ps");
        exit(1);
    }

    // ===== Process 2: grep firefox =====
    if (fork() == 0) {
        // stdin <- pipe1 read end
        dup2(pipe1[0], STDIN_FILENO);
        // stdout -> pipe2 write end
        dup2(pipe2[1], STDOUT_FILENO);

        close(pipe1[0]);
        close(pipe1[1]);
        close(pipe2[0]);
        close(pipe2[1]);

        execlp("grep", "grep", "firefox", NULL);
        perror("execlp grep");
        exit(1);
    }

    // ===== Process 3: wc -l =====
    if (fork() == 0) {
        // stdin <- pipe2 read end
        dup2(pipe2[0], STDIN_FILENO);

        close(pipe1[0]);
        close(pipe1[1]);
        close(pipe2[0]);
        close(pipe2[1]);

        execlp("wc", "wc", "-l", NULL);
        perror("execlp wc");
        exit(1);
    }

    // Parent: đóng hết fd
    close(pipe1[0]);
    close(pipe1[1]);
    close(pipe2[0]);
    close(pipe2[1]);

    return 0;
}
