mov 10h, #74h
mov 11h, #20h ; 7420
mov 12h, #59h
mov 13h, #0E2h ; 5942
; add lower bits
mov a, 11h
add a, 13h
mov 19h, a
; add higher bits
mov a, 10h
addc a, 12h
mov 18h, a