; Original Japanese Borland large-model CRT toupper, source-level
; 8086 instruction semantics and far/near ABI; no target CODE array.
.8086
extrn __ctype:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _toupper

_toupper:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr [bp + 6]
    cmp dx, -1
    jne loc_0012
    mov ax, 0ffffh
    jmp short loc_002c
loc_0012:
    mov al, dl
    mov ah, 0
    mov bx, ax
    test byte ptr DGROUP:__ctype[bx+1],8
    je loc_0028
    mov al, dl
    mov ah, 0
    add ax, 0ffe0h
    jmp short loc_002c
loc_0028:
    mov al, dl
    mov ah, 0
loc_002c:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
