; Entire original Japanese Borland CRT cgets input/editing routine.
; Original PC-98 double-byte/Kanji and console character behavior, backspace,
; echo, near internal erase helper and exact far buffer-length API.
.8086
extrn __wkanji:word
extrn _getch:far
extrn _putch:far
extrn __mbctype:byte
extrn __mbsbtype:far
extrn ___conio_type:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _cgets

 ; Complete original near erase/backspace/echo subroutine.
cgets_erase_character:
    push si
    push di
    mov ax,8
    push ax
    call _putch
    mov ax,32
    push ax
    call _putch
    mov ax,8
    push ax
    call _putch
    add sp,6
    pop di
    pop si
    ret

; Complete far cgets input/edit function.
_cgets:
    push bp
    mov bp,sp
    sub sp,12
    push si
    push di
    mov dx,[bp+8]
    mov ax,[bp+6]
    add ax,2
    mov [bp-4],dx
    mov [bp-6],ax
    les bx,[bp+6]
    mov al,es:[bx]
    mov ah,0
    mov [bp-8],ax
    mov word ptr [bp-10],0

cgets_004a:
    mov byte ptr [bp-11],0

cgets_004e:
    call _getch
    mov [bp-2],ax
    cmp ax,8
    jz cgets_0073
    cmp ax,13
    jnz cgets_0063
    jmp near ptr cgets_00e4

cgets_0063:
    cmp byte ptr [bp-11],0
    jnz cgets_006c
    jmp near ptr cgets_0100

cgets_006c:
    mov byte ptr [bp-11],0
    jmp near ptr cgets_013a

cgets_0073:
    cmp word ptr [bp-10],0
    jz cgets_004e
    cmp word ptr DGROUP:__wkanji,0
    jz cgets_00db
    cmp byte ptr [bp-11],0
    jnz cgets_00db
    cmp word ptr [bp-10],2
    jl cgets_00db
    mov ax,[bp-10]
    dec ax
    push ax
    push word ptr [bp-4]
    push word ptr [bp-6]
    call __mbsbtype
    add sp,6
    cmp ax,2
    jnz cgets_00db
    cmp word ptr DGROUP:___conio_type,2
    jnz cgets_00d5
    mov bx,[bp-10]
    mov es,[bp-4]
    add bx,[bp-6]
    cmp byte ptr es:[bx-2],133
    jz cgets_00db
    mov bx,[bp-10]
    add bx,[bp-6]
    cmp byte ptr es:[bx-2],134
    jnz cgets_00d5
    mov bx,[bp-10]
    add bx,[bp-6]
    cmp byte ptr es:[bx-1],159
    jc cgets_00db

cgets_00d5:
    call cgets_erase_character
    dec word ptr [bp-10]

cgets_00db:
    call cgets_erase_character
    dec word ptr [bp-10]
    jmp near ptr cgets_004a

cgets_00e4:
    les bx,[bp-6]
    add bx,[bp-10]
    mov byte ptr es:[bx],0
    les bx,[bp+6]
    mov al,[bp-10]
    mov es:[bx+1],al
    mov dx,[bp-4]
    mov ax,[bp-6]
    jmp short cgets_0155

cgets_0100:
    cmp word ptr DGROUP:__wkanji,0
    jz cgets_012e
    mov al,[bp-2]
    mov ah,0
    mov bx,ax
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz cgets_012e
    mov ax,[bp-10]
    add ax,2
    cmp ax,[bp-8]
    jl cgets_0128
    call _getch
    jmp near ptr cgets_004e

cgets_0128:
    mov byte ptr [bp-11],1
    jmp short cgets_013a

cgets_012e:
    mov ax,[bp-10]
    inc ax
    cmp ax,[bp-8]
    jl cgets_013a
    jmp near ptr cgets_004e

cgets_013a:
    push word ptr [bp-2]
    call _putch
    pop cx
    les bx,[bp-6]
    add bx,[bp-10]
    mov al,[bp-2]
    mov es:[bx],al
    inc word ptr [bp-10]
    jmp near ptr cgets_004e

cgets_0155:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_TEXT ends
end
