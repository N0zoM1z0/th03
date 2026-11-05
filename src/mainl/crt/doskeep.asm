; Original Japanese Borland CRT member: doskeep
; Calls C exit cleanup and performs DOS INT 21h AH=31h TSR.
; Full 8086 ABI and DOS carry/error behavior, no patched object bytes.
.8086
extrn __cexit:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __dos_keep

__dos_keep:
    push bp
    mov bp,sp
    push si
    push di
    call __cexit
    mov dx,[bp+8]
    mov al,[bp+6]
    mov ah,31h
    int 21h
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
