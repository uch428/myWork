#include <GLFW/glfw3.h>
#include <iostream>
#include <thread>
#include <chrono>




void temp(){
    std::this_thread::sleep_for(std::chrono::seconds(3));
    glfwPostEmptyEvent();
}

int main() {
    GLFWwindow* window;

    if (!glfwInit()) return -1;

    window = glfwCreateWindow(640, 480, "Simple example", nullptr, nullptr);

    if (!window) {
        glfwTerminate();
        return -1;
    }

    // 3秒待ってから空イベントを投げる
    std::thread t1(temp);


    /*
    std::thread thd([]{
          std::this_thread::sleep_for(std::chrono::seconds(3));
          glfwPostEmptyEvent();
    });
    */

    t1.detach();

    //thd.detach();

    glfwMakeContextCurrent(window);
    while (!glfwWindowShouldClose(window)) {
        glfwSwapBuffers(window);

        // 外部イベント待ち
        // キーやマウス入力、glfwPostEmptyEventで待機解除
        glfwWaitEvents();

        std::cout << "WOW!!" << std::endl;
    }

    glfwTerminate();
}


// http://blog.livedoor.jp/tek_nishi/archives/8688303.html
