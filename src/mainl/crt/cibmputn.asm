; Complete original Japanese PC-98 cibmputn video module.
; Native 8086 instructions, original segment and near interface.
; Symbolic real-mode video and cursor state, no CODE byte arrays.
.8086
extrn __directvideo:word,__wgarbage:word,__video:byte
extrn __IBM_VPTR:near,__IBM_VRAM:near,__IBM_REFRESH_VRAM:near
extrn __IBM_CHECK_DBCS_TRAIL:near,__IBM_FILL_SPACE:near,__IBM_OFF_CURSOR:near
extrn __IBM_SET_CURSOR:near,__IBM_VIDEOINT:near,___col:word
extrn ___row:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __IBM_RESET_VRAM_ACCESS,__IBM_START_VRAM_ACCESS,__IBM_END_VRAM_ACCESS,__IBM_OUTPUT_CHAR

; Original exported PC-98 video API at CODE+0.
__IBM_RESET_VRAM_ACCESS:
    push si
    push di
    mov word ptr DGROUP:vram_in_use, 0
    pop di
    pop si
    ret

; Original exported PC-98 video API at CODE+11.
__IBM_START_VRAM_ACCESS:
    push si
    push di
    cmp word ptr DGROUP:vram_in_use, 0
    jne video_007b
    call __IBM_OFF_CURSOR
    mov word ptr DGROUP:saved_cursor, ax
    cmp byte ptr DGROUP:__video+11, 0
    jne video_004b
    cmp word ptr DGROUP:__directvideo, 0
    je video_004b
    mov ax, word ptr DGROUP:___col
    inc ax
    push ax
    mov ax, word ptr DGROUP:___row
    inc ax
    push ax
    call __IBM_VPTR
    mov word ptr DGROUP:vram_in_use, dx
    mov word ptr DGROUP:saved_vram_offset, ax
    mov word ptr DGROUP:saved_char_segment, dx
    mov word ptr DGROUP:saved_char_offset, ax
    mov word ptr DGROUP:pending_char_count, 0
    jmp short video_0051
video_004b:
    mov word ptr DGROUP:vram_in_use, 0ffffh
video_0051:
    cmp word ptr DGROUP:__wgarbage, 0
    je video_007b
    cmp word ptr DGROUP:___col, 0
    jbe video_007b
    push word ptr DGROUP:___col
    push word ptr DGROUP:___row
    call __IBM_CHECK_DBCS_TRAIL
    or ax, ax
    je video_007b
    mov al, byte ptr DGROUP:___col
    dec al
    push ax
    push word ptr DGROUP:___row
    call __IBM_FILL_SPACE
video_007b:
    pop di
    pop si
    ret

; Original exported PC-98 video API at CODE+126.
__IBM_END_VRAM_ACCESS:
    push si
    push di
    cmp word ptr DGROUP:vram_in_use, 0
    je video_00e4
    cmp byte ptr DGROUP:__video+11, 0
    jne video_00ab
    cmp word ptr DGROUP:__directvideo, 0
    je video_00ab
    cmp word ptr DGROUP:pending_char_count, 0
    jle video_00ab
    push word ptr DGROUP:saved_char_segment
    push word ptr DGROUP:saved_char_offset
    push word ptr DGROUP:pending_char_count
    call __IBM_REFRESH_VRAM
video_00ab:
    cmp word ptr DGROUP:__wgarbage, 0
    je video_00d7
    mov al, byte ptr DGROUP:__video+10
    mov ah, 0
    cmp ax, word ptr DGROUP:___col
    jbe video_00d7
    push word ptr DGROUP:___col
    push word ptr DGROUP:___row
    call __IBM_CHECK_DBCS_TRAIL
    or ax, ax
    je video_00d7
    push word ptr DGROUP:___col
    push word ptr DGROUP:___row
    call __IBM_FILL_SPACE
video_00d7:
    push word ptr DGROUP:saved_cursor
    call __IBM_SET_CURSOR
    mov word ptr DGROUP:vram_in_use, 0
video_00e4:
    pop di
    pop si
    ret
video_00e7:
    push bp
    mov bp, sp
    push si
    push di
    mov dl, byte ptr DGROUP:___col
    mov dh, byte ptr DGROUP:___row
    mov ah, 2
    mov bh, 0
    call __IBM_VIDEOINT
    mov bl, byte ptr DGROUP:__video+4
    mov al, byte ptr [bp + 4]
    mov ah, 9
    mov bh, 0
    mov cx, 1
    call __IBM_VIDEOINT
    inc word ptr DGROUP:___col
    pop di
    pop si
    pop bp
    ret 2

; Original exported PC-98 video API at CODE+278.
__IBM_OUTPUT_CHAR:
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    cmp byte ptr DGROUP:__video+11, 0
    jne video_0192
    cmp word ptr DGROUP:__directvideo, 0
    je video_0192
    mov al, byte ptr [bp + 4]
    mov ah, byte ptr DGROUP:__video+4
    mov word ptr [bp - 2], ax
    test byte ptr [bp + 5], 0ffh
    je video_016f
    mov ax, word ptr [bp + 4]
    mov cl, 8
    shr ax, cl
    mov ah, byte ptr DGROUP:__video+4
    mov word ptr [bp - 4], ax
    push word ptr DGROUP:vram_in_use
    push word ptr DGROUP:saved_vram_offset
    push ss
    lea ax, [bp - 4]
    push ax
    mov ax, 2
    push ax
    call __IBM_VRAM
    add word ptr DGROUP:saved_vram_offset, 4
    add word ptr DGROUP:pending_char_count, 2
    add word ptr DGROUP:___col, 2
    jmp short video_01a9
video_016f:
    push word ptr DGROUP:vram_in_use
    push word ptr DGROUP:saved_vram_offset
    push ss
    lea ax, [bp - 2]
    push ax
    mov ax, 1
    push ax
    call __IBM_VRAM
    add word ptr DGROUP:saved_vram_offset, 2
    inc word ptr DGROUP:pending_char_count
    inc word ptr DGROUP:___col
    jmp short video_01a9
video_0192:
    test byte ptr [bp + 5], 0ffh
    je video_01a3
    mov ax, word ptr [bp + 4]
    mov cl, 8
    shr ax, cl
    push ax
    call video_00e7
video_01a3:
    push word ptr [bp + 4]
    call video_00e7
video_01a9:
    pop di
    pop si
    mov sp, bp
    pop bp
    ret 2
_TEXT ends
_BSS segment word public 'BSS'
assume cs:nothing
saved_vram_offset:
    dw ?
vram_in_use:
    dw ?
saved_cursor:
    dw ?
saved_char_offset:
    dw ?
saved_char_segment:
    dw ?
pending_char_count:
    dw ?
_BSS ends
end
