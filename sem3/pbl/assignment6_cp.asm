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

%macro open 3
  rw 2, %1, %2, %3 ; filename, flags, permissions
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
  src    resb 256
  dest   resb 256
  srcfd  resq 1
  destfd resq 1
  buf    resb 512
  buflen resq 1

section .text
  global _start

_start:
  ; get src filename
  pop r8
  pop r8
  pop r8
  mov rsi, src
nextcharsrc:
  mov al, byte[r8]
  mov byte[rsi], al
  cmp al, 0
  je copiedsrc
  inc rsi
  inc r8
  jmp nextcharsrc
copiedsrc:

  ; get dest filename
  pop r8
  mov rsi, dest
nextchardest:
  mov al, byte[r8]
  mov byte[rsi], al
  cmp al, 0
  je copieddest
  inc rsi
  inc r8
  jmp nextchardest
copieddest:

  ; FIXME: add error handling
  ; open source file
  open src, 0, 0777o
  mov qword[srcfd], rax

  ; open destination file
  open dest, 0x241, 0777o ; 0x200 = O_TRUNC, 0x40 = O_CREAT, 0x1 = O_WRONLY
                          ; creat() is functionally identical to open with
                          ; O_TRUNC|O_CREAT|O_WRONLY flags
  mov qword[destfd], rax

writenext:
  ; read file
  read qword[srcfd], buf, 512
  mov qword[buflen], rax

  ; write data
  write qword[destfd], buf, qword[buflen]
  cmp qword[buflen], 512
  je writenext

  ; close file
  close qword[srcfd]
  close qword[destfd]

  exit 0
