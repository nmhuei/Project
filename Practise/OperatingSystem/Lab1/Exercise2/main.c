#include <stdio.h>
#include <unistd.h>

int main() {
    int a2b[2];
    int b2a[2];

    pipe(a2b);
    pipe(b2a);

    if (fork() == 0) {
        // proc A
        dup2(a2b[0], 1);
        dup2(b2a[0], 0);
        close(a2b[0]);  close(a2b[1]);
        close(b2a[0]);  close(b2a[1]);

        execlp("./A", "A", NULL);
    }
    // proc B

    dup2(a2b[0], 0);
    dup2(b2a[0], 1);
    close(a2b[0]);  close(a2b[1]);
    close(b2a[0]);  close(b2a[1]);

    execlp("./B", "B", NULL);
}
