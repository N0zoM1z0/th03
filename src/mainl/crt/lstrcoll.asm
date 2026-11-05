; Entire original Borland Japanese CRT lstrcoll.
; Full locale callback through __pLocale+01A0h, far collation result.
; Full native 8086 code, original far ABI and group-frame semantics.
.8086
extrn __pLocale:dword
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __lstrcoll

__lstrcoll:
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    les bx,dword ptr DGROUP:__pLocale
    call dword ptr es:[bx+416]
    add sp,8
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
