; Entire original Japanese Borland CRT h_pina member.
; Huge 16:16 pointer increment/decrement with near-to-far stubs and ES memory updates.
; Natural 8086 source, complete near/far aliases and original branch behavior.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public N_PINA@,F_PINA@,PINA@,N_PDEA@,F_PDEA@,PDEA@

; Original aliases share an exact instruction address.
N_PINA@:
    pop cx
    push cs
    push cx

; Original aliases share an exact instruction address.
F_PINA@:
PINA@:
    mov cl,4
    add ax,es:[bx]
    mov dx,ax
    jc h_pina_001d
    shr dx,cl
    add dx,es:[bx+2]
    and ax,15
    xchg ax,es:[bx]
    xchg dx,es:[bx+2]
    retf

h_pina_001d:
    shr dx,cl
    add dx,es:[bx+2]
    add dx,4096
    and ax,15
    xchg ax,es:[bx]
    xchg dx,es:[bx+2]
    retf

; Original aliases share an exact instruction address.
N_PDEA@:
    pop cx
    push cs
    push cx

; Original aliases share an exact instruction address.
F_PDEA@:
PDEA@:
    mov cl,4
    mov dx,es:[bx]
    sub dx,ax
    mov ax,dx
    jc h_pina_0051
    shr dx,cl
    add dx,es:[bx+2]
    and ax,15
    xchg ax,es:[bx]
    xchg dx,es:[bx+2]
    retf

h_pina_0051:
    shr dx,cl
    add dx,es:[bx+2]
    sub dx,4096
    and ax,15
    xchg ax,es:[bx]
    xchg dx,es:[bx+2]
    retf
_TEXT ends
end
