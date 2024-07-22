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
  arr     db 0ffh, 0ffh, 0ffh, 0ffh, 0ffh
  msg     db "Result of array addition is:"
  msgLen  db $-msg
  newline db 10

section .bss
  temp   resb 1

section .text
  global _start

_start:
  write 1, msg, msgLen ; print initial message
  mov rsi, arr         ; store array address in RSI
  mov ax, 00h          ; set AX to 0
  mov bx, 00h          ; set BX to 0
  mov cx, 5            ; set CX to 5 i.e. array elements left
up:
  mov bl, byte[rsi]    ; copy array element into BL
  add ax, bx           ; add AX to BX
  jnc skip             ; if no carry, skip
  inc ah               ; else increment AH
skip:
  inc rsi              ; increment array address to next pos
  dec cx               ; decrement counter
  jnz up               ; if counter is not zero, go to up

  mov bp, 04h          ; set counter to track how many numbers have been printed
againx:
  rol ax, 4            ; rotate left, ie. shift bytes to the left, eg. 1000 0111
  mov bx, ax           ; copy number from AX into BX register
  and ax, 0Fh          ; mask number with 0000 1111 to keep LSBs only eg. 0000 0111
  cmp ax, 09h          ; compare value in AX register with 9
  jbe downx            ; if less than or equal to, jump straight to downx label
  add ax, 07h          ; else add 7 to AX register to account for hex numbers
downx:
  add ax, 30h          ; add 48 (0011 0000) to number due to ASCII value
  mov byte[temp], al   ; move contents of AL into temp variable
  write 1, temp, 1     ; write byte in temp to stdout
  mov ax, bx           ; restore number from BX register back into AX
  dec bp               ; decrement counter in BP register
  cmp bp, 0h           ; check if counter has reached zero
  jnz againx           ; if not zero, go back to loop (againx)
  write 1, newline, 1  ; write newline then exit
  exit 0
