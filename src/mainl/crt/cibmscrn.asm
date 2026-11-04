; Original Japanese PC-98 direct-video screen and DBCS cursor engine.
; True 16-bit near/far BIOS and stream operation source.
; Six public APIs and full original PC-98 screen logic.
.8086
extrn _free:far,_malloc:far,__directvideo:word
extrn __wgarbage:word,__wedgectrl:word,_gettext:far
extrn _puttext:far,__mbctype:byte,__video:byte
extrn __WHEREXY:near,__IBM_VPTR:near,__IBM_VRAM:near
extrn __IBM_REFRESH_VRAM:near,__IBM_VIDEOINT:near,__IBM_VIDEOINTESBP:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __IBM_SCREENIO,__IBM_CHECK_DBCS_TRAIL,__IBM_FILL_SPACE,__IBM_OFF_CURSOR,__IBM_SET_CURSOR,__IBM_MOVELINE
pc98_char_xy_from_index:
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    mov ax, word ptr [bp + 4]
    sub ax, word ptr DGROUP:__video+16
    shr ax, 1
    mov cx, ax
    mov al, byte ptr DGROUP:__video+10
    mov ah, 0
    mov word ptr [bp - 4], ax
    push ax
    mov ax, cx
    xor dx, dx
    pop bx
    div bx
    mov bl, al
    mov ah, 0
    imul word ptr [bp - 4]
    mov dl, cl
    sub dl, al
    mov byte ptr [bp - 1], dl
    mov ah, bl
    mov al, byte ptr [bp - 1]
    pop di
    pop si
    mov sp, bp
    pop bp
    ret 4
screen_003e:
    push bp
    mov bp, sp
    push si
    push di
    les bx,dword ptr [bp + 0ah]
    mov dx, word ptr es:[bx]
    les bx,dword ptr [bp + 6]
    cmp dx, word ptr es:[bx]
    je screen_005e
    mov bh, 0
    mov ah, 2
    call __IBM_VIDEOINT
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx], dx
screen_005e:
    add dl, byte ptr [bp + 4]
    cmp dl, byte ptr DGROUP:__video+10
    jb screen_006b
    inc dh
    jmp short screen_0072
screen_006b:
    cmp dl, 0ffh
    jne screen_0074
    dec dh
screen_0072:
    mov dl, 0
screen_0074:
    les bx,dword ptr [bp + 0ah]
    mov word ptr es:[bx], dx
    pop di
    pop si
    pop bp
    ret 0ah
screen_0080:
    push bp
    mov bp, sp
    sub sp, 10h
    push si
    push di
    call __WHEREXY
    mov word ptr [bp - 0ah], ax
    mov word ptr [bp - 8], ax
    mov ax, word ptr [bp + 0ch]
    cmp ax, word ptr DGROUP:__video+18
    jne screen_009f
    mov ax, 1
    jmp short screen_00a1
screen_009f:
    xor ax, ax
screen_00a1:
    mov byte ptr [bp - 0bh], al
    or al, al
    je screen_00b4
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    call pc98_char_xy_from_index
    mov word ptr [bp - 4], ax
screen_00b4:
    mov ax, word ptr [bp + 8]
    cmp ax, word ptr DGROUP:__video+18
    jne screen_00c2
    mov ax, 1
    jmp short screen_00c4
screen_00c2:
    xor ax, ax
screen_00c4:
    mov byte ptr [bp - 0ch], al
    or al, al
    je screen_00d7
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call pc98_char_xy_from_index
    mov word ptr [bp - 6], ax
screen_00d7:
    mov word ptr [bp - 0eh], 1
    cmp byte ptr [bp - 0ch], 0
    jne screen_00e5
    jmp near ptr screen_0170
screen_00e5:
    cmp byte ptr [bp - 0bh], 0
    jne screen_00ee
    jmp near ptr screen_0170
screen_00ee:
    mov ax, word ptr [bp - 6]
    cmp ax, word ptr [bp - 4]
    jb screen_00f9
    jmp short screen_0170
    nop
screen_00f9:
    mov ax, word ptr [bp + 4]
    dec ax
    mov word ptr [bp - 10h], ax
    add word ptr [bp - 6], ax
    add word ptr [bp - 4], ax
    mov word ptr [bp - 0eh], 0ffffh
    jmp short screen_0170
