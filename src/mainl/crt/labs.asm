; Original Japanese Borland large-model CRT labs, source-level
; 8086 instruction semantics and far/near ABI; no target CODE array.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _labs

_labs:
    push bp
    mov bp, sp
    push si
    push di
    cmp word ptr [bp + 8], 0
    jg loc_0022
    jl loc_0013
    cmp word ptr [bp + 6], 0
    jae loc_0022
loc_0013:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    neg dx
    neg ax
    sbb dx, 0
    jmp short loc_0028
loc_0022:
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
loc_0028:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
