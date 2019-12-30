#include <iostream>

using namespace std;

typedef long long ll;

int run(ll a) {
    ll b = 0, c = 0, d = 0;
    int expected = 0, matched = 0;

    d=a;
    d += 2532;
MAIN_LOOP:
    a=d;
FOO:
    b=a;
    a=0;
LOOP_A:
    c=2;
LOOP_B:
    if (b==0) goto LBL_A;
    b--;
    c--;
    if (c!=0) goto LOOP_B;
    a++;
    goto LOOP_A;
LBL_A:
    b=2;
LOOP_C:
    if (c == 0) goto LBL_B;
    b--;
    c--;
    goto LOOP_C;
LBL_B:
    if (b != expected) return false;
    expected = 1-expected;
    matched++;
    if (matched == 100) return true;
    if (a != 0) goto FOO;
    goto MAIN_LOOP;
}

int main() {
    for(int a=0;;a++) {
        if (a%1000 == 0) cout << "a = " << a << endl;
        if (run(a)) {
            cout << "DONE at a = " << a << endl;
            return 0;
        }
    }
}