screen_010d:
    cmp byte ptr [bp - 0ch], 0
    je screen_012f
    push ss
    lea ax, [bp - 6]
    push ax
    push ss
    lea ax, [bp - 8]
    push ax
    push word ptr [bp - 0eh]
    call screen_003e
    mov bh, 0
    mov ah, 8
    call __IBM_VIDEOINT
    mov word ptr [bp - 2], ax
    jmp short screen_013c
screen_012f:
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx]
    mov word ptr [bp - 2], ax
    add word ptr [bp + 6], 2
screen_013c:
    cmp byte ptr [bp - 0bh], 0
    je screen_0163
    push ss
    lea ax, [bp - 4]
    push ax
    push ss
    lea ax, [bp - 8]
    push ax
    push word ptr [bp - 0eh]
    call screen_003e
    mov ax, word ptr [bp - 2]
    mov bl, ah
    mov cx, 1
    mov bh, 0
    mov ah, 9
    call __IBM_VIDEOINT
    jmp short screen_0170
screen_0163:
    les bx,dword ptr [bp + 0ah]
    mov ax, word ptr [bp - 2]
    mov word ptr es:[bx], ax
    add word ptr [bp + 0ah], 2
screen_0170:
    mov ax, word ptr [bp + 4]
    dec word ptr [bp + 4]
    or ax, ax
    jne screen_010d
    mov dx, word ptr [bp - 0ah]
    mov bh, 0
    mov ah, 2
    call __IBM_VIDEOINT
    pop di
    pop si
    mov sp, bp
    pop bp
    ret 0ah

; Original PC-98 native screen API at CODE+396.
__IBM_SCREENIO:
    push bp
    mov bp, sp
    push si
    push di
    cmp byte ptr DGROUP:__video+11, 0
    jne screen_01bf
    cmp word ptr DGROUP:__directvideo, 0
    je screen_01bf
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    push word ptr [bp + 4]
    call __IBM_VRAM
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    push word ptr [bp + 4]
    call __IBM_REFRESH_VRAM
    jmp short screen_01d1
screen_01bf:
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    push word ptr [bp + 4]
    call screen_0080
screen_01d1:
    pop di
    pop si
    pop bp
    ret 0ah

; Original PC-98 native screen API at CODE+471.
__IBM_CHECK_DBCS_TRAIL:
    push bp
    mov bp, sp
    sub sp, 0ah
    push si
    push di
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], ax
    mov ax, 1
    push ax
    mov ax, word ptr [bp + 4]
    inc ax
    push ax
    call __IBM_VPTR
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
    mov word ptr [bp - 4], 0
    cmp word ptr [bp - 2], 0
    jle screen_0266
    push ss
    lea ax, [bp - 0ah]
    push ax
    mov ax, word ptr [bp - 2]
    add ax, ax
    mov dx, word ptr [bp - 8]
    add dx, ax
    push word ptr [bp - 6]
    push dx
    mov ax, 1
    push ax
    call __IBM_SCREENIO
    mov al, byte ptr [bp - 0ah]
    mov ah, 0
    mov bx, ax
    test byte ptr DGROUP:__mbctype[bx+1], 8
    je screen_0266
    jmp short screen_0260
screen_022c:
    dec word ptr [bp - 2]
    push ss
    lea ax, [bp - 0ah]
    push ax
    mov ax, word ptr [bp - 2]
    add ax, ax
    mov dx, word ptr [bp - 8]
    add dx, ax
    push word ptr [bp - 6]
    push dx
    mov ax, 1
    push ax
    call __IBM_SCREENIO
    mov al, byte ptr [bp - 0ah]
    mov ah, 0
    mov bx, ax
    test byte ptr DGROUP:__mbctype[bx+1], 4
    je screen_0266
    mov ax, 1
    sub ax, word ptr [bp - 4]
    mov word ptr [bp - 4], ax
screen_0260:
    cmp word ptr [bp - 2], 0
    jg screen_022c
screen_0266:
    mov ax, word ptr [bp - 4]
    pop di
    pop si
    mov sp, bp
    pop bp
    ret 4

