#include <stdio.h>
#include <unistd.h>

int main() { 
    char resA = 'a';
    char resB;
    write(1, &resA, 1);
    read(0, &resB, 1);
    FILE *f = fopen("resA", "w");
    fprintf(f, "A[%c]\n", resB);
    fclose(f);
}