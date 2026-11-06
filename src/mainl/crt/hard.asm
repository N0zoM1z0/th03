; Original Japanese Borland hard: complete platform/runtime member.
; Preserve register ABI, interrupt behavior, storage and native relocation order.
.8086
extrn __hardresume:far
extrn __hardretn:far
extrn ___harderr:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _harderr
public _hardresume
public _hardretn
; Complete disjoint instruction chunks follow original OMF field chronology.

org 48
    call __hardretn
    pop cx
    pop di
    pop si
    pop bp
    retf

org 30
    call __hardresume
    pop cx
    pop di
    pop si
    pop bp
    retf
_hardretn label far
    push bp
    mov bp, sp
    push si
    push di
    push word ptr [bp+6]

org 11
    call ___harderr
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf
_hardresume label far
    push bp
    mov bp, sp
    push si
    push di
    push word ptr [bp+6]

org 0
_harderr label far
    push bp
    mov bp, sp
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
end
