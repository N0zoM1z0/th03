; Borland DOS large-model byte/word clearing and memset wrapper.
; _setmem is the original far helper: (far destination, WORD count, BYTE value).
; Fill unaligned leading byte first, then use forward REP STOSW and tail byte.
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _setmem
public _memset
_setmem proc far
    push bp
    mov bp,sp
    push si
    push di
    les di,dword ptr [bp+6]
    mov cx,[bp+10]
    mov al,[bp+12]
    mov ah,al
    cld
    test di,1
    je short aligned
    jcxz short set_done
    stosb
    dec cx
aligned:
    shr cx,1
    rep stosw
    jnc short set_done
    stosb
set_done:
    pop di
    pop si
    pop bp
    retf
_setmem endp

; _memset is a separate original far cdecl wrapper, preserving its
; pointer return in DX:AX and the near CALL into the preceding far entry.
_memset proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+10]
    push word ptr [bp+12]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push cs
    call near ptr _setmem
    add sp,8
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    pop bp
    retf
_memset endp
_TEXT ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
end
