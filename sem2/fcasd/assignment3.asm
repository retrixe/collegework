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
  num1  db 7ah ; number to print (stored in hex representation)
  num2  db 04h ; number to print (stored in hex representation)
  newline db 10  ; \n

section .bss
  temp resb 1

section .text
  global _start

_start:
  mov al, byte[num1]
  add al, byte[num2]
  mov bp, 2
againx:
  rol al, 4
  mov bl, al
  and al, 0Fh
  cmp al, 09h
  jbe downx
  add al, 07h
downx:
  add al, 30h
  mov byte[temp], al
  write 1, temp, 1
  mov al, bl
  dec bp
  cmp bp, 00
  jnz againx
  syscall
  exit 0
