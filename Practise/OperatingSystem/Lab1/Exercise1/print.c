#include <stdio.h>
#include <unistd.h>

int main() {
    char buf[1024];
    int nb;

    while (1) {
        nb = read(0, buf, sizeof(buf));
        if (nb == 0) return 0;

        buf[nb] = 0;
        printf(" print : %s\n", buf);
    }
}