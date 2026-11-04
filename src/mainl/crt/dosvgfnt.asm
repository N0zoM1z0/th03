; Reconstructed Borland 16-bit large-model dosvgfnt.
; Original far ABI, semantic branches and normal assembler source.
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
public _dosvgetfont

label_0000:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    sub ax, 0de82h
    rcr ah, 1
    jb label_0013
    cmp al, 0deh
    sbb al, 5eh

label_0013:
    xor ah, 20h
    pop di
    pop si
    pop bp
    retf

_dosvgetfont:
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    mov dh, byte ptr [bp + 8]
    mov dl, byte ptr [bp + 0ah]
    mov ax, word ptr [bp + 0ch]
    cmp word ptr [bp + 6], 100h
    sbb bh, bh
    inc bh
    mov bl, 0
    push bp
    mov bp, ax
    mov ax, 5000h
    int 15h
    pop bp
    jae label_0047
    mov al, ah
    xor ah, ah
    jmp short label_0071

label_0047:
    mov word ptr [bp - 2], es
    mov word ptr [bp - 4], bx
    cmp word ptr [bp + 6], 2121h
    jb label_0066
    cmp word ptr [bp + 6], 7e7eh
    ja label_0066
    push word ptr [bp + 6]
    push cs
    call label_0000
    pop cx
    mov word ptr [bp + 6], ax

label_0066:
    mov cx, word ptr [bp + 6]
    les si, dword ptr [bp + 0eh]
    call dword ptr [bp - 4]
    xor ah, ah

label_0071:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
end
