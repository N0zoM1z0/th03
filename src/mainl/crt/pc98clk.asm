; Reconstructed Borland 16-bit large-model pc98clk.
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
public _pc98clock

label_0000:
    push bp
    mov bp, sp
    push si
    push di
    mov al, byte ptr [bp + 4]
    aam 0ah
    shl ah, 1
    shl ah, 1
    shl ah, 1
    shl ah, 1
    or al, ah
    pop di
    pop si
    pop bp
    ret 2

label_001a:
    push bp
    mov bp, sp
    push si
    push di
    mov al, byte ptr [bp + 4]
    mov ah, al
    and ah, 0f0h
    shr ah, 1
    shr ah, 1
    sub al, ah
    shr ah, 1
    sub al, ah
    pop di
    pop si
    pop bp
    ret 2

_pc98clock:
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    push ds
    cld
    cmp word ptr [bp + 6], 0
    jne label_0072
    push ss
    pop es
    lea bx, [bp - 6]
    xor ah, ah
    int 1ch
    push ss
    pop ds
    les di, dword ptr [bp + 8]
    lea si, [bp - 6]
    mov cx, 4
    lodsb
    push ax
    call label_001a
    stosb
    lodsb
    mov ah, al
    shr al, cl
    and ah, 0fh
    stosw

label_006a:
    lodsb
    push ax
    call label_001a
    stosb
    loop label_006a

label_0072:
    cmp word ptr [bp + 6], 1
    jne label_009e
    push ss
    pop es
    lds si, dword ptr [bp + 8]
    lea di, [bp - 6]
    mov cx, 4
    lodsb
    push ax
    call label_0000
    stosb
    lodsw
    shl al, cl
    or al, ah
    stosb

label_008f:
    lodsb
    push ax
    call label_0000
    stosb
    loop label_008f
    lea bx, [bp - 6]
    mov ah, 1
    int 1ch

label_009e:
    pop ds
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
end
