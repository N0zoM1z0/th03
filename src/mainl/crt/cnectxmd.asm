; Original NEC PC-98 video text mode driver and BIOS ESC dispatcher.
; Full native 16-bit 8086 instructions, typed switch tables and data.
; Preserve CODE local fixups, video DGROUP frames and far ABI.
; No target CODE byte arrays or post-assembly object patches.
.8086
extrn __video:byte,__GOTOXY:far,___nec_get_screen_height:far
extrn __NEC_VIDEOINTDC:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public ___nec_textmode
send_nec_video_escape:
    push bp
    mov bp, sp
    push si
    push di
    jmp short nec_text_0017
nec_text_0007:
    les bx,dword ptr [bp + 4]
    mov dl, byte ptr es:[bx]
    mov cl, 10h
    mov ah, 0
    call __NEC_VIDEOINTDC
    inc word ptr [bp + 4]
nec_text_0017:
    les bx,dword ptr [bp + 4]
    cmp byte ptr es:[bx], 0
    jne nec_text_0007
    pop di
    pop si
    pop bp
    ret 4
query_nec_video_state:
    push si
    push di
    xor ax, ax
    mov es, ax
    mov al, byte ptr es:[459h]
    mov ah, 0
    and ax, 0c0h
    pop di
    pop si
    ret
change_nec_text_mode:
    push bp
    mov bp, sp
    push si
    push di
    cmp byte ptr [bp + 4], 0
    je nec_text_0049
    push ds
    mov ax,offset DGROUP:esc_nec_on
    jmp short nec_text_004d
nec_text_0049:
    push ds
    mov ax,offset DGROUP:esc_nec_off
nec_text_004d:
    push ax
    call send_nec_video_escape
    pop di
    pop si
    pop bp
    ret 2

; Original public NEC text-mode control entry.
___nec_textmode:
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    cmp word ptr [bp + 6], -1
    jne nec_text_006d
    mov al, byte ptr DGROUP:__video+8
    mov ah, 0
    mov word ptr [bp + 6], ax
nec_text_006d:
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 4], ax
    mov cx, 7
    mov bx,offset video_mode_values
nec_text_0079:
    mov ax, word ptr cs:[bx]
    cmp ax, word ptr [bp - 4]
    je nec_text_0088
    add bx, 2
    loop nec_text_0079
    jmp short nec_text_00c8
nec_text_0088:
    jmp word ptr cs:[bx + 0eh]
nec_mode_008c:
    cmp byte ptr DGROUP:__video+15, 0
    je nec_text_0098
    mov ax, 54h
    jmp short nec_text_009b
nec_text_0098:
    mov ax, 50h
nec_text_009b:
    mov word ptr [bp + 6], ax
    jmp short nec_text_00c8
nec_mode_00a0:
    mov word ptr [bp + 6], 51h
    jmp short nec_text_00c8
nec_mode_00a7:
    mov word ptr [bp + 6], 50h
    jmp short nec_text_00c8
nec_mode_00ae:
    mov word ptr [bp + 6], 52h
    jmp short nec_text_00c8
nec_mode_00b5:
    mov word ptr [bp + 6], 55h
    jmp short nec_text_00c8
nec_mode_00bc:
    mov word ptr [bp + 6], 54h
    jmp short nec_text_00c8
nec_mode_00c3:
    mov word ptr [bp + 6], 56h
nec_text_00c8:
    test byte ptr [bp + 6], 4
    je nec_text_00d8
    cmp byte ptr DGROUP:__video+15, 0
    jne nec_text_00d8
    jmp near ptr nec_mode_0160
nec_text_00d8:
    cmp byte ptr DGROUP:__video+14, 0
    je nec_text_00f7
    mov bx, word ptr [bp + 6]
    sub bx, 50h
    cmp bx, 6
    ja nec_mode_0160
    add bx, bx
    jmp word ptr cs:mode_horizontal_dispatch[bx]
nec_mode_00f1:
    mov byte ptr [bp - 1], 1fh
    jmp short nec_text_0113
nec_text_00f7:
    mov bx, word ptr [bp + 6]
    sub bx, 50h
    cmp bx, 5
    ja nec_mode_0160
    add bx, bx
    jmp word ptr cs:mode_vertical_dispatch[bx]
nec_mode_0109:
    mov byte ptr [bp - 1], 14h
    jmp short nec_text_0113
nec_mode_010f:
    mov byte ptr [bp - 1], 19h
nec_text_0113:
    call query_nec_video_state
    mov bl, al
    mov dl, byte ptr [bp + 6]
    and dl, 4
    or bl, bl
    jne nec_text_0126
    or dl, dl
    jne nec_text_012e
