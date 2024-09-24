; sample data
mov 10h, #54h
mov 11h, #28h
mov 12h, #49h
mov 13h, #24h
mov 14h, #56h
mov 15h, #65h
mov 16h, #76h
mov 17h, #34h

; as edsim does not support extern mem
; we are using r0 instead of dptr w movx

; block transfer to extern
mov r7, #8 ; 8 bytes transfer
mov r1, #10h ; ptr to intern mem
mov r0, #0060h ; ptr to extern mem
externaltransfer:
mov a, @r1
mov @r0, a
inc r0
inc r1
djnz r7, externaltransfer

; block transfer back to intern
mov r7, #8 ; 8 bytes transfer
mov r0, #0060h ; ptr to extern mem
mov r1, #18h ; ptr to intern mem
internaltransfer:
mov a, @r0
mov @r1, a
inc r0
inc r1
djnz r7, internaltransfer