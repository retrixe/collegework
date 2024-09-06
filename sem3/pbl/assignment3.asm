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
  gdtBaseMsg db "Global descriptor table base address: "
  gdtBaseMsgLen equ $-gdtBaseMsg
  gdtLimitMsg db "Global descriptor table limit: "
  gdtLimitMsgLen equ $-gdtLimitMsg
  ldtMsg db "Local descriptor table selector: "
  ldtMsgLen equ $-ldtMsg
  idtBaseMsg db "Interrupt descriptor table base address: "
  idtBaseMsgLen equ $-idtBaseMsg
  idtLimitMsg db "Interrupt descriptor table limit: "
  idtLimitMsgLen equ $-idtLimitMsg
  trMsg db "Task register selector: "
  trMsgLen equ $-trMsg
  mswMsg db "Machine status word: "
  mswMsgLen equ $-mswMsg
  newline db 10
  space db " "

section .bss
  temp resb 1
  gdtbase resq 1
  gdtlimit resw 1
  ldt resw 1
  idtbase resq 1
  idtlimit resw 1
  trcontent resw 1
  mswcontent resw 1

section .text
  global _start

_start:
  mov rsi, gdtbase
  sgdt [rsi]
  write 1, gdtBaseMsg, gdtBaseMsgLen
  mov rax, qword[gdtbase]
  call display64bithexnumber
  write 1, newline, 1
  write 1, gdtLimitMsg, gdtLimitMsgLen
  movzx rax, word[gdtlimit]
  call display16bithexnumber
  write 1, newline, 1
  write 1, newline, 1

  mov rsi, ldt
  sldt [rsi]
  write 1, ldtMsg, ldtMsgLen
  movzx rax, word[ldt]
  call display16bithexnumber
  write 1, newline, 1
  write 1, newline, 1

  mov rsi, idtbase
  sidt [rsi]
  write 1, idtBaseMsg, idtBaseMsgLen
  mov rax, qword[idtbase]
  call display64bithexnumber
  write 1, newline, 1
  write 1, idtLimitMsg, idtLimitMsgLen
  movzx rax, word[idtlimit]
  call display16bithexnumber
  write 1, newline, 1
  write 1, newline, 1

  mov rsi, trcontent
  str [rsi]
  write 1, trMsg, trMsgLen
  movzx rax, word[trcontent]
  call display16bithexnumber
  write 1, newline, 1
  write 1, newline, 1

  mov rsi, mswcontent
  smsw [rsi]
  write 1, mswMsg, mswMsgLen
  movzx rax, word[mswcontent]
  call display16bithexnumber
  write 1, newline, 1

  exit 0

display64bithexnumber:
  mov bp, 16           ; set counter to track how many numbers have been printed
unpacknextdigit64:
  rol rax, 4           ; rotate left, ie. shift bytes to the left, eg. 1000 0111
  mov rbx, rax         ; copy number from AX into BX register
  and rax, 0Fh         ; mask number with 0000 1111 to keep LSBs only eg. 0000 0111
  cmp rax, 09h         ; compare value in AX register with 9
  jbe skiphex64        ; if less than or equal to, jump straight to downx label
  add rax, 07h         ; else add 7 to AX register to account for hex numbers
skiphex64:
  add rax, 30h         ; add 48 (0011 0000) to number due to ASCII value
  mov byte[temp], al   ; move contents of AL into temp variable
  write 1, temp, 1     ; write byte in temp to stdout
  mov rax, rbx         ; restore number from BX register back into AX
  dec bp               ; decrement counter in BP register
  cmp bp, 0h           ; check if counter has reached zero
  jnz unpacknextdigit64; if not zero, go back to loop (againx)
  ret

display16bithexnumber:
  mov bp, 04h          ; set counter to track how many numbers have been printed
unpacknextdigit16:
  rol ax, 4            ; rotate left, ie. shift bytes to the left, eg. 1000 0111
  mov bx, ax           ; copy number from AX into BX register
  and ax, 0Fh          ; mask number with 0000 1111 to keep LSBs only eg. 0000 0111
  cmp ax, 09h          ; compare value in AX register with 9
  jbe skiphex16        ; if less than or equal to, jump straight to downx label
  add ax, 07h          ; else add 7 to AX register to account for hex numbers
skiphex16:
  add ax, 30h          ; add 48 (0011 0000) to number due to ASCII value
  mov byte[temp], al   ; move contents of AL into temp variable
  write 1, temp, 1     ; write byte in temp to stdout
  mov ax, bx           ; restore number from BX register back into AX
  dec bp               ; decrement counter in BP register
  cmp bp, 0h           ; check if counter has reached zero
  jnz unpacknextdigit16; if not zero, go back to loop (againx)
  ret
