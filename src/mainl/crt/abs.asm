; Original Japanese Borland large-model CRT abs, source-level
; 8086 instruction semantics and far/near ABI; no target CODE array.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _abs

_abs:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    or ax, ax
    jge loc_000e
    neg ax
loc_000e:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
