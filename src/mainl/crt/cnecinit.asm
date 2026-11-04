; Original Japanese NEC PC-98 cnecinit direct-video CRT module.
; Symbolic 8086 real mode BIOS, character/attribute VRAM semantics.
; Preserve literal segment frame and exported native helpers.
.8086
extrn __directvideo:word,__video:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public ___nec_c0crtinit,___nec_get_screen_height,___nec_get_windowy2,__NEC_VIDEOINT18,__NEC_VIDEOINTDC

; Original NEC video CRT public CODE+0.
___nec_c0crtinit:
    push si
    push di
    mov al, 0
    mov byte ptr __video, al
    mov byte ptr __video+1, al
    xor ax, ax
    mov es, ax
    mov al, byte ptr es:[71dh]
    mov ah, 0
    mov word ptr __video+4, ax
    mov al, byte ptr es:[714h]
    mov word ptr __video+6, ax
    mov byte ptr __video+2, 4fh
    mov byte ptr __video+10, 50h
    mov al, byte ptr es:[712h]
    inc ax
    mov byte ptr __video+9, al
    mov dx, 0a000h
    mov bx, 5051h
    mov cl, 15h
    mov al, byte ptr es:[501h]
    and al, 8
    je nec_video_0048
    mov dx, 0e000h
    mov bx, 5250h
    mov cl, 1ah
nec_video_0048:
    mov byte ptr __video+14, al
    cmp byte ptr __video+9, cl
    jb nec_video_0053
    mov bl, bh
nec_video_0053:
    mov byte ptr __video+8, bl
    mov ax, word ptr es:[632h]
    test ax, ax
    jne nec_video_0060
    xchg dx, ax
nec_video_0060:
    mov word ptr __video+16, 0
    mov word ptr __video+18, ax
    mov al, byte ptr es:[458h]
    and al, 80h
    mov byte ptr __video+15, al
    je nec_video_0083
    mov al, byte ptr es:[459h]
    and al, 0c0h
    cmp al, 80h
    jne nec_video_0083
    add byte ptr __video+8, 4
nec_video_0083:
    mov byte ptr __video+3, 0ffh
    mov word ptr DGROUP:__directvideo, 0
    pop di
    pop si
    ret

; Original NEC video CRT public CODE+145.
___nec_get_screen_height:
    push si
    push di
    xor ax, ax
    mov es, ax
    mov al, byte ptr es:[712h]
    inc al
    mov byte ptr DGROUP:__video+9, al
    mov ah, 0
    pop di
    pop si
    retf

; Original NEC video CRT public CODE+165.
___nec_get_windowy2:
    push si
    push di
    push cs
    call ___nec_get_screen_height
    dec ax
    mov dx, ax
    mov al, byte ptr DGROUP:__video+3
    mov ah, 0
    cmp ax, dx
    jle nec_video_00bb
    mov ax, dx
    jmp short nec_video_00c0
nec_video_00bb:
    mov al, byte ptr DGROUP:__video+3
    mov ah, 0
nec_video_00c0:
    pop di
    pop si
    retf

; Original NEC video CRT public CODE+195.
__NEC_VIDEOINT18:
    push si
    push di
    int 18h
    pop di
    pop si
    ret

; Original NEC video CRT public CODE+202.
__NEC_VIDEOINTDC:
    push si
    push di
    int 0dch
    pop di
    pop si
    ret
_TEXT ends
end
