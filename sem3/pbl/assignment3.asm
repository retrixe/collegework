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
  askStrMsg    db  "Enter string: "
  askStrMsgLen equ $-askStrMsg
  catStrMsg    db  "Concatenated string (also to find substr): "
  catStrMsgLen equ $-catStrMsg
  spacesMsg    db  "Spaces in concatenated string: "
  spacesMsgLen equ $-spacesMsg
  wordsMsg     db  "Words in concatenated string: "
  wordsMsgLen  equ $-wordsMsg
  charsMsg     db  "Characters in concatenated string: "
  charsMsgLen  equ $-charsMsg
  substrMsg    db  "Substring occurrences: "
  substrMsgLen equ $-substrMsg
  newline db 10
  space   db " "

section .bss
  str1 resb 7Fh
  len1 resb 1
  str2 resb 7Fh
  len2 resb 1
  str3 resb 0FFh
  len3 resb 1
  temp   resb 1
  input  resb 3
  chars  resb 1
  spaces resb 1
  words  resb 1
  substr resb 1
  tempq  resq 1

section .text
  global _start

_start:
  write 1, askStrMsg, askStrMsgLen
  read 0, str1, 7Fh
  mov byte[len1], al
  dec byte[len1] ; don't copy the last character

  write 1, askStrMsg, askStrMsgLen
  read 0, str2, 7Fh
  mov byte[len2], al
  dec byte[len2] ; don't copy the last character

  mov rsi, str1
  mov rdi, str3
  mov rcx, 0
  mov cl, byte[len1]
  cld
  rep movsb

  mov rsi, str2
  ; rdi was incremented prev
  mov cl, byte[len2]
  ; cld was done before
  rep movsb

  mov al, byte[len1]
  add al, byte[len2]
  mov byte[len3], al

  write 1, catStrMsg, catStrMsgLen
  write 1, str3, 0FFh
  write 1, newline, 1

  ; =====================================
  ; count spaces, chars and words
  ; =====================================
  mov rdi, str3
  mov al, 20h
  mov bl, 0            ; bl = number of spaces
  movzx rcx, byte[len3]
countnextchar:
  ; old logic without repne:
  ; scasb -> jne notspace -> inc bl -> notspace: -> dec cl -> jnz countnextchar
  repne scasb          ; performs cmp byte[rdi], 20h until space found OR end of string
  jne exitspacesloop   ; if not a space, then naturally repne traversed entire string
  inc bl               ; but if it's a space, then increment spaces
  jmp countnextchar    ; then start loop again
exitspacesloop:
  mov byte[spaces], bl
  ; words = spaces + 1
  inc bl
  mov byte[words], bl
  dec bl
  ; chars = length - spaces
  mov al, byte[len3]
  sub al, bl
  mov byte[chars], al

  write 1, spacesMsg, spacesMsgLen
  mov al, byte[spaces]
  call displayhexnumber
  write 1, newline, 1

  write 1, wordsMsg, wordsMsgLen
  mov al, byte[words]
  call displayhexnumber
  write 1, newline, 1

  write 1, charsMsg, charsMsgLen
  mov al, byte[chars]
  call displayhexnumber
  write 1, newline, 1

  ; ======================
  ; substring
  ; ======================
  mov qword[tempq], str1;store pointer in `tempq` because RSI continuously changes
                     ; hence we must store this backup, else "aaa" with substr "aa"
                     ; returns 1 instead of 2
  mov bl, 0          ; stores count of substrings
  mov al, byte[len1]
  sub al, byte[len2]
  inc al             ; comparisons must be len1 - len2 + 1
comparesubstr:
  mov rsi, qword[tempq];put pointer in RSI
  mov rdi, str2      ; put substring pointer in RDI
  movzx rcx, byte[len2];put substring length in RCX
  repe cmpsb         ; compare entire string between RSI/RDI of RCX length
  jne substrnotmatched;if not equal, then proceed to next loop, else INC BL
  inc bl
substrnotmatched:
  inc qword[tempq]   ; increment pointer in `tempq`
  dec al
  jnz comparesubstr  ; if there are more comparisons, then go back to loop
  mov byte[substr], bl

  write 1, substrMsg, substrMsgLen
  mov al, byte[substr]
  call displayhexnumber
  write 1, newline, 1  ; write newline then exit

  exit 0

displayhexnumber:
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
  ret
