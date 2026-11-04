; Reconstructed Borland 16-bit large-model stsetf2.
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
public @ios@setf$qll

@ios@setf$qll:
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    les bx, dword ptr [bp + 6]
    add bx, 10h
    mov word ptr [bp - 6], bx
    mov dx, word ptr es:[bx + 2]
    mov ax, word ptr es:[bx]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    mov dx, word ptr [bp + 10h]
    mov ax, word ptr [bp + 0eh]
    not ax
    not dx
    and word ptr es:[bx], ax
    and word ptr es:[bx + 2], dx
    mov dx, word ptr [bp + 0ch]
    mov ax, word ptr [bp + 0ah]
    and ax, word ptr [bp + 0eh]
    and dx, word ptr [bp + 10h]
    mov bx, word ptr [bp + 6]
    or word ptr es:[bx + 10h], ax
    or word ptr es:[bx + 12h], dx
    test byte ptr es:[bx + 10h], 1
    je label_0055
    or word ptr es:[bx + 0ch], 100h
    jmp short label_005e

label_0055:
    les bx, dword ptr [bp + 6]
    and word ptr es:[bx + 0ch], 0feffh

label_005e:
    mov dx, word ptr [bp - 2]
    mov ax, word ptr [bp - 4]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXTA ends
end
