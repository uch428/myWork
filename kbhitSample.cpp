//#include <stdio.h>
#include <cstdio>
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>
int kbhit(void)
{
    struct termios oldt, newt;
    int ch;
    int oldf;

    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);
    oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
    fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);

    ch = getchar();

    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    fcntl(STDIN_FILENO, F_SETFL, oldf);

    if (ch != EOF) {
        ungetc(ch, stdin);
        return 1;
    }

    return 0;
}

int main(void)
{
    puts("何かキーを押したら終了します。");

    while (1) {
        if (kbhit()) {
            printf("'%c'を押しました。\n", getchar());
            break;
        }
        printf(".");
    }

    return 0;
}

// https://hotnews8.net/programming/tricky-code/c-code03
