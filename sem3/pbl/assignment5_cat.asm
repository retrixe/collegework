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

%macro open 2
  rw 2, %1, 0, %2 ; filename, permissions
%endmacro

%macro close 1
  rw 3, %1, 0, 0
%endmacro

%macro exit 1
  mov rax, 60 ; exit syscall
  mov rdi, %1 ; exit code
  syscall
%endmacro

section .data

section .bss
  fname  resb 256
  fd     resq 1
  buf    resb 512
  buflen resq 1

section .text
  global _start

_start:
  ; get filename
  pop r8
  pop r8
  pop r8
  mov rsi, fname
nextchar:
  mov al, byte[r8]
  mov byte[rsi], al
  cmp al, 0
  je copiedfname
  inc rsi
  inc r8
  jmp nextchar
copiedfname:

  ; open file
  open fname, 0777o
  mov qword[fd], rax

writenext:
  ; read file
  read qword[fd], buf, 512
  mov qword[buflen], rax

  ; write data
  write 1, buf, qword[buflen]
  cmp qword[buflen], 512
  je writenext

  ; close file
  close qword[fd]

  exit 0
