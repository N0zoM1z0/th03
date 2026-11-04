; Reconstructed Borland 16-bit large-model getswit.
; Original far ABI, semantic branches and normal assembler source.
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
public __getswitchar,__setswitchar

__getswitchar:
    push si
    push di
    mov ax, 3700h
    int 21h
    mov al, dl
    mov ah, 0
    pop di
    pop si
    retf

__setswitchar:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, 3701h
    mov dl, byte ptr [bp + 6]
    int 21h
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
