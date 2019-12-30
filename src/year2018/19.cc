#include <cstdio>
#include <cstdlib>
#include <cassert>

using namespace std;

int main() {
  long long a=1, b=0, c=0, d=0, e=0, f=0;

  goto addr_17;               // addi [5, 16, 5]
addr_1:
  e = 1;                      // seti [1, 8, 4]
addr_2:
  d = 1;                      // seti [1, 5, 3]
addr_3:
  b = e * d;                  // mulr [4, 3, 1]
  b = b == c ? 1 : 0;         // eqrr [1, 2, 1]
  assert(b == 0 || b == 1);
  if (b) goto addr_7;         // addr [1, 5, 5]
  goto addr_8;                // addi [5, 1, 5]
addr_7:
  a = e + a;                  // addr [4, 0, 0]
addr_8:
  d = d + 1;                  // addi [3, 1, 3]
  b = d > c ? 1 : 0;          // gtrr [3, 2, 1]
  assert(b == 0 || b == 1);
  if (b) goto addr_12;        // addr [5, 1, 5]
  goto addr_3;                // seti [2, 5, 5]
addr_12:
  e = e + 1;                  // addi [4, 1, 4]
  b = e > c ? 1 : 0;          // gtrr [4, 2, 1]
  assert(b == 0 || b == 1);
  if (b) goto addr_16;        // addr [1, 5, 5]
  goto addr_2;                // seti [1, 2, 5]
addr_16:
  printf("%lld\n", a);
  exit(0);
addr_17:
  c = c + 2;                  // addi [2, 2, 2]
  c = c * c;                  // mulr [2, 2, 2]
  c = 19 * c;                 // mulr [5, 2, 2]
  c = c * 11;                 // muli [2, 11, 2]
  b = b + 8;                  // addi [1, 8, 1]
  b = b * 22;                 // mulr [1, 5, 1]
  b = b + 18;                 // addi [1, 18, 1]
  c = c + b;                  // addr [2, 1, 2]
  assert(a == 0 || a == 1);
  if (a) goto addr_27;        // addr [5, 0, 5]
  goto addr_1;                // seti [0, 7, 5]
addr_27:
  b = 27;                     // setr [5, 0, 1]
  b = b * 28;                 // mulr [1, 5, 1]
  b = 29 + b;                 // addr [5, 1, 1]
  b = 30 * b;                 // mulr [5, 1, 1]
  b = b * 14;                 // muli [1, 14, 1]
  b = b * 32;                 // mulr [1, 5, 1]
  c = c + b;                  // addr [2, 1, 2]
  a = 0;                      // seti [0, 0, 0]
  goto addr_1;                // seti [0, 9, 5]
  return 0;
}
