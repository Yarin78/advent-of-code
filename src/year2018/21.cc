#include <cstdio>
#include <cstdlib>
#include <cassert>

using namespace std;

int main() {
  long long a=0, b=0, c=0, d=0, e=0, f=0;

  d = 123;                    // seti [123, 0, 3]
addr_1:
  d = d & 456;                // bani [3, 456, 3]
  d = d == 72 ? 1 : 0;        // eqri [3, 72, 3]
  assert(d == 0 || d == 1);
  if (d) goto addr_5;         // addr [3, 2, 2]
  goto addr_1;                // seti [0, 0, 2]
addr_5:
  d = 0;                      // seti [0, 6, 3]
addr_6:
  e = d | 65536;              // bori [3, 65536, 4]
  d = 7041048;                // seti [7041048, 8, 3]
addr_8:
  f = e & 255;                // bani [4, 255, 5]
  d = d + f;                  // addr [3, 5, 3]
  d = d & 16777215;           // bani [3, 16777215, 3]
  d = d * 65899;              // muli [3, 65899, 3]
  d = d & 16777215;           // bani [3, 16777215, 3]
  f = 256 > e ? 1 : 0;        // gtir [256, 4, 5]
  assert(f == 0 || f == 1);
  if (f) goto addr_16;        // addr [5, 2, 2]
  goto addr_17;               // addi [2, 1, 2]
addr_16:
  goto addr_28;               // seti [27, 6, 2]
addr_17:
  f = 0;                      // seti [0, 1, 5]
addr_18:
  b = f + 1;                  // addi [5, 1, 1]
  b = b * 256;                // muli [1, 256, 1]
  b = b > e ? 1 : 0;          // gtrr [1, 4, 1]
  assert(b == 0 || b == 1);
  if (b) goto addr_23;        // addr [1, 2, 2]
  goto addr_24;               // addi [2, 1, 2]
addr_23:
  goto addr_26;               // seti [25, 1, 2]
addr_24:
  f = f + 1;                  // addi [5, 1, 5]
  goto addr_18;               // seti [17, 8, 2]
addr_26:
  e = f;                      // setr [5, 2, 4]
  goto addr_8;                // seti [7, 9, 2]
addr_28:
  f = d == a ? 1 : 0;         // eqrr [3, 0, 5]
  assert(f == 0 || f == 1);
  if (f) exit(0);             // addr [5, 2, 2]
  goto addr_6;                // seti [5, 3, 2]
  return 0;                
}
