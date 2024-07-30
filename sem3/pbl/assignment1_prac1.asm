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

;%macro pack 2
;  mov rax, 0           ; clear RAX since we store the elements in AL
;  mov rsi, %2          ; set RSI to ptr to input array
;%%packnextdigit:
;  mov cl, byte[rsi]    ; move into cl the byte at RSI ptr
;  cmp cl, 0ah          ; compare it with newline
;  je %%finishedpacking ; if it is a newline, we've finished packing the number
;  cmp cl, 39h          ; compare cl with 39h
;  jbe %%skiphex        ; 30h to 39h are 0 to 9, so skip hex subtraction
;  sub cl, 07h          ; else subtract 7 more since A to F are 40h to 45h
;%%skiphex:
;  sub cl, 30h          ; subtract 30h to convert ASCII to number
;  rol al, 4            ; rotate AL 4 bits to the left to make space for the incoming digit
;  add al, cl           ; add the digit to AL
;  inc rsi              ; increment input array ptr in RSI
;  jmp %%packnextdigit  ; go back to the start to pack the next digit
;%%finishedpacking:
;  mov byte[%1], al     ; move into the number the result in AL
;%endmacro

section .data
  askMsg     db  "Enter operation (1 for add, 2 for subtract): "
  askMsgLen  equ $-askMsg
  askMsg1    db  "Enter number 1: "
  askMsg1Len equ $-askMsg1
  askMsg2    db  "Enter number 2: "
  askMsg2Len equ $-askMsg2
  resMsg     db  "Result of operation is: "
  resMsgLen  equ $-resMsg
  newline    db  10

section .bss
  input  resb 3
  op     resb 2
  n1     resb 1
  n2     resb 1
  temp   resb 1

section .text
  global _start

_start:
  write 1, askMsg, askMsgLen
  read 0, op, 02h

  ; note this logic only works to accept numbers from 00h to FFh, beyond that, errors occur
  ; as the registers used throughout the code and 'n' are only 1 byte in size
  ; the array size is fixed at FFh and 'input' is only 2 bytes w/ 1 byte for newline
  write 1, askMsg1, askMsg1Len
  read 0, input, 03h
  ; pack n1, input
  mov rax, 0           ; clear RAX since we store 'n1' in AL
  mov rsi, input       ; set RSI to ptr to 'input'
packnextdigitn1:
  mov cl, byte[rsi]    ; move into cl the byte at RSI ptr
  cmp cl, 0ah          ; compare it with newline
  je finishedpackingn1 ; if it is a newline, we've finished packing 'n1'
  cmp cl, 39h          ; compare cl with 39h
  jbe skiphexn1        ; 30h to 39h are 0 to 9, so skip hex subtraction
  sub cl, 07h          ; else, subtract 7 more since A to F are 40h to 45h
skiphexn1:
  sub cl, 30h          ; subtract 30h to convert ASCII to number
  rol al, 4            ; rotate AL 4 bits to the left to make space for the incoming digit
  add al, cl           ; add the digit to AL
  inc rsi              ; increment 'input' ptr in RSI
  jmp packnextdigitn1  ; go back to the start to pack the next digit
finishedpackingn1:
  mov byte[n1], al     ; move into 'n1' the result in AL

  write 1, askMsg2, askMsg2Len
  read 0, input, 03h
  ; pack n2, input
  mov rax, 0           ; clear RAX since we store the elements in AL
  mov rsi, input       ; set RSI to ptr to 'input'
packnextdigitn2:
  mov cl, byte[rsi]    ; move into cl the byte at RSI ptr
  cmp cl, 0ah          ; compare it with newline
  je finishedpackingn2 ; if it is a newline, we've finished packing 'n2'
  cmp cl, 39h          ; compare cl with 39h
  jbe skiphexn2        ; 30h to 39h are 0 to 9, so skip hex subtraction
  sub cl, 07h          ; else subtract 7 more since A to F are 40h to 45h
skiphexn2:
  sub cl, 30h          ; subtract 30h to convert ASCII to number
  rol al, 4            ; rotate AL 4 bits to the left to make space for the incoming digit
  add al, cl           ; add the digit to AL
  inc rsi              ; increment 'input' ptr in RSI
  jmp packnextdigitn2  ; go back to the start to pack the next digit
finishedpackingn2:
  mov byte[n2], al     ; move into 'n2' the result in AL

  write 1, resMsg, resMsgLen
  mov ax, 00h          ; set AX (AH+AL) to 0
  mov al, byte[n1]     ; move 'n1' into al
  cmp byte[op], 31h    ; compare op with '1' i.e. 31h
  jne subtract         ; if op is not '1', then skip addition and subtract
  add al, byte[n2]     ; add 'n2' into al
  jnc skipcarry        ; if no carry, skip
  inc ah               ; else increment AH
skipcarry:
  jmp skipsubtract     ; after addition, skip subtraction
subtract:
  sub al, byte[n2]     ; subtract 'n2' from al
skipsubtract:

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
