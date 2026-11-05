; Original Borland locale-sensitive character classification: all 13 APIs.
; Full Japanese CRT `is` member. Caller supplies a 16-bit character and
; classification mask; real 8086 near helper shares original far wrappers.
.8086
extrn __pLocale:dword
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public ___isctype,_isalnum,_isascii,_isalpha,_iscntrl,_isdigit,_isgraph,_islower,_isprint,_ispunct,_isspace,_isupper,_isxdigit

___isctype:
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+6]
    cmp dx,-1
    jnz branch_0011
    xor ax,ax
    jmp short branch_002a

branch_0011:
    les bx,dword ptr DGROUP:__pLocale
    les bx,es:[bx+338]
    mov ax,dx
    and ax,255
    add bx,ax
    mov al,es:[bx+1]
    mov ah,0
    and ax,[bp+8]

branch_002a:
    pop di
    pop si
    pop bp
    retf

_isalnum:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,14
    push ax
    push word ptr [bp+6]
    push cs
    call ___isctype
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf

_isascii:
    push bp
    mov bp,sp
    push si
    push di
    cmp word ptr [bp+6],128
    jnc branch_0055
    mov ax,1
    jmp short branch_0057

branch_0055:
    xor ax,ax

branch_0057:
    pop di
    pop si
    pop bp
    retf

_isalpha:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,12
    push ax
    push word ptr [bp+6]
    push cs
    call ___isctype
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf

_iscntrl:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,32
    push ax
    push word ptr [bp+6]
    push cs
    call ___isctype
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf

_isdigit:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,2
    push ax
    push word ptr [bp+6]
    push cs
    call ___isctype
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf

_isgraph:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,94
    push ax
    push word ptr [bp+6]
    push cs
    call ___isctype
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf

_islower:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,8
    push ax
    push word ptr [bp+6]
    push cs
    call ___isctype
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf

_isprint:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,94
    push ax
    push word ptr [bp+6]
    push cs
    call ___isctype
    pop cx
    pop cx
    or ax,ax
    jnz branch_00ea
    mov ax,[bp+6]
    and ax,255
    cmp ax,32
    jnz branch_00ef

branch_00ea:
    mov ax,1
    jmp short branch_00f1

branch_00ef:
    xor ax,ax

branch_00f1:
    pop di
    pop si
    pop bp
    retf

_ispunct:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,64
    push ax
    push word ptr [bp+6]
    push cs
    call ___isctype
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf

_isspace:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,1
    push ax
    push word ptr [bp+6]
    push cs
    call ___isctype
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf

_isupper:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,4
    push ax
    push word ptr [bp+6]
    push cs
    call ___isctype
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf

_isxdigit:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,16
    push ax
    push word ptr [bp+6]
    push cs
    call ___isctype
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