; Original PC-98 native screen API at CODE+625.
__IBM_FILL_SPACE:
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    mov dl, byte ptr [bp + 6]
    mov dh, byte ptr [bp + 4]
    mov bh, 0
    mov cx, 1
    mov ax, 1310h
    push ax
    push ss
    lea ax, [bp - 2]
    push ax
    call __IBM_VIDEOINTESBP
    mov byte ptr [bp - 2], 20h
    mov dl, byte ptr [bp + 6]
    mov dh, byte ptr [bp + 4]
    mov bh, 0
    mov cx, 1
    mov ax, 1302h
    push ax
    push ss
    lea ax, [bp - 2]
    push ax
    call __IBM_VIDEOINTESBP
    pop di
    pop si
    mov sp, bp
    pop bp
    ret 4

; Original PC-98 native screen API at CODE+691.
__IBM_OFF_CURSOR:
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    mov ah, 3
    mov bh, 0
    call __IBM_VIDEOINT
    mov word ptr [bp - 2], cx
    cmp word ptr [bp - 2], 2000h
    je screen_02d4
    mov ah, 1
    mov cx, 2000h
    call __IBM_VIDEOINT
screen_02d4:
    mov ax, word ptr [bp - 2]
    pop di
    pop si
    mov sp, bp
    pop bp
    ret

; Original PC-98 native screen API at CODE+733.
__IBM_SET_CURSOR:
    push bp
    mov bp, sp
    push si
    push di
    mov ah, 1
    mov cx, word ptr [bp + 4]
    call __IBM_VIDEOINT
    pop di
    pop si
    pop bp
    ret 2

; Original PC-98 native screen API at CODE+752.
__IBM_MOVELINE:
    push bp
    mov bp, sp
    sub sp, 0eh
    push si
    push di
    mov al, byte ptr [bp + 0ch]
    mov ah, 0
    inc ax
    mov word ptr [bp - 8], ax
    mov al, byte ptr [bp + 0ah]
    mov ah, 0
    inc ax
    mov word ptr [bp - 0ah], ax
    mov al, byte ptr [bp + 8]
    mov ah, 0
    inc ax
    mov word ptr [bp - 0ch], ax
    mov al, byte ptr [bp + 6]
    mov ah, 0
    inc ax
    mov word ptr [bp - 0eh], ax
    cmp word ptr DGROUP:__wgarbage, 0
    jne screen_032a
    cmp word ptr DGROUP:__wedgectrl, 0
    je screen_039f
screen_032a:
    mov al, byte ptr [bp + 4]
    mov ah, 0
    add ax, ax
    push ax
    call _malloc
    pop cx
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    or ax, dx
    jne screen_0347
    xor ax, ax
    jmp short screen_03c1
    nop
screen_0347:
    call __IBM_OFF_CURSOR
    mov word ptr [bp - 6], ax
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    push word ptr [bp - 0ah]
    mov al, byte ptr [bp + 4]
    mov ah, 0
    add ax, word ptr [bp - 8]
    dec ax
    push ax
    push word ptr [bp - 0ah]
    push word ptr [bp - 8]
    call _gettext
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    push word ptr [bp - 0eh]
    mov al, byte ptr [bp + 4]
    mov ah, 0
    add ax, word ptr [bp - 0ch]
    dec ax
    push ax
    push word ptr [bp - 0eh]
    push word ptr [bp - 0ch]
    call _puttext
    push word ptr [bp - 6]
    call __IBM_SET_CURSOR
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    call _free
    add sp, 1ch
    jmp short screen_03be
screen_039f:
    push word ptr [bp - 0ch]
    push word ptr [bp - 0eh]
    call __IBM_VPTR
    push dx
    push ax
    push word ptr [bp - 8]
    push word ptr [bp - 0ah]
    call __IBM_VPTR
    push dx
    push ax
    mov al, byte ptr [bp + 4]
    mov ah, 0
    push ax
    call __IBM_SCREENIO
screen_03be:
    mov ax, 1
screen_03c1:
    pop di
    pop si
    mov sp, bp
    pop bp
    ret 0ah
_TEXT ends
end
