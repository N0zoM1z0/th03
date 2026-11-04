; Original Japanese PC-98 DOS console native counted output engine.
; Saves screen cursor, preserves window flags and double-byte Kanji.
; This is typed 8086 code, not original machine byte initializer.
.8086
extrn __wkanji:word,__wnewline:word,__wscroll:word,__video:byte
extrn __RESET_VRAM_ACCESS:near,__START_VRAM_ACCESS:near
extrn __END_VRAM_ACCESS:near,__OUTPUT_CHAR:near,__SCROLL:near
extrn __GOTOXY:far,__WHEREXY:near,__cputbell:far
extrn ___get_windowy2:far,___conio_type:word,__mbctype:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __CPUTN
scroll_at_window_bottom:
    push si
    push di
    call __END_VRAM_ACCESS
    mov al, 6
    push ax
    push word ptr DGROUP:__video
    push word ptr DGROUP:__video+1
    push word ptr DGROUP:__video+2
    call ___get_windowy2
    push ax
    mov al, 1
    push ax
    call __SCROLL
    dec word ptr DGROUP:___row
    pop di
    pop si
    ret
advance_console_line:
    push si
    push di
    call __END_VRAM_ACCESS
    mov al, byte ptr DGROUP:__video
    mov ah, 0
    mov word ptr DGROUP:___col, ax
    mov ax, word ptr DGROUP:__wscroll
    add word ptr DGROUP:___row, ax
    call ___get_windowy2
    cmp ax, word ptr DGROUP:___row
    jae loc_0049
    call scroll_at_window_bottom
loc_0049:
    pop di
    pop si
    ret
put_console_character:
    push bp
    mov bp, sp
    push si
    push di
    mov bx, word ptr [bp + 4]
    sub bx, 7
    cmp bx, 6
    jbe loc_005f
    jmp near ptr loc_00eb
loc_005f:
    add bx, bx
    jmp word ptr cs:[bx+output_char_dispatch]
loc_0066:
    call __END_VRAM_ACCESS
    push word ptr DGROUP:___col
    push word ptr DGROUP:___row
    call __GOTOXY
    call __cputbell
    call __WHEREXY
    mov ah, 0
    mov word ptr DGROUP:___col, ax
    call __WHEREXY
    mov cl, 8
    shr ax, cl
    mov ah, 0
    mov word ptr DGROUP:___row, ax
    call __RESET_VRAM_ACCESS
    jmp near ptr loc_0192
loc_0095:
    call __END_VRAM_ACCESS
loc_0098:
    mov al, byte ptr DGROUP:__video
    mov ah, 0
    mov word ptr DGROUP:___col, ax
    jmp near ptr loc_0192
loc_00a3:
    call __END_VRAM_ACCESS
    inc word ptr DGROUP:___row
    cmp word ptr DGROUP:__wnewline, 0
    je loc_00b4
    jmp near ptr loc_0192
loc_00b4:
    jmp short loc_0098
loc_00b6:
    call __END_VRAM_ACCESS
    mov al, byte ptr DGROUP:__video
    mov ah, 0
    cmp ax, word ptr DGROUP:___col
    jb loc_00c7
    jmp near ptr loc_0192
loc_00c7:
    dec word ptr DGROUP:___col
    jmp near ptr loc_0192
loc_00ce:
    call __END_VRAM_ACCESS
    mov al, byte ptr DGROUP:__video
    mov ah, 0
    mov dx, word ptr DGROUP:___col
    sub dx, ax
    and dx, 7
    mov ax, 8
    sub ax, dx
    add word ptr DGROUP:___col, ax
    jmp near ptr loc_0192
loc_00eb:
    cmp word ptr DGROUP:__wkanji, 0
    jne loc_00f5
    jmp near ptr loc_0189
