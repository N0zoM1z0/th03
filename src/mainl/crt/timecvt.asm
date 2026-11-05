; Original Borland Japanese CRT timecvt; complete 16-bit ABI leaf.
.8086
extrn __dostounix:far
extrn __unixtodos:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _dostounix
_dostounix proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call __dostounix
    add sp,8
    pop di
    pop si
    pop bp
    retf
_dostounix endp
public _unixtodos
_unixtodos proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+16]
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call __unixtodos
    add sp,12
    pop di
    pop si
    pop bp
    retf
_unixtodos endp
_TEXT ends
end
