#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/stat.h>
//zmq
#include <zmq.hpp>
//kbhit
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
    // 空のファイル作成
    FILE *fp;
    const string file_path = "./key.dat";
    fp = fopen(file_path.c_str(), "w");
    fclose(fp);

    // IPC keyの取得
    const int id = 50;
    const key_t key = ftok(file_path.c_str(), id);
    if(key == -1){
        cerr << "Failed to acquire key" << endl;
        return EXIT_FAILURE;
    }

    // 共有メモリIDの取得
    const int size = 0x6400;
    const int seg_id = shmget(key, size,
                              IPC_CREAT | IPC_EXCL | S_IRUSR | S_IWUSR);
    if(seg_id == -1){
        cerr << "Failed to acquire segment" << endl;
        return EXIT_FAILURE;
    }

    // shmat:作成した共有メモリをプロセスのアドレス空間にアタッチする
      // 共有メモリ用のアドレスを取得(shmat). そこをshared_memory変数のアドレスにする
      // -> そこに文字列いれれば完了

    //char* const shared_memory = reinterpret_cast<char*>(shmat(seg_id, 0, 0));
    double* const shared_memory = reinterpret_cast<double*>(shmat(seg_id, 0, 0));
    // 共有メモリに書き込む
    /*
    string s;
    int flag = 0;
    cout << "if you want to close, please type 'q'" << endl;
    while(flag == 0){
        cout << "word: ";
        cin >> s;
        if(s == "q") flag = 1;
        else sprintf(shared_memory, s.c_str());
    }
    */
    string s;
    s = "test";


    double pupilAngleX, pupilAngleY;
    int cnt = 0;

    puts("type any key to exit\n");
    while(1)
    {
          if(kbhit())
          {
              printf("--break--\n");
              break;
          }

          //main process that receives data
          printf("...\n");
          //Setting ZMQ
          zmq::context_t context(1);
          zmq::socket_t socket(context, ZMQ_REP);
          socket.bind("tcp://127.0.0.1:5553");    // if needed, put sleep to wait for socket to be properly bounded
          //printf("\n -- Refreshed data --\n");
          while(1)
          {
                zmq::message_t rcv_msg;
                socket.recv(&rcv_msg, 0);
                switch(cnt)
                  {
                  case 0:
                    pupilAngleX = *(double*)rcv_msg.data();
                    printf("degX : %f \n", pupilAngleX);
                    *shared_memory = pupilAngleX;
                    printf("address: %d,  *shared_memory: %f \n", shared_memory, *shared_memory);
                  //  sprintf(shared_memory, s.c_str());
                  //  printf("address: %d , *shared_memory: %c\n", shared_memory, *shared_memory);
                    cnt = 1;
                    break;
                  case 1:
                    pupilAngleY = *(double*)rcv_msg.data();
                    //printf("degY : %f \n", pupilAngleY);
                    cnt = 0;
                    break;
                }
                if( !rcv_msg.more() )
                {
                  //printf("--a loop ende \n");
                  break;
                }
          }

    }


    // 共有メモリをプロセスから切り離す
    shmdt(shared_memory);

    // 共有メモリを解放する
    shmctl(seg_id, IPC_RMID, NULL);
    printf("Releasing shared memory done\n");

    return 0;
}
