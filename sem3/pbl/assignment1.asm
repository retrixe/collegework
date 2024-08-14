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
  resMsg     db  "Result of array addition is: "
  resMsgLen  equ $-resMsg
  newline    db  10

section .bss
  array  resb 0ffh
  input  resb 3
  n      resb 1
  temp   resb 1
  cnt    resb 1 ; we could replace this with 'temp'

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
  call readnumber
  inc rbp              ; move to the next array position
  dec byte[cnt]        ; decrement the 'cnt' temp counter
  jnz readnextnum      ; if we still have positions left to fill, jump back to read the next number

  write 1, resMsg, resMsgLen
  mov rsi, array       ; store array address in RSI
  mov ax, 00h          ; set AX (AH+AL) to 0
  mov bx, 00h          ; set BX (BH+BL) to 0
  mov cl, byte[n]      ; set CX to how many array elements are accepted
addnextel:
  mov bl, byte[rsi]    ; copy array element into BL
  add al, bl           ; add AL to BL
  jnc skipcarry        ; if no carry, skip
  inc ah               ; else increment AH
skipcarry:
  inc rsi              ; increment array address to next pos
  dec cl               ; decrement counter
  jnz addnextel        ; if counter is not zero, go to up

  mov bp, 04h          ; set counter to track how many numbers have been printed
unpacknextdigit:
  rol ax, 4            ; rotate left, ie. shift bytes to the left, eg. 1000 0111
  mov bx, ax           ; copy number from AX into BX register
  and ax, 0Fh          ; mask number with 0000 1111 to keep LSBs only eg. 0000 0111
  cmp ax, 09h          ; compare value in AX register with 9
  jbe skiphex          ; if less than or equal to, jump straight to downx label
  add ax, 07h          ; else add 7 to AX register to account for hex numbers
skiphex:
  add ax, 30h          ; add 48 (0011 0000) to number due to ASCII value
  mov byte[temp], al   ; move contents of AL into temp variable
  write 1, temp, 1     ; write byte in temp to stdout
  mov ax, bx           ; restore number from BX register back into AX
  dec bp               ; decrement counter in BP register
  cmp bp, 0h           ; check if counter has reached zero
  jnz unpacknextdigit  ; if not zero, go back to loop (againx)
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
