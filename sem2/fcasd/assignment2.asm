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
  add al, byte[num2]   ; add num2 to AL register
  mov bp, 02h          ; set counter to track how many numbers have been printed
  jmp _loop            ; enter the loop
_loop:
  mov bl, byte[number] ; move value of number into BL register -> 0111 1000
; rol bl, 4            ; rotate left, shift bytes to the left -> 1000 0111
  mov dx, bp           ; copy counter into dx register, TODO: is dx appropriate?
  jmp _loop_shift      ; enter loop to shift bytes, until digit to print is last
_loop_shift:
  cmp dx, 1h           ; check if we are on the final digit to print
  je _loop_end         ; if counter is 1, stop shifting digits
  rol bl, 4            ; rotate left, shift bytes 4 to the left
  dec dx               ; decrement counter to indicate 1 digit shifted
  jmp _loop_shift      ; go back to loop start
_loop_end:
  and bl, 0Fh          ; mask number with 0000 1111 to keep LSBs -> 0000 0111
  add bl, 30h          ; add 48 (0011 0000) to number -> 0011 0111
  mov byte[temp], bl   ; move contents of bl into temp variable
  write 1, temp, 1     ; write byte in temp to stdout
  dec bp               ; decrement counter in bp register
  cmp bp, 0h           ; check if counter has reached zero
  je _finish           ; if so, jump to _finish
  jmp _loop            ; go back to loop start
_finish:
  write 1, newline, 1  ; write newline then exit
  exit 0

_start2:
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

