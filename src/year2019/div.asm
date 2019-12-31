a = 0
b = 1
tmp = 2
x = 3

  in (a)
  in (b)
div:
  mulfromarray (ptr), 2, (tmp)

  addto 1, (ptr)
  setarray (tmp), (ptr)
  lt (tmp), (a), (tmp)
  jt (tmp), div
loop:
  addfromarray (ptr), (lo), (x)
  addto -1, (ptr)
  mul (b), (x), (tmp)
  lt (a), (tmp), (tmp)
  jt (tmp), skip
  mov (x), (lo)
skip:
  eq (ptr), powers, (tmp)
  jf (tmp), loop
  out (lo)

  halt

ptr:
  db powers+1
lo:
  db 1
powers:
  db 0
  db 1