loc_00f5:
    cmp word ptr DGROUP:saved_kanji_byte, 0
    je loc_0173
    cmp word ptr DGROUP:___conio_type, 2
    jne loc_012f
    cmp word ptr DGROUP:saved_kanji_byte, 85h
    je loc_011a
    cmp word ptr DGROUP:saved_kanji_byte, 86h
    jne loc_012f
    cmp word ptr [bp + 4], 9fh
    jge loc_012f
loc_011a:
    mov ax, word ptr DGROUP:saved_kanji_byte
    mov cl, 8
    shl ax, cl
    mov dx, word ptr [bp + 4]
    and dx, 0ffh
    add ax, dx
    mov word ptr [bp + 4], ax
    jmp short loc_0162
loc_012f:
    mov al, byte ptr DGROUP:__video+2
    mov ah, 0
    mov dl, byte ptr DGROUP:__video
    mov dh, 0
    sub ax, dx
    cmp ax, 1
    jl loc_016b
    mov ax, word ptr DGROUP:saved_kanji_byte
    mov cl, 8
    shl ax, cl
    mov dx, word ptr [bp + 4]
    and dx, 0ffh
    add ax, dx
    mov word ptr [bp + 4], ax
    mov al, byte ptr DGROUP:__video+2
    mov ah, 0
    cmp ax, word ptr DGROUP:___col
    ja loc_0162
    call advance_console_line
loc_0162:
    call __START_VRAM_ACCESS
    push word ptr [bp + 4]
    call __OUTPUT_CHAR
loc_016b:
    mov word ptr DGROUP:saved_kanji_byte, 0
    jmp short loc_0192
loc_0173:
    mov al, byte ptr [bp + 4]
    mov ah, 0
    mov bx, ax
    test byte ptr DGROUP:__mbctype[bx+1], 4
    je loc_0189
    mov ax, word ptr [bp + 4]
    mov word ptr DGROUP:saved_kanji_byte, ax
    jmp short loc_0192
loc_0189:
    call __START_VRAM_ACCESS
    push word ptr [bp + 4]
    call __OUTPUT_CHAR
loc_0192:
    mov al, byte ptr DGROUP:__video+2
    mov ah, 0
    cmp ax, word ptr DGROUP:___col
    jae loc_01a0
    call advance_console_line
loc_01a0:
    call ___get_windowy2
    cmp ax, word ptr DGROUP:___row
    jae loc_01ae
    call scroll_at_window_bottom
loc_01ae:
    pop di
    pop si
    pop bp
    ret 2

; Original seven-entry handler dispatch for special output.
output_char_dispatch label word
    dw loc_0066
    dw loc_00b6
    dw loc_00ce
    dw loc_00a3
    dw loc_00eb
    dw loc_00eb
    dw loc_0095

; Original public near counted output callback at CODE+450.
__CPUTN:
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    mov word ptr [bp - 2], 0
    call __WHEREXY
    mov dx, ax
    mov al, dl
    mov ah, 0
    mov word ptr DGROUP:___col, ax
    mov ax, dx
    mov cl, 8
    shr ax, cl
    mov ah, 0
    mov word ptr DGROUP:___row, ax
    call __RESET_VRAM_ACCESS
    jmp short loc_01fd
loc_01eb:
    les bx,dword ptr [bp + 0ah]
    mov al, byte ptr es:[bx]
    mov ah, 0
    mov word ptr [bp - 2], ax
    inc word ptr [bp + 0ah]
    push ax
    call put_console_character
loc_01fd:
    mov ax, word ptr [bp + 8]
    dec word ptr [bp + 8]
    or ax, ax
    jne loc_01eb
    call __END_VRAM_ACCESS
    push word ptr DGROUP:___col
    push word ptr DGROUP:___row
    call __GOTOXY
    mov ax, word ptr [bp - 2]
    pop di
    pop si
    mov sp, bp
    pop bp
    ret 0ah
_TEXT ends
_DATA segment word public 'DATA'
saved_kanji_byte dw 0
_DATA ends
_BSS segment word public 'BSS'
public ___col,___row
___col dw ?
___row dw ?
_BSS ends
end
