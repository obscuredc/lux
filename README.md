# lux
it is a stack based programming language. very like assembly themed. only integers are allowed as parameters, so to build "strings" is very annoying.
## documentation
note that the documentation is not consistent with the language - by this I mean when a new command is added, it may take a while for it to be documented.
#### psh
push a value (`p0`) onto the stack
#### pop
pop top value of the stack
#### cpy
pops the top value of the stack then pushes it twice
#### tbuf_psh
pops the top value of the stack then turns it to unicode and appends it to the textbuffer
#### tbuf_out
outputs values of the textbuffer onto the screen
#### out
outputs values in the stack (turned into unicode) from first index to last until it reaches a zero.
#### add
pops 2 top values of stack, adds them, and pushes result
#### sub
pops 2 values from top of stack, then does `Topmost value - Other value` and pushes result
#### mul
pops 2 values from top of stack, then multiples and pushes result
#### div
pops 2 values from top of stack, then does `Topmost value / Other value` and pushes result
#### jmp
jumps to the command index specified (`p0`) which starts from 0 being the first *note rem counts as a command*
#### jmp_eq
jumps to the command index specified (`p0`) which starts from 0 being the first only if top two values of stack are equal *doesn't pop the top two* *note rem counts as a command*
#### jmp_ls
jumps to the command index specified (`p0`) which starts from 0 being the first only if the top value popped is less than the second value popped *doesen't pop the values, re-pushes them* *note rem counts as a command*
#### jmp_leq
jumps to the command index specified (`p0`) which starts from 0 being the first only if the top value popped is less than or equal to the second value popped *doesn't pop the values, re-pushes them* *note rem counts as a command*
#### rem
a comment. can only contain numbers in it tho
#### vstack
outputs the contents of the raw stack without turning into unicode
#### dummy
outputs the `[lux/log]: dummy`. useful for debug
#### rev
reverses the stack, making the top value the bottom one, etc