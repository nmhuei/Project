#include <stdio.h>
#include <unistd.h>

int main() { 
    char resB = 'b';
    char resA;
    write(1, &resB, 1);
    read(0, &resA, 1);
    FILE *f = fopen("resB", "w");
    fprintf(f, "A[%c]\n", resA);
    fclose(f);
}