; Reconstructed Borland 16-bit large-model stbuflow.
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
public @streambuf@underflow$qv

@streambuf@underflow$qv:
    push bp
    mov bp, sp
    push si
    push di
    les bx, dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 22h]
    cmp ax, word ptr es:[bx + 1eh]
    jbe label_001d
    les bx, dword ptr es:[bx + 1eh]
    mov al, byte ptr es:[bx]
    mov ah, 0
    jmp short label_0033

label_001d:
    les bx, dword ptr [bp + 6]
    mov dx, word ptr es:[bx + 24h]
    mov ax, word ptr es:[bx + 22h]
    mov word ptr es:[bx + 20h], dx
    mov word ptr es:[bx + 1eh], ax
    mov ax, 0ffffh

label_0033:
    pop di
    pop si
    pop bp
    retf
_TEXTA ends
end
