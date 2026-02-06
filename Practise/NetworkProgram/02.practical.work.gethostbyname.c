#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netdb.h>
#include <arpa/inet.h>

int main(int argc, char *argv[]) {
    char domain[256];

    // 1️⃣ Lấy domain
    if (argc >= 2) {
        strncpy(domain, argv[1], sizeof(domain) - 1);
        domain[sizeof(domain) - 1] = '\0';
    } else {
        if (fgets(domain, sizeof(domain), stdin) == NULL) {
            fprintf(stderr, "No input\n");
            return 1;
        }
        domain[strcspn(domain, "\n")] = '\0'; // bỏ newline
    }

    // 2️⃣ Resolve domain
    struct hostent *he = gethostbyname(domain);
    if (he == NULL) {
        herror("gethostbyname");
        return 1;
    }

    // 3️⃣ In IP
    struct in_addr **addr_list =
        (struct in_addr **) he->h_addr_list;

    for (int i = 0; addr_list[i] != NULL; i++) {
        printf("%s\n", inet_ntoa(*addr_list[i]));
    }

    return 0;
}
