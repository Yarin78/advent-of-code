#include <cstdio>
#include <set>

using namespace std;

int main() {
    long long A,B,C,D,E,F;
    printf("hello\n");
    A = 0;
    long long lastD = 0;
    set<long long> seen = set<long long>();


    D = 0;
    START:
    E = D | 65536;
    D = 7041048;
    FOO:
    F = E & 255;
    D = D + F;
    D &= 16777215;
    D *= 65899;
    D &= 16777215;
    if (256 > E) {
        //printf("A = %lld, B = %lld, C = %lld, D = %lld, E = %lld, F = %lld\n", A, B, C, D, E, F);
        if (A == D) {
            printf("DONE!");
            return 0;
        }
        if (seen.count(D)) {
            printf("REPEAT\n");
            printf("lastD = %lld\n", lastD);
            return 0;
        }
        lastD = D;
        seen.insert(D);
        goto START;
    }
    F = 0;
    LOOP:
    B = F + 1;
    B *= 256;
    if (B > E) {
        E = F;
        goto FOO;
    }
    F += 1;
    goto LOOP;

}
