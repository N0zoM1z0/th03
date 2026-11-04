; Original Japanese NEC PC-98 cnecscrn direct-video CRT module.
; Symbolic 8086 real mode BIOS, character/attribute VRAM semantics.
; Preserve literal segment frame and exported native helpers.
.8086
extrn __wclrnorm:word,__wgarbage:word,__video:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __NEC_ZAP_LINE,__NEC_MOVELINE
nec_video_0000:
    push si
    push di
    mov ax, word ptr es:[di]
    or ah, ah
    je nec_video_001c
    test ax, 8080h
    jne nec_video_001c
    cmp al, 9
    jb nec_video_0016
    cmp al, 0ch
    jb nec_video_001c
nec_video_0016:
    mov ax, 20h
    mov word ptr es:[di], ax
nec_video_001c:
    pop di
    pop si
    ret
nec_video_001f:
    push si
    push di
    mov ax, word ptr es:[di]
    or ah, ah
    je nec_video_003d
    test ax, 8080h
    je nec_video_003d
    and al, 7fh
    cmp al, 9
    jb nec_video_0037
    cmp al, 0ch
    jb nec_video_003d
nec_video_0037:
    mov ax, 20h
    mov word ptr es:[di], ax
nec_video_003d:
    pop di
    pop si
    ret

; Original NEC video CRT public CODE+64.
__NEC_ZAP_LINE:
    push bp
    mov bp, sp
    push si
    push di
    cld
    mov bl, byte ptr __video+10
    mov dx, word ptr __video+4
    cmp word ptr __wclrnorm, 0
    je nec_video_0059
    mov dx, word ptr __video+6
nec_video_0059:
    mov es, word ptr __video+18
    mov al, byte ptr [bp + 8]
    mov ah, 0
    mov di, ax
    mov al, byte ptr [bp + 4]
    mov cl, byte ptr [bp + 6]
    mov ch, 0
    sub cx, di
    inc cx
    mul bl
    add di, ax
    shl di, 1
    mov si, di
    push cx
    mov ax, 20h
    rep stosw
    pop cx
    lea di, [si + 2000h]
    xchg dx, ax
    rep stosw
    cmp word ptr __wgarbage, 0
    je nec_video_00ad
    sub di, 2000h
    cmp byte ptr [bp + 8], 0
    je nec_video_009f
    xchg di, si
    dec di
    dec di
    call nec_video_0000
    xchg di, si
nec_video_009f:
    mov al, byte ptr __video+10
    mov dl, byte ptr [bp + 6]
    inc dx
    cmp dl, al
    jae nec_video_00ad
    call nec_video_001f
nec_video_00ad:
    pop di
    pop si
    pop bp
    ret 6

; Original NEC video CRT public CODE+179.
__NEC_MOVELINE:
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    cld
    mov ax, word ptr __wgarbage
    mov word ptr [bp - 2], ax
    push ds
    mov bl, byte ptr __video+10
    mov al, byte ptr [bp + 0ah]
    mul bl
    add al, byte ptr [bp + 0ch]
    adc ah, 0
    shl ax, 1
    mov si, ax
    mov al, byte ptr [bp + 6]
    mul bl
    add al, byte ptr [bp + 8]
    adc ah, 0
    shl ax, 1
    mov di, ax
    mov ax, word ptr __video+18
    mov ds, ax
    mov es, ax
    mov cl, byte ptr [bp + 4]
    mov ch, 0
    push di
    cmp si, di
    jae nec_video_0100
    mov ax, cx
    dec ax
    shl ax, 1
    add si, ax
    add di, ax
    std
nec_video_0100:
    jcxz nec_video_010e
nec_video_0102:
    mov ax, word ptr [si + 2000h]
    mov word ptr es:[di + 2000h], ax
    movsw
    loop nec_video_0102
nec_video_010e:
    cld
    pop si
    pop ds
    cmp word ptr [bp - 2], 0
    je nec_video_0142
    mov cl, byte ptr [bp + 8]
    mov ch, 0
    jcxz nec_video_0124
    lea di, [si - 2]
    call nec_video_0000
nec_video_0124:
    mov al, byte ptr [bp + 4]
    mov ah, 0
    xchg di, ax
    add cx, di
    shl di, 1
    add di, si
    cmp cl, bl
    jae nec_video_0137
    call nec_video_001f
nec_video_0137:
    xchg di, si
    call nec_video_001f
    lea di, [si - 2]
    call nec_video_0000
nec_video_0142:
    mov ax, 1
    pop di
    pop si
    mov sp, bp
    pop bp
    ret 0ah
_TEXT ends
end
