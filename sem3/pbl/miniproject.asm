org 0000h
; initialise LCD in 8-bit 2 line 5x7 dots mode
mov A, #38h
acall lcdcommand
; display on, cursor blinking
mov A, #0Fh
acall lcdcommand
; register all characters
acall lcdbuildchar1 ; euro
acall lcdbuildchar2 ; dollar
acall lcdbuildchar3 ; yen
acall lcdbuildchar4 ; franc
acall lcdbuildchar5 ; rupee

; poll keypad
pollkeypad:
acall keypadread
; compare r0 with 05h
cjne r0, #05h, continue
continue:
jnc pollkeypad
; increment r0 by 1 and save it in 30h
inc r0
mov 30h, r0

; clear display
mov A, #01h
acall lcdcommand
; entry mode
mov A, #06h
acall lcdcommand

mov r0, #30h ; pointer to string
mov 31h, #00h
acall lcdsendstring

acall delay500ms
sjmp pollkeypad

lcdbuildchar1:
	mov A, #48h ; CGRAM mem location
	acall lcdcommand
	; pattern for each row
	mov A, #00h
	acall lcdsenddata
	mov A, #06h
	acall lcdsenddata
	mov A, #09h
	acall lcdsenddata
	mov A, #1Ch
	acall lcdsenddata
	mov A, #08h
	acall lcdsenddata
	mov A, #1Ch
	acall lcdsenddata
	mov A, #09h
	acall lcdsenddata
	mov A, #06h
	acall lcdsenddata
ret

lcdbuildchar2:
	mov A, #50h ; CGRAM mem location
	acall lcdcommand
	; pattern for each row
	mov A, #04h
	acall lcdsenddata
	mov A, #0Fh
	acall lcdsenddata
	mov A, #14h
	acall lcdsenddata
	mov A, #0Eh
	acall lcdsenddata
	mov A, #05h
	acall lcdsenddata
	mov A, #1Eh
	acall lcdsenddata
	mov A, #04h
	acall lcdsenddata
	mov A, #00h
	acall lcdsenddata
ret

lcdbuildchar3:
	mov A, #58h ; CGRAM mem location
	acall lcdcommand
	; pattern for each row
	mov A, #00h
	acall lcdsenddata
	mov A, #11h
	acall lcdsenddata
	mov A, #0Ah
	acall lcdsenddata
	mov A, #1Fh
	acall lcdsenddata
	mov A, #04h
	acall lcdsenddata
	mov A, #1Fh
	acall lcdsenddata
	mov A, #04h
	acall lcdsenddata
	mov A, #04h
	acall lcdsenddata
ret

lcdbuildchar4:
	mov A, #60h ; CGRAM mem location
	acall lcdcommand
	; pattern for each row
	mov A, #0Fh
	acall lcdsenddata
	mov A, #08h
	acall lcdsenddata
	mov A, #08h
	acall lcdsenddata
	mov A, #0Eh
	acall lcdsenddata
	mov A, #08h
	acall lcdsenddata
	mov A, #1Ch
	acall lcdsenddata
	mov A, #08h
	acall lcdsenddata
	mov A, #00h
	acall lcdsenddata
ret

lcdbuildchar5:
	mov A, #68h ; CGRAM mem location
	acall lcdcommand
	; pattern for each row
	mov A, #1Fh
	acall lcdsenddata
	mov A, #02h
	acall lcdsenddata
	mov A, #1Fh
	acall lcdsenddata
	mov A, #02h
	acall lcdsenddata
	mov A, #1Fh
	acall lcdsenddata
	mov A, #04h
	acall lcdsenddata
	mov A, #02h
	acall lcdsenddata
	mov A, #01h
	acall lcdsenddata
ret

lcdsendstring:
	mov A, @r0 ; set A to value in R0
	jz lcdsendstringexit ; if zero, exit
	acall lcdsenddata ; send data
	inc r0 ; increment R0 to next ptr
	sjmp lcdsendstring ; jump to fn start
lcdsendstringexit:ret

lcdcommand:
	mov p1, A ; send command to P1
	clr p3.7 ; clear RS pin
	setb  p3.6 ; toggle E pin
	clr   p3.6
	acall lcdbusy ; wait for LCD to fulfil req
ret

lcdsenddata:
	mov p1, A ; send data to P1
	setb p3.7 ; set RS pin
	setb p3.6 ; toggle E pin
	clr p3.6
	acall lcdbusy ; wait for LCD to fulfil req
ret

lcdbusy:
	mov r7, #50h ; 50 * FF clock iterations
	lcdbusyback:
	mov r6, #0FFh
	djnz r6, $
	djnz r7, lcdbusyback
ret

keypadread:
	clr f0
	mov r0, #0 ; R0 holds position of key
	; read row 3
	clr p0.3
	acall keypadcolread
	jb f0, keypadreadend
	setb p0.3
	; read row 2
	clr p0.2
	acall keypadcolread
	jb f0, keypadreadend
	setb p0.2
	; read row 1
	clr p0.1
	acall keypadcolread
	jb f0, keypadreadend
	setb p0.1
	; read row 0
	clr p0.0
	acall keypadcolread
	jb f0, keypadreadend
	setb p0.0
	; if no key was found (F0 flag), jump
	sjmp keypadread
keypadreadend: ret

keypadcolread:
	; read column 2
	jnb p0.6, keyfound
	inc r0
	; read column 1
	jnb p0.5, keyfound
	inc r0
	; read column 0
	jnb p0.4, keyfound
	inc r0
ret
keyfound:
	setb f0
ret

delay500ms:
	mov r7, #07h
	mov tmod, #10h
delayback:
	mov tl1, #0h
	mov th1, #0h
	setb tcon.6
	jnb tcon.7, $
	clr tcon.7
	clr tcon.6
	djnz r7, delayback
ret