nec_text_0126:
    or bl, bl
    je nec_text_0132
    or dl, dl
    jne nec_text_0132
nec_text_012e:
    push dx
    call change_nec_text_mode
nec_text_0132:
    cmp byte ptr [bp - 1], 18h
    jae nec_text_013e
    push ds
    mov ax,offset DGROUP:esc_video_on
    jmp short nec_text_014e
nec_text_013e:
    cmp byte ptr [bp - 1], 19h
    jbe nec_text_014a
    push ds
    mov ax,offset DGROUP:esc_video_query
    jmp short nec_text_014e
nec_text_014a:
    push ds
    mov ax,offset DGROUP:esc_video_off
nec_text_014e:
    push ax
    call send_nec_video_escape
    push ds
    mov ax,offset DGROUP:esc_clear_display
    push ax
    call send_nec_video_escape
    mov al, byte ptr [bp + 6]
    mov byte ptr DGROUP:__video+8, al
nec_mode_0160:
    xor ax, ax
    mov es, ax
    mov ax, word ptr es:[632h]
    mov word ptr DGROUP:__video+18, ax
    cmp word ptr DGROUP:__video+18, 0
    jne nec_text_0184
    cmp byte ptr DGROUP:__video+14, 0
    je nec_text_017e
    mov ax, 0e000h
    jmp short nec_text_0181
nec_text_017e:
    mov ax, 0a000h
nec_text_0181:
    mov word ptr DGROUP:__video+18, ax
nec_text_0184:
    mov word ptr DGROUP:__video+16, 0
    mov byte ptr DGROUP:__video+10, 50h
    call ___nec_get_screen_height
    mov byte ptr DGROUP:__video+9, al
    mov byte ptr DGROUP:__video, 0
    mov byte ptr DGROUP:__video+1, 0
    mov al, byte ptr DGROUP:__video+10
    add al, 0ffh
    mov byte ptr DGROUP:__video+2, al
    mov byte ptr DGROUP:__video+3, 0ffh
    mov ax, word ptr DGROUP:__video+6
    mov word ptr DGROUP:__video+4, ax
    mov al, 0
    push ax
    push ax
    call __GOTOXY
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original two indexed near jump-dispatch tables in CODE; each word relocates.
mode_vertical_dispatch:
    dw offset nec_mode_010f ; native indexed text-video branch
    dw offset nec_mode_0109 ; native indexed text-video branch
    dw offset nec_mode_0160 ; native indexed text-video branch
    dw offset nec_mode_0160 ; native indexed text-video branch
    dw offset nec_mode_010f ; native indexed text-video branch
    dw offset nec_mode_0109 ; native indexed text-video branch
mode_horizontal_dispatch:
    dw offset nec_mode_010f ; native indexed text-video branch
    dw offset nec_mode_0160 ; native indexed text-video branch
    dw offset nec_mode_00f1 ; native indexed text-video branch
    dw offset nec_mode_0160 ; native indexed text-video branch
    dw offset nec_mode_010f ; native indexed text-video branch
    dw offset nec_mode_0160 ; native indexed text-video branch
    dw offset nec_mode_00f1 ; native indexed text-video branch

; Original video mode selector values, not executable instructions.
video_mode_values:
    dw 0 ; native NEC mode selector
    dw 1 ; native NEC mode selector
    dw 3 ; native NEC mode selector
    dw 9 ; native NEC mode selector
    dw 16 ; native NEC mode selector
    dw 17 ; native NEC mode selector
    dw 25 ; native NEC mode selector

; Original switch targets (real local CODE relocations).
video_mode_handlers:
    dw offset nec_mode_00a7 ; native NEC text mode entry
    dw offset nec_mode_00a0 ; native NEC text mode entry
    dw offset nec_mode_008c ; native NEC text mode entry
    dw offset nec_mode_00ae ; native NEC text mode entry
    dw offset nec_mode_00bc ; native NEC text mode entry
    dw offset nec_mode_00b5 ; native NEC text mode entry
    dw offset nec_mode_00c3 ; native NEC text mode entry
_TEXT ends

_DATA segment word public 'DATA'
assume cs:nothing
; Actual NEC PC-98 terminal control escape strings.
esc_nec_on:
    db 27,'[?5h',0
esc_nec_off:
    db 27,'[?5l',0
esc_video_on:
    db 27,'[>3h',0
esc_video_query:
    db 27,'[>3n',0
esc_video_off:
    db 27,'[>3l',0
esc_clear_display:
    db 27,'[2J',0
_DATA ends
end
