#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/stat.h>
// kbhit
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>
using namespace std;

// -pthreadオプションがコンパイル時に必要
// $ g++ -o thread_rM_sample thread_rM_sample.cpp -o -pthread


// 作成済みの共有メモリのIDを取得する
const string file_path = "./key.dat";
const int id = 50;
const key_t key = ftok(file_path.c_str(), id);
const int seg_id = shmget(key, 0, 0);

double* const shared_memory = reinterpret_cast<double*>(shmat(seg_id, 0, 0));
double angle = 0.0;



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

/*
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
*/

void* readMemory(void* args)
{
    printf("hit any key to exit\n");

    while(!kbhit())
    {
        angle = *shared_memory;
      //  printf("t_*shared memory: %f\n", *shared_memory);
      //  printf("t_angle: %f\n", angle);
    }

    return 0;
}



int main() {

    pthread_t thr_readMemory;  // Thread handle.

    pthread_create(&thr_readMemory, NULL, readMemory, (void *)NULL);


    while(!kbhit())
    {
        printf("main_angle  =  %f \n", angle);

    }
    printf("--");

    shmdt(shared_memory);
    printf("detaching memory done \n");
//    pthread_join(handle, NULL);
    int pthread_detach(pthread_t thr_readMemory);
    printf("--");

    return 0;
}
