; Reconstructed Borland 16-bit large-model longtoa.
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
public __LONGTOA,__UTOA

__LONGTOA:
    push bp
    mov bp, sp
    sub sp, 22h
    push si
    push di
    push es
    les di, dword ptr [bp + 0ah]
    mov bx, word ptr [bp + 8]
    cmp bx, 24h
    ja label_0070
    cmp bl, 2
    jb label_0070
    mov ax, word ptr [bp + 0eh]
    mov cx, word ptr [bp + 10h]
    or cx, cx
    jge label_0035
    cmp byte ptr [bp + 6], 0
    je label_0035
    mov byte ptr es:[di], 2dh
    inc di
    neg cx
    neg ax
    sbb cx, 0

label_0035:
    lea si, [bp - 22h]
    jcxz label_004a

label_003a:
    xchg cx, ax
    sub dx, dx
    div bx
    xchg cx, ax
    div bx
    mov byte ptr ss:[si], dl
    inc si
    jcxz label_0052
    jmp short label_003a

label_004a:
    sub dx, dx
    div bx
    mov byte ptr ss:[si], dl
    inc si

label_0052:
    or ax, ax
    jne label_004a
    lea cx, [bp - 22h]
    neg cx
    add cx, si
    cld

label_005e:
    dec si
    mov al, byte ptr ss:[si]
    sub al, 0ah
    jae label_006a
    add al, 3ah
    jmp short label_006d

label_006a:
    add al, byte ptr [bp + 4]

label_006d:
    stosb
    loop label_005e

label_0070:
    mov al, 0
    stosb
    pop es
    mov dx, word ptr [bp + 0ch]
    mov ax, word ptr [bp + 0ah]
    pop di
    pop si
    mov sp, bp
    pop bp
    ret 0eh

__UTOA:
    push bp
    mov bp, sp
    push si
    push di
    xor ax, ax
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    push word ptr [bp + 4]
    mov ax, 0ah
    push ax
    mov al, 0
    push ax
    mov al, 61h
    push ax
    call __LONGTOA
    pop di
    pop si
    pop bp
    ret 6
_TEXT ends
end
