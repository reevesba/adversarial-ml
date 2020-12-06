#include <stdio.h>
#include <string.h>

int main(void)
{
    char username[16];
    char password[16];

    printf("User name: \n");
    gets(username);

    printf("Password: \n");
    gets(password);

    if (strcmp(username, "admin") == 0) {
        if (strcmp(password, "3Kg3H5dN") ==0) {
            printf("Access Granted.\n");
            return 0;
        }
    }

    printf("Access Denied.\n");
    return 1;
}
