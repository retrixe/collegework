%macro rw 4
  mov rax, %1 ; syscall ID (0 for read, 1 for write)
  mov rdi, %2 ; fd of stream to read from/write to
  mov rsi, %3 ; pointer loc to read from/write to
  mov rdx, %4 ; data length
  syscall
%endmacro

%macro read 3
  rw 0, %1, %2, %3 ; read syscall
%endmacro

%macro write 3
  rw 1, %1, %2, %3 ; write syscall
%endmacro

%macro exit 1
  mov rax, 60 ; exit syscall
  mov rdi, %1 ; exit code
  syscall
%endmacro

section .data
  askNMsg    db  "Enter n: "
  askNMsgLen equ $-askNMsg
  askMsg     db  "Enter array number: "
  askMsgLen  equ $-askMsg
  resMsg     db  "Result of array sorting is: "
  resMsgLen  equ $-resMsg
  newline    db  10
  space      db  " "

section .bss
  array  resb 0ffh
  input  resb 3
  n      resb 1
  temp   resb 1
  cnt    resb 1
  cnt2   resb 1

section .text
  global _start

_start:
  write 1, askNMsg, askNMsgLen
  read 0, input, 03h
  mov rbp, n
  call readnumber

  mov byte[cnt], al    ; move into 'cnt' temp counter 'n'
  mov rbp, array       ; set RBP to ptr to 'array'
readnextnum:
  write 1, askMsg, askMsgLen
  read 0, input, 03h
  call readnumber      ; read number from user
  inc rbp              ; move to the next array position
  dec byte[cnt]        ; decrement the 'cnt' temp counter
  jnz readnextnum      ; if we still have positions left to fill, jump back to read the next number

  mov byte[cnt], 1     ; cnt = 1 - outer loop
outerloop:
  mov byte[cnt2], 0    ; cnt2 = 0 - inner loop
  mov rbp, array       ; put array pointer in RBP
innerloop:
  mov al, byte[rbp]    ; move byte at RBP ptr into AL
  cmp al, byte[rbp + 1]; compare AL with the byte after RBP ptr
  jbe skipexchange     ; if they are less than or equal, skip exchange
  xchg al, byte[rbp + 1];exchange AL value with RBP+1 value
  mov byte[rbp], al    ; put AL value (previously RBP+1) back in RBP
skipexchange:
  inc rbp              ; increment RBP (array pointer)
  inc byte[cnt2]       ; increment cnt2 of inner loop
  mov al, byte[n]      ; copy value of n into al
  sub al, byte[cnt]    ; subtract cnt from al
  cmp byte[cnt2], al   ; now compare cnt2 and al (n - cnt)
  jge exitinnerloop    ; exit inner loop if cnt2 >= al
  jmp innerloop        ; else re-enter inner loop
exitinnerloop:
  inc byte[cnt]        ; increment cnt of outer loop
  mov al, byte[n]      ; copy value of n into al
  cmp byte[cnt], al    ; compare cnt with al
  jge exitouterloop    ; exit outer loop if cnt >= n
  jmp outerloop        ; else re-enter outer loop
exitouterloop:

  write 1, resMsg, resMsgLen
  mov al, byte[n]      ; copy n into AL
  mov byte[cnt], al    ; copy AL into cnt
  mov rbp, array       ; copy array ptr to first element in RBP
writenextnum:
  mov al, byte[rbp]    ; copy element from current array ptr to AL
  mov byte[cnt2], 02h  ; set counter to track how many numbers have been printed
unpacknextdigit:
  rol al, 4            ; rotate left, ie. shift bytes to the left, eg. 1000 0111
  mov bl, al           ; copy number from AL into BL register
  and al, 0Fh          ; mask number with 0000 1111 to keep LSBs only eg. 0000 0111
  cmp al, 09h          ; compare value in AL register with 9
  jbe skiphex          ; if less than or equal to, jump straight to downx label
  add al, 07h          ; else add 7 to AL register to account for hex numbers
skiphex:
  add ax, 30h          ; add 48 (0011 0000) to number due to ASCII value
  mov byte[temp], al   ; move contents of AL into temp variable
  write 1, temp, 1     ; write byte in temp to stdout
  mov ax, bx           ; restore number from BX register back into AX
  dec byte[cnt2]       ; decrement counter
  jnz unpacknextdigit  ; if not zero, go back to loop (againx)
  inc rbp              ; move to next array element ptr in RBP
  write 1, space, 1    ; write space
  dec byte[cnt]        ; decrement counter of loop
  jnz writenextnum     ; if counter is not zero, jump back to write next num

  write 1, newline, 1  ; write newline then exit
  exit 0

; note this logic only works to accept numbers from 00h to FFh, beyond that, errors occur
; as the registers used throughout the code and 'n' are only 1 byte in size
; the array size is fixed at FFh and 'input' is only 2 bytes w/ 1 byte for newline
readnumber:
  mov rax, 0           ; clear RAX since we store the number in AL
  mov rsi, input       ; set RSI to ptr to 'input'
packnextdigit:
  mov cl, byte[rsi]    ; move into cl the byte at RSI ptr
  cmp cl, 0ah          ; compare it with newline
  je finishedpacking   ; if it is a newline, we've finished packing number
  cmp cl, 39h          ; compare cl with 39h
  jbe skiphexpacking   ; 30h to 39h are 0 to 9, so skip hex subtraction
  sub cl, 07h          ; else subtract 7 more since A to F are 40h to 45h
skiphexpacking:
  sub cl, 30h          ; subtract 30h to convert ASCII to number
  rol al, 4            ; rotate AL 4 bits to the left to make space for the incoming digit
  add al, cl           ; add the digit to AL
  inc rsi              ; increment source ptr in RSI
  jmp packnextdigit    ; go back to the start to pack the next digit
finishedpacking:
  mov byte[rbp], al    ; move into RBP the result in AL
  ret
