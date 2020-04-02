#include <zmq.hpp>
// 参考 http://blog.livedoor.jp/tmako123-programming/archives/51046977.html
// 参考2 http://blog.futurestandard.jp/entry/2017/03/02/143449
//ライブラリ https://pyzmq.readthedocs.io/en/latest/api/zmq.html

int main(int argc, char*argv[])
{
  double diameter, angle;
 // double data[] = {diameter, angle};
  int cnt = 0;
  while(1)
    {
    //Setting ZMQ
    zmq::context_t context(1);
    zmq::socket_t socket(context, ZMQ_REP);
    socket.bind("tcp://127.0.0.1:5553");    // if needed, put sleep to wait for socket to be properly bounded
    printf("\n -- Refreshed data --\n");
    while(1)
    {
      zmq::message_t rcv_msg;
      socket.recv(&rcv_msg, 0);
      switch(cnt)
      {
        case 0:
          diameter = *(double*)rcv_msg.data();
          printf("dia : %f \n", diameter);
          cnt = 1;
          break;
        case 1:
          angle = *(double*)rcv_msg.data();
          printf("angle : %f \n", angle);
          cnt = 0;
          break;
      }
      if( !rcv_msg.more() )
      {
        printf("a loop ended \n");
        break;
      }
    }
  }
}
//受信
