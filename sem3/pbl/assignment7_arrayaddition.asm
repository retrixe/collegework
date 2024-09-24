mov 10h, #0FFh
mov 11h, #0FFh
mov 12h, #0FFh
mov 13h, #0FFh
mov 14h, #0FFh
; loop through array
mov r0, #5
mov r1, #10h
mov a, #0h
mov b, #0h
up:
add a, @r1
xch a, b ; add upper 8 bit carry to B
addc a, #0h
xch a, b
inc r1
djnz r0, up
; save result
mov 18h, b
mov 19h, a
