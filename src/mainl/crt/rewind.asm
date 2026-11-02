; Original Borland DOS far-cdecl rewind: seek absolute offset zero.
; Clear the original FILE error/EOF bit only when fseek succeeds.
.8086
extrn _fseek:far
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _rewind
_rewind proc far
    push bp
    mov bp,sp
    push si
    push di
    xor ax,ax
    push ax
    push ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call _fseek
    add sp,0Ah
    or ax,ax
    jne short done
    les bx,dword ptr [bp+6]
    and word ptr es:[bx+2],0FFEFh
done:
    pop di
    pop si
    pop bp
    retf
_rewind endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
end
