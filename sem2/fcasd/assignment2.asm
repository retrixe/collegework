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
  num1    db 7ah ; number to print (hex representation)
  num2    db 04h ; number to add to num1 (also in hex)
  newline db 10  ; \n

section .bss
  temp resb 1

section .text
  global _start

_start:
  mov al, byte[num1]   ; copy num1 into AL register
  add al, byte[num2]   ; add num2 to AL register, eg. 0111 1000
  mov bp, 02h          ; set counter to track how many numbers have been printed
againx:
  rol al, 4            ; rotate left, ie. shift bytes to the left, eg. 1000 0111
  mov bl, al           ; copy number from AL into BL register
  and al, 0Fh          ; mask number with 0000 1111 to keep LSBs only eg. 0000 0111
  cmp al, 09h          ; compare value in AL register with 9
  jbe downx            ; if less than or equal to, jump straight to downx label
  add al, 07h          ; else add 7 to AL register to account for hex numbers
downx:
  add al, 30h          ; add 48 (0011 0000) to number due to ASCII value
  mov byte[temp], al   ; move contents of AL into temp variable
  write 1, temp, 1     ; write byte in temp to stdout
  mov al, bl           ; restore number from BL register back into AL
  dec bp               ; decrement counter in bp register
  cmp bp, 0h           ; check if counter has reached zero
  jnz againx           ; if not zero, go back to loop (againx)
  write 1, newline, 1  ; write newline then exit
  exit 0

