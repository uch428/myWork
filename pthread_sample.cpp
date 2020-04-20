#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
// kbhit
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>
int a;





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


// 新しいスレッドで実行されるタスク
void *doSomething(void* pArg) {
    int *pVal = (int*) pArg;
    printf("worker thread [%d]\n", *pVal);
    *pVal = 200;
    a = 20;
    while(1)
    {
        a += 1;
        // printf(".");
        sleep(1);
    }
    return 0;
}



int main() {
    pthread_t handle;  // Thread handle.
    int data = 100;
    a = 10;
    pthread_create(&handle, NULL, doSomething, &data);

    printf("main thread [%d]\n", data);
    while(!kbhit())
    {
        printf("a = %d \n", a);

    }
    printf("--");
//    pthread_join(handle, NULL);
    int pthread_detach(pthread_t handle);
    printf("--");

}
