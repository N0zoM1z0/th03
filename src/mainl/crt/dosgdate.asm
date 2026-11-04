; Reconstructed Borland 16-bit large-model dosgdate.
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
public __dos_getdate,__dos_gettime

__dos_getdate:
    push bp
    mov bp, sp
    push si
    push di
    mov ah, 2ah
    int 21h
    les bx, dword ptr [bp + 6]
    mov byte ptr es:[bx + 4], al
    mov byte ptr es:[bx], dl
    mov byte ptr es:[bx + 1], dh
    mov word ptr es:[bx + 2], cx
    pop di
    pop si
    pop bp
    retf

__dos_gettime:
    push bp
    mov bp, sp
    push si
    push di
    mov ah, 2ch
    int 21h
    les bx, dword ptr [bp + 6]
    mov byte ptr es:[bx], ch
    mov byte ptr es:[bx + 1], cl
    mov byte ptr es:[bx + 2], dh
    mov byte ptr es:[bx + 3], dl
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
