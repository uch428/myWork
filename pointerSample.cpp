#include <cstdio>
using namespace std;



int main(void)
{
    int a;
    int* p;

    a = 3;
    printf("aのアドレス: %p \n", &a);

    p = &a;
    printf("ポインタ変数pの値(=アドレス): %p \n", p);
    printf("ポインタ変数p(アドレス)が指す値: %d \n", *p);
    return 0;
}
