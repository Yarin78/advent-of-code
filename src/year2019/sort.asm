n = 0
cnt = 1
tmp = 2
ptr = 3

  in (n)
  mov 0, (cnt)
input_loop:
  eq (cnt), (n), (tmp)
  jt (tmp), input_done
  in (tmp)
  add data, (cnt), (ptr)
  setarray (tmp), (ptr)
  addto 1, (cnt)
  jmp input_loop

input_done:
  # Pointer stack pointer after input data + temp space
  add data, (n), (ptr)
  addto (n), (ptr)
  addbp (ptr)
  mov (n), (bp+1)
  mov data, (bp+2)
  call sort

  mov data, (ptr)
output_loop:
  eq (n), 0, (tmp)
  jt (tmp), output_done
  getarray (ptr), (tmp)
  out (tmp)
  addto 1, (ptr)
  addto -1, (n)
  jmp output_loop
output_done:
  halt

sort:
  params m, start, local_tmp, mupper, upper, lower, a, b

  lt [m], 2, (tmp)
  jt (tmp), sort_done

  # [mupper] is the number of elements in the first half

  mov 0, [mupper]
  mov 0, [local_tmp]
divide_loop:
  addto 1, [mupper]
  addto 2, [local_tmp]
  lt [local_tmp], [m], (tmp)
  jt (tmp), divide_loop

  # Divide
  mov [mupper], (bp+1)
  mov [start], (bp+2)
  call sort
  mov [mupper], (bp+1)
  mul -1, (bp+1), (bp+1)
  addto [m], (bp+1)
  add [start], [mupper], (bp+2)
  call sort

  # Conquer
  mov 0, [upper]
  mov [mupper], [lower]
  add data, (n), (ptr)

conquer_loop:
  lt [upper], [mupper], (tmp)
  jf (tmp), conquer_loop_done
  lt [lower], [m], (tmp)
  jf (tmp), conquer_loop_done

  add [start], [upper], (tmp)
  getarray (tmp), [a]
  add [start], [lower], (tmp)
  getarray (tmp), [b]
  lt [a], [b], (tmp)
  jf (tmp), lower_smaller
  setarray [a], (ptr)
  addto 1, [upper]
  jmp conquer_step
lower_smaller:
  setarray [b], (ptr)
  addto 1, [lower]
conquer_step:
  addto 1, (ptr)
  jmp conquer_loop
conquer_loop_done:

fill_out:
  lt [upper], [mupper], (tmp)
  jf (tmp), fill_out2
  add [start], [upper], (tmp)
  getarray (tmp), [a]
  setarray [a], (ptr)
  addto 1, [upper]
  addto 1, (ptr)
  jmp fill_out
fill_out2:
  lt [lower], [m], (tmp)
  jf (tmp), copy_back
  add [start], [lower], (tmp)
  getarray (tmp), [b]
  setarray [b], (ptr)
  addto 1, [lower]
  addto 1, (ptr)
  jmp fill_out2
copy_back:
  mov [start], [upper]
  add data, (n), [lower]

copy_back_loop:
  lt [lower], (ptr), (tmp)
  jf (tmp), copy_back_done
  getarray [lower], (tmp)
  setarray (tmp), [upper]
  addto 1, [lower]
  addto 1, [upper]
  jmp copy_back_loop
copy_back_done:

sort_done:
  ret

data:
