; Complete original Japanese PC-98 cibminit video module.
; Native 8086 instructions, original segment and near interface.
; Symbolic real-mode video and cursor state, no CODE byte arrays.
.8086
extrn __wgarbage:word,__wkanji:word,__wedgectrl:word
extrn __video:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __IBM_VIDEOINT,__IBM_VIDEOINTESDI,__IBM_VIDEOINTESBP,___ibm_c0crtinit,___ibm_crtinit,___ibm_get_screen_height,___ibm_get_windowy2
video_bios_probe:
    push bp
    mov bp, sp
    push si
    push di
    jmp short video_001f
video_0007:
    les bx,dword ptr [bp + 4]
    inc word ptr [bp + 4]
    mov al, byte ptr es:[bx]
    les bx,dword ptr [bp + 8]
    inc word ptr [bp + 8]
    cmp al, byte ptr es:[bx]
    je video_001f
    xor ax, ax
    jmp short video_002b
video_001f:
    les bx,dword ptr [bp + 4]
    cmp byte ptr es:[bx], 0
    jne video_0007
    mov ax, 1
video_002b:
    pop di
    pop si
    pop bp
    ret 8
video_0031:
    push si
    push di
    mov ah, 12h
    mov bl, 10h
    call __IBM_VIDEOINT
    mov al, bl
    add al, 0f0h
    mov ah, 0
    pop di
    pop si
    ret

; Original exported PC-98 video API at CODE+67.
__IBM_VIDEOINT:
    push si
    push di
    push bp
    push ds
    push cx
    mov cx, 40h
    mov ds, cx
    pop cx
    cmp ah, 0
    je video_005d
    cmp ah, 0fh
    je video_00c2
video_0058:
    int 10h
    jmp near ptr video_00ee
video_005d:
    cmp al, 2
    je video_0079
    cmp al, 3
    je video_0079
    cmp al, 40h
    je video_0092
    cmp al, 70h
    je video_0075
    cmp al, 71h
    jne video_0058
    mov al, 12h
    jmp short video_0058
video_0075:
    mov al, 11h
    jmp short video_0058
video_0079:
    push ax
    mov ax, 1a00h
    int 10h
    cmp al, 1ah
    je video_0088
    and byte ptr ds:[0087h], 0feh
video_0088:
    mov ah, 1
    mov cx, 607h
    int 10h
    pop ax
    jmp short video_0058
video_0092:
    mov bl, 10h
    mov ah, 12h
    int 10h
    cmp bl, 10h
    je video_00ee
    mov ax, 1112h
    xor bl, bl
    int 10h
    mov ax, 1200h
    mov bl, 20h
    int 10h
    mov ax, 1a00h
    int 10h
    cmp al, 1ah
    je video_00ee
    or byte ptr ds:[0087h], 1
    mov ah, 1
    mov cx, 600h
    int 10h
    jmp short video_00ee
video_00c2:
    int 10h
    cmp al, 2
    je video_00dc
    cmp al, 3
    je video_00dc
    cmp al, 11h
    je video_00d8
    cmp al, 12h
    jne video_00ee
    mov al, 71h
    jmp short video_00ee
video_00d8:
    mov al, 70h
    jmp short video_00ee
video_00dc:
    push ax
    call video_0031
    or al, al
    pop ax
    je video_00ee
    cmp byte ptr ds:[0084h], 18h
    jbe video_00ee
    mov al, 40h
video_00ee:
    pop ds
    pop bp
    pop di
    pop si
    ret

; Original exported PC-98 video API at CODE+243.
__IBM_VIDEOINTESDI:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 0ah]
    mov cx, word ptr [bp + 4]
    les di,dword ptr [bp + 6]
    int 10h
    mov dx, es
    mov ax, di
    pop di
    pop si
    pop bp
    ret 8

; Original exported PC-98 video API at CODE+269.
__IBM_VIDEOINTESBP:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 8]
    les bp,dword ptr [bp + 4]
    int 10h
    pop di
    pop si
    pop bp
    ret 6
video_0120:
    push si
    push di
    mov si, 0ffffh
    mov ax, 6300h
    clc
    push ds
    int 21h
    xor ax, ax
    mov dx, ds
    pop ds
    jb video_0141
    cmp si, -1
    je video_0141
    mov es, dx
    cmp byte ptr es:[si], 1
    sbb ax, ax
    inc ax
video_0141:
    pop di
    pop si
    ret

