a = 0
b = 1
tmp = 2
x = 3

  in (a)
  in (b)
div:
  mov (ptr), (NEXT+1)
  mul (0), 2, (tmp)
  addto 1, (ptr)
  mov (ptr), (NEXT+3)
  mov (tmp), (0)
  lt (tmp), (a), (tmp)
  jt (tmp), div
loop:
  mov (ptr), (NEXT+1)
  add (0), (lo), (x)
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
