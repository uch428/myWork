#include <zmq.hpp>

int main()
{
    zmq::context_t context(1);
    zmq::socket_t socket(context, ZMQ_REQ);
    zmq::message_t request(10);
    zmq::detail::send_result_t res = socket.send(request, zmq::send_flags::none);
}
