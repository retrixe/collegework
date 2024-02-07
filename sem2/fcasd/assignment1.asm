%macro rw 4
  mov rax, %1 ; syscall ID (0 for read, 1 for write)
  mov rdi, %2 ; fd of stream to read from/write to
  mov rdx, %4 ; data length
  mov rsi, %3 ; pointer loc to read from/write to
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
  name_prompt         db  "Enter your name: "
  name_prompt_len     equ $-name_prompt
  division_prompt     db  "Enter your division: "
  division_prompt_len equ $-division_prompt
  rollno_prompt       db  "Enter your roll no: "
  rollno_prompt_len   equ $-rollno_prompt

  name_response         db  "Name: "
  name_response_len     equ $-name_response
  division_response     db  "Division: "
  division_response_len equ $-division_response
  rollno_response       db  "Roll no: "
  rollno_response_len   equ $-rollno_response

section .bss
  name     resb 16
  division resb 16
  rollno   resb 16

section .text
  global _start

_start:
  write 1, name_prompt, name_prompt_len
  read  0, name, 16
  write 1, division_prompt, division_prompt_len
  read  0, division, 16
  write 1, rollno_prompt, rollno_prompt_len
  read  0, rollno, 16

  write 1, name_response, name_response_len
  write 1, name, 16
  write 1, division_response, division_response_len
  write 1, division, 16
  write 1, rollno_response, rollno_response_len
  write 1, rollno, 16
  exit 0
