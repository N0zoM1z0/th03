; Original DOS large-model far cdecl byte comparator.
; Compares two far buffers for a WORD length without reading a zero-length
; input; returns the unsigned difference of the final compared bytes in AX.
; The target keeps DS across the far string instruction and restores it.
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _memcmp
_memcmp proc far
    push bp
    mov bp,sp
    push si
    push di
    push ds
    mov ax,[bp+14]
    mov cx,ax
    jcxz short compare_done
    lds si,dword ptr [bp+6]
    les di,dword ptr [bp+10]
    cld
    repe cmpsb
    mov al,[si-1]
    xor ah,ah
    mov cl,es:[di-1]
    xor ch,ch
compare_done:
    pop ds
    sub ax,cx
    pop di
    pop si
    pop bp
    retf
_memcmp endp
_TEXT ends
; Preserve the original BSS-before-DATA GRPDEF, including zero-size BSS
; ownership in the linked map. Declaring DGROUP late changes record order.
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
end
