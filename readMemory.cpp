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


int main(int argc, char*argv[])
{
    // 作成済みの共有メモリのIDを取得する
    const string file_path = "./key.dat";
    const int id = 50;
    const key_t key = ftok(file_path.c_str(), id);
    const int seg_id = shmget(key, 0, 0);
    if(seg_id == -1){
        cerr << "Failed to acquire segment" << endl;
        return EXIT_FAILURE;
    }

    // 共有メモリをプロセスにアタッチする
//    char* const shared_memory = reinterpret_cast<char*>(shmat(seg_id, 0, 0));
    double* const shared_memory = reinterpret_cast<double*>(shmat(seg_id, 0, 0));

    // 共有メモリを読み取る
    int flag = 0;


    char c;
    double angle;
    printf("hit any key to end the program\n");
    /*
    while(flag == 0){
        cin.get(c);
        if(c == 'q') flag = 1;
        else
        {
          angle = *shared_memory;
          printf("%f\n", *shared_memory);
        }
    }
    */



    while(!kbhit())
    {
        angle = *shared_memory;
        printf("%f\n", *shared_memory);

    }

    // 共有メモリをプロセスから切り離す
    shmdt(shared_memory);
    printf("detaching memory done \n");
    return 0;
}
