  in (num)
#  addbp stack

loop:
  eq (cur), (next_fizz), (tmp)
  jf (tmp), chk_buzz_only
  addto 3, (next_fizz)
  eq (cur), (next_buzz), (tmp)
  jf (tmp), fizz_only
  # FizzBuzz!
  addto 5,(next_buzz)
  mov fizzbuzz,(bp+1)
  jmp next
fizz_only:
  # Fizz!
  mov fizz,(bp+1)
  jmp next
chk_buzz_only:
  eq (cur), (next_buzz), (tmp)
  jf (tmp), no_fizz_or_buzz
  addto 5,(next_buzz)
  mov buzz,(bp+1)
  jmp next
no_fizz_or_buzz:
  mov digits,(bp+1)
next:
  call show
  call inc
  addto 1, (cur)
  lt (num), (cur), (tmp)
  jf (tmp), loop

  halt


inc:
  addto 1,(digits+2)
  eq 58, (digits+2), (tmp)
  jf (tmp), incdone
  mov 48,(digits+2)
  addto 1,(digits+1)
  eq 58, (digits+1), (tmp)
  jf (tmp), incdone
  mov 48,(digits+1)
  addto 1,(digits+0)
incdone:
  jmp (bp+0)

show:
  mov (bp+1), (NEXT+1)
  eq (0), 48, (tmp)
  jf (tmp), show2
  addto 1,(bp+1)
  jmp show
show2:
  # bp+1 = addr to print
  mov (bp+1),(NEXT+1)
  out (0)
  mov (bp+1),(NEXT+1)
  eq (0), 10, (tmp)
  jt (tmp), (bp)
  addto 1,(bp+1)
  jmp show2


digits:
  db 48
  db 48
  db 49
  db 10

fizz:
  db 'F'
  db 'i'
  db 'z'
  db 'z'
  db 10

buzz:
  db 'B'
  db 'u'
  db 'z'
  db 'z'
  db 10

fizzbuzz:
  db 'F'
  db 'i'
  db 'z'
  db 'z'
  db 'B'
  db 'u'
  db 'z'
  db 'z'
  db 10

cur:
  db 1
num:
  db 0
next_fizz:
  db 3
next_buzz:
  db 5

tmp:
  db 0

stack:
