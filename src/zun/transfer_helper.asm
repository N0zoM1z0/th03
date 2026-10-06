; Complete relocation helper; discards its own CALL return and enters 0100h.
.8086
.model tiny
.code
org 100h
start:
 rep movsb
 pop ax
 mov ax, 100h
 push ax
 retn
END start
