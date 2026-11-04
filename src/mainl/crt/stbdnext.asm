; Reconstructed Borland 16-bit large-model stbdnext.
; Original far ABI, semantic branches and normal assembler source.
.8086
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @streambuf@do_snextc$qv

@streambuf@do_snextc$qv:
    push bp
    mov bp, sp
    push si
    push di
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    les bx, dword ptr [bp + 6]
    mov bx, word ptr es:[bx]
    call dword ptr [bx + 0ch]
    pop cx
    pop cx
    cmp ax, 0ffffh
    jne label_0020
    mov ax, 0ffffh
    jmp short label_002c

label_0020:
    les bx, dword ptr [bp + 6]
    les bx, dword ptr es:[bx + 1eh]
    mov al, byte ptr es:[bx]
    mov ah, 0

label_002c:
    pop di
    pop si
    pop bp
    retf
_TEXTA ends
end
