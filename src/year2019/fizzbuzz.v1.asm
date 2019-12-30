tmp:
  in (num)

loop:
  eq (cur), (next_fizz), (tmp)
  jf (tmp), chk_buzz_only
  addto 3, (next_fizz)
  eq (cur), (next_buzz), (tmp)
  jf (tmp), fizz_only
  # FizzBuzz!
  addto 5,(next_buzz)
  mov fizzbuzz,(target+1)
  jmp display
fizz_only:
  # Fizz!
  mov fizz,(target+1)
  jmp display
chk_buzz_only:
  eq (cur), (next_buzz), (tmp)
  jf (tmp), no_fizz_or_buzz
  addto 5,(next_buzz)
  mov buzz,(target+1)
  jmp display
no_fizz_or_buzz:
  mov digits,(target+1)
display:
target:
  eq (0), 48, (tmp)
  jf (tmp), show
  addto 1,(target+1)
  jmp display
show:
  mov (target+1),(NEXT+1)
  out (0)
  mov (target+1),(NEXT+1)
  eq (0), 10, (tmp)
  jt (tmp), inc
  addto 1,(target+1)
  jmp show
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

  addto 1, (cur)
  lt (num), (cur), (tmp)
  jf (tmp), loop

  halt



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