; Original exported PC-98 video API at CODE+324.
___ibm_c0crtinit:
    push si
    push di
    mov ah, 0fh
    call __IBM_VIDEOINT
    push ax
    call ___ibm_crtinit
    pop cx
    mov ah, 8
    mov bh, 0
    call __IBM_VIDEOINT
    and ah, 7fh
    mov al, ah
    mov ah, 0
    mov word ptr DGROUP:__video+6, ax
    mov word ptr DGROUP:__video+4, ax
    pop di
    pop si
    ret

; Original exported PC-98 video API at CODE+359.
___ibm_crtinit:
    push bp
    mov bp, sp
    push si
    push di
    mov al, byte ptr [bp + 4]
    mov byte ptr DGROUP:__video+8, al
    mov ah, 0fh
    call __IBM_VIDEOINT
    mov byte ptr DGROUP:__video+10, ah
    cmp al, byte ptr DGROUP:__video+8
    je video_0195
    mov al, byte ptr DGROUP:__video+8
    mov ah, 0
    call __IBM_VIDEOINT
    mov ah, 0fh
    call __IBM_VIDEOINT
    mov byte ptr DGROUP:__video+8, al
    mov byte ptr DGROUP:__video+10, ah
video_0195:
    mov byte ptr DGROUP:__video+13, 0
    cmp byte ptr DGROUP:__video+8, 7
    jne video_01a6
    mov ax, 0b000h
    jmp short video_01a9
video_01a6:
    mov ax, 0b800h
video_01a9:
    mov word ptr DGROUP:__video+18, ax
    mov word ptr DGROUP:__video+16, 0
    les di,dword ptr DGROUP:__video+16
    mov ah, 0feh
    int 10h
    cmp word ptr DGROUP:__video+16, di
    jne video_01c8
    mov ax, es
    cmp word ptr DGROUP:__video+18, ax
    je video_01d5
video_01c8:
    mov word ptr DGROUP:__video+16, di
    mov word ptr DGROUP:__video+18, es
    mov byte ptr DGROUP:__video+13, 1
video_01d5:
    cmp byte ptr DGROUP:__video+13, 0
    jne video_01f6
    cmp byte ptr DGROUP:__video+8, 3
    jbe video_01f6
    cmp byte ptr DGROUP:__video+8, 7
    je video_01f6
    cmp byte ptr DGROUP:__video+8, 40h
    je video_01f6
    mov ax, 1
    jmp short video_01f8
video_01f6:
    xor ax, ax
video_01f8:
    mov byte ptr DGROUP:__video+11, al
    mov ax, 40h
    mov es, ax
    mov al, byte ptr es:[0084h]
    inc al
    mov byte ptr DGROUP:__video+9, al
    call video_0120
    mov word ptr DGROUP:__wkanji, ax
    mov word ptr DGROUP:__wgarbage, ax
    mov word ptr DGROUP:__wedgectrl, ax
    cmp byte ptr DGROUP:__video+13, 0
    jne video_0243
    cmp byte ptr DGROUP:__video+8, 7
    je video_0243
    mov ax, 0f000h
    mov dx, 0ffeah
    push ax
    push dx
    push ds
    mov ax,offset DGROUP:compaq_vendor_string
    push ax
    call video_bios_probe
    or ax, ax
    jne video_0243
    call video_0031
    or ax, ax
    jne video_0243
    mov ax, 1
    jmp short video_0245
video_0243:
    xor ax, ax
video_0245:
    mov byte ptr DGROUP:__video+12, al
    mov al, 0
    mov byte ptr DGROUP:__video+1, al
    mov byte ptr DGROUP:__video, al
    mov al, byte ptr DGROUP:__video+10
    add al, 0ffh
    mov byte ptr DGROUP:__video+2, al
    mov al, byte ptr DGROUP:__video+9
    add al, 0ffh
    mov byte ptr DGROUP:__video+3, al
    pop di
    pop si
    pop bp
    ret

; Original exported PC-98 video API at CODE+612.
___ibm_get_screen_height:
    push si
    push di
    mov ax, 40h
    mov es, ax
    mov al, byte ptr es:[0084h]
    inc al
    mov byte ptr DGROUP:__video+9, al
    mov ah, 0
    pop di
    pop si
    retf

; Original exported PC-98 video API at CODE+633.
___ibm_get_windowy2:
    push si
    push di
    push cs
    call ___ibm_get_screen_height
    dec ax
    mov dx, ax
    mov al, byte ptr DGROUP:__video+3
    mov ah, 0
    cmp ax, dx
    jle video_028f
    mov ax, dx
    jmp short video_0294
video_028f:
    mov al, byte ptr DGROUP:__video+3
    mov ah, 0
video_0294:
    pop di
    pop si
    retf
_TEXT ends
_DATA segment word public 'DATA'
compaq_vendor_string db 'COMPAQ',0
_DATA ends
end
