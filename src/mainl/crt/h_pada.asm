; Entire original Japanese Borland CRT h_pada member.
; Huge 16:16 pointer add and subtract: carry, 1MB segment normalization and shared far aliases.
; Natural 8086 source, complete near/far aliases and original branch behavior.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public N_PADA@,F_PADA@,PADA@,N_PSBA@,F_PSBA@,PSBA@

; Original aliases share an exact instruction address.
N_PADA@:
    pop es
    push cs
    push es

; Original aliases share an exact instruction address.
F_PADA@:
PADA@:
    mov es,dx
    xchg ax,bx
    mov dx,es:[bx+2]
    push bx
    mov bx,es:[bx]
    or cx,cx
    jnl h_pada_001e
    not ax
    not cx
    add ax,1
    adc cx,0
    jmp short h_pada_0062

h_pada_001e:
    add bx,ax
    jnc h_pada_0026
    add dx,4096

h_pada_0026:
    mov ah,cl
    mov cl,4
    shl ah,cl
    xor al,al
    add dx,ax
    mov ch,bl
    shr bx,cl
    add dx,bx
    mov al,ch
    and ax,15
    pop bx
    mov es:[bx],ax
    mov es:[bx+2],dx
    retf

; Original aliases share an exact instruction address.
N_PSBA@:
    pop es
    push cs
    push es

; Original aliases share an exact instruction address.
F_PSBA@:
PSBA@:
    mov es,dx
    xchg ax,bx
    mov dx,es:[bx+2]
    push bx
    mov bx,es:[bx]
    or cx,cx
    jnl h_pada_0062
    not ax
    not cx
    add ax,1
    adc cx,0
    jmp short h_pada_001e

h_pada_0062:
    sub bx,ax
    jnc h_pada_006a
    sub dx,4096

h_pada_006a:
    mov ah,cl
    mov cl,4
    shl ah,cl
    xor al,al
    sub dx,ax
    mov ch,bl
    shr bx,cl
    add dx,bx
    mov al,ch
    and ax,15
    pop bx
    mov es:[bx],ax
    mov es:[bx+2],dx
    retf
_TEXT ends
end
