; Original DOS Borland far-cdecl strftime: native 8086 format dispatcher.
; 1168 real executable 8086 CODE bytes plus two immutable 22-WORD CODE
; lookup tables of format characters and target offset labels (88 bytes).
; Real initialized DATA contains seven source-owned C format fragments.
; Genuine far string helpers and near __UTOA import with original ABI.
; Disjoint native assembly blocks restore original OMF FIXUPP order;
; no embedded executable CODE DB arrays, binary patches or filler.
.8086
extrn __UTOA:near
extrn __tzname:word
extrn _strcat:far
extrn _strcpy:far
extrn _strlen:far
extrn _strncpy:far
extrn _SWeekday:word
extrn _LWeekday:word
extrn _SMonth:word
extrn _LMonth:word
extrn _AmPm:word
extrn _atime:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
fmt_double_zero db '00',0
fmt_space_one db ' ',0
fmt_space_two db ' ',0
fmt_comma_space db ', ',0
fmt_colon_zero_one db ':0',0
fmt_colon_zero_two db ':0',0
fmt_literal_percent db '%',0
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
public _strftime
; 1168 typed executable CODE bytes + 44 static format WORDs +
; 44 symbolic switch WORDs. All CODE positions are original.
; BCC ordered FIXUPP writer sequence: low body, table, high body.
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 03F6h
    mov ax,word ptr DGROUP:[bx+__tzname]
    jmp near ptr strftime_at_00bf
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 03F2h
    mov dx,word ptr DGROUP:[bx+__tzname+2]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 038Eh
    call _strlen
    pop cx
    pop cx
    lea dx, [bp-02eh]
    add ax, dx
    push ax
    les bx, dword ptr [bp+010h]
    cmp word ptr es:[bx], 9
    jle short strftime_at_03a9
    mov ax, 1
    jmp short strftime_at_03ab
strftime_at_03a9:
    xor ax, ax
strftime_at_03ab:
    pop dx
    sub dx, ax
    jmp near ptr strftime_at_0166
fmt_y_03b1:
    les bx, dword ptr [bp+010h]
    mov ax, word ptr es:[bx+0ah]
    add ax, 076ch
    mov bx, 064h
    cwd
    idiv bx
    mov word ptr [bp-6], dx
    push dx
    cmp word ptr [bp-6], 0ah
    jge short strftime_at_03d0
strftime_at_03cb:
    mov ax, 1
    jmp short strftime_at_03d2
strftime_at_03d0:
    xor ax, ax
strftime_at_03d2:
    jmp near ptr strftime_at_02fe
fmt_Y_03d5:
    les bx, dword ptr [bp+010h]
    mov ax, word ptr es:[bx+0ah]
    add ax, 076ch
    push ax
strftime_at_03e0:
    push ss
    lea ax, [bp-02eh]
    jmp near ptr strftime_at_0304
fmt_Z_03e7:
    les bx, dword ptr [bp+010h]
    mov bx, word ptr es:[bx+010h]
    mov cl, 2
    shl bx, cl
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 037Bh
    call _strcat
    add sp, 8
    les bx, dword ptr [bp+010h]
    push word ptr es:[bx]
    push ss
    lea ax, [bp-02eh]
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0372h
    mov ax,offset DGROUP:fmt_colon_zero_two
    push ax
    push ss
    lea ax, [bp-02eh]
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 036Eh
    call __UTOA
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 034Bh
    call _strlen
    pop cx
    pop cx
    lea dx, [bp-02eh]
    add ax, dx
    push ax
    les bx, dword ptr [bp+010h]
    cmp word ptr es:[bx+2], 9
    jle short strftime_at_0367
    mov ax, 1
    jmp short strftime_at_0369
strftime_at_0367:
    xor ax, ax
strftime_at_0369:
    pop dx
    sub dx, ax
    push ss
    push dx
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0337h
    call _strcat
    add sp, 8
    les bx, dword ptr [bp+010h]
    push word ptr es:[bx+2]
    push ss
    lea ax, [bp-02eh]
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 032Eh
    mov ax,offset DGROUP:fmt_colon_zero_one
    push ax
    push ss
    lea ax, [bp-02eh]
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 032Ah
    call __UTOA
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0305h
strftime_at_0305:
    call __UTOA
    jmp near ptr strftime_at_0405
fmt_X_030b:
    les bx, dword ptr [bp+010h]
    mov ax, word ptr es:[bx+4]
    mov word ptr [bp-014h], ax
    push ax
    cmp word ptr [bp-014h], 0ah
    jge short strftime_at_0321
    mov ax, 1
    jmp short strftime_at_0323
strftime_at_0321:
    xor ax, ax
strftime_at_0323:
    lea dx, [bp-02eh]
    add ax, dx
    push ss
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 02F7h
    call _strlen
    pop cx
    pop cx
strftime_at_02fe:
    lea dx, [bp-02eh]
    add ax, dx
    push ss
strftime_at_0304:
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 02DFh
    call _strcat
    add sp, 8
    les bx, dword ptr [bp+010h]
    mov ax, word ptr es:[bx+0ah]
    add ax, 076ch
    push ax
    push ss
    lea ax, [bp-02eh]
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 02D6h
    mov ax,offset DGROUP:fmt_comma_space
    push ax
    push ss
    lea ax, [bp-02eh]
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 02D2h
    call __UTOA
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 02C4h
    call _strlen
    pop cx
    pop cx
    lea dx, [bp-02eh]
    add ax, dx
    push ss
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 02B0h
    call _strcat
    add sp, 020h
    les bx, dword ptr [bp+010h]
    push word ptr es:[bx+6]
    push ss
    lea ax, [bp-02eh]
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 02A7h
    mov ax,offset DGROUP:fmt_space_two
    push ax
    push ss
    lea ax, [bp-02eh]
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 02A1h
    call _strcat
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0298h
    push word ptr DGROUP:[bx+_SMonth]
    push ss
    lea ax, [bp-02eh]
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0294h
    push word ptr DGROUP:[bx+_SMonth+2]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0284h
    call _strcat
    les bx, dword ptr [bp+010h]
    mov bx, word ptr es:[bx+8]
    mov cl, 2
    shl bx, cl
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 027Bh
    mov ax,offset DGROUP:fmt_space_one
    push ax
    push ss
    lea ax, [bp-02eh]
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0275h
    call _strcpy
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 026Ch
    push word ptr DGROUP:[bx+_SWeekday]
    push ss
    lea ax, [bp-02eh]
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0268h
    push word ptr DGROUP:[bx+_SWeekday+2]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01B1h
    mov ax,word ptr DGROUP:[bx+_AmPm]
    jmp near ptr strftime_at_00bf
fmt_S_01b8:
    les bx, dword ptr [bp+010h]
    mov ax, word ptr es:[bx]
    mov word ptr [bp-012h], ax
    push ax
    cmp word ptr [bp-012h], 0ah
    jl short strftime_at_01cb
    jmp near ptr strftime_at_03d0
strftime_at_01cb:
    jmp near ptr strftime_at_03cb
fmt_U_01ce:
    les bx, dword ptr [bp+010h]
    mov ax, word ptr es:[bx+0ch]
    push ax
    mov ax, word ptr es:[bx+0eh]
    mov bx, 7
    cwd
    idiv bx
    pop ax
    sub ax, dx
    mov word ptr [bp-6], ax
    cmp word ptr [bp-6], 0
    jge short strftime_at_01f0
    add word ptr [bp-6], 7
strftime_at_01f0:
    les bx, dword ptr [bp+010h]
    mov ax, word ptr es:[bx+0eh]
    add ax, word ptr [bp-6]
    mov bx, 7
    cwd
    idiv bx
    mov word ptr [bp-6], ax
    push ax
    cmp word ptr [bp-6], 0ah
    jl short strftime_at_020d
    jmp near ptr strftime_at_03d0
strftime_at_020d:
    jmp near ptr strftime_at_03cb
fmt_w_0210:
    les bx, dword ptr [bp+010h]
    push word ptr es:[bx+0ch]
    jmp near ptr strftime_at_03e0
fmt_W_021a:
    les bx, dword ptr [bp+010h]
    mov ax, word ptr es:[bx+0ch]
    push ax
    mov ax, word ptr es:[bx+0eh]
    mov bx, 7
    cwd
    idiv bx
    pop ax
    sub ax, dx
    mov word ptr [bp-6], ax
    cmp word ptr [bp-6], 0
    jge short strftime_at_023c
    add word ptr [bp-6], 7
strftime_at_023c:
    les bx, dword ptr [bp+010h]
    mov ax, word ptr es:[bx+0eh]
    add ax, word ptr [bp-6]
    dec ax
    mov bx, 7
    cwd
    idiv bx
    mov word ptr [bp-6], ax
    push ax
    cmp word ptr [bp-6], 0ah
    jl short strftime_at_025a
    jmp near ptr strftime_at_03d0
strftime_at_025a:
    jmp near ptr strftime_at_03cb
fmt_x_025d:
    les bx, dword ptr [bp+010h]
    mov bx, word ptr es:[bx+0ch]
    mov cl, 2
    shl bx, cl
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01ADh
    mov dx,word ptr DGROUP:[bx+_AmPm+2]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0D4h
    call _atime
    add sp, 8
    jmp near ptr strftime_at_0405
fmt_d_00df:
    les bx, dword ptr [bp+010h]
    mov ax, word ptr es:[bx+6]
    mov word ptr [bp-0ch], ax
    push ax
    cmp word ptr [bp-0ch], 0ah
    jl short strftime_at_00f3
    jmp near ptr strftime_at_03d0
strftime_at_00f3:
    jmp near ptr strftime_at_03cb
fmt_H_00f6:
    les bx, dword ptr [bp+010h]
    mov ax, word ptr es:[bx+4]
    mov word ptr [bp-0eh], ax
    push ax
    cmp word ptr [bp-0eh], 0ah
    jl short strftime_at_010a
    jmp near ptr strftime_at_03d0
strftime_at_010a:
    jmp near ptr strftime_at_03cb
fmt_I_010d:
    les bx, dword ptr [bp+010h]
    mov ax, word ptr es:[bx+4]
    mov bx, 0ch
    cwd
    idiv bx
    mov word ptr [bp-6], dx
    cmp word ptr [bp-6], 0
    jne short strftime_at_0128
    mov word ptr [bp-6], 0ch
strftime_at_0128:
    push word ptr [bp-6]
    cmp word ptr [bp-6], 0ah
    jl short strftime_at_0134
    jmp near ptr strftime_at_03d0
strftime_at_0134:
    jmp near ptr strftime_at_03cb
fmt_j_0137:
    les bx, dword ptr [bp+010h]
    mov ax, word ptr es:[bx+0eh]
    inc ax
    mov word ptr [bp-6], ax
    push ax
    cmp word ptr [bp-6], 0ah
    jge short strftime_at_014e
    mov ax, 1
    jmp short strftime_at_0150
strftime_at_014e:
    xor ax, ax
strftime_at_0150:
    push ax
    cmp word ptr [bp-6], 064h
    jge short strftime_at_015c
    mov ax, 1
    jmp short strftime_at_015e
strftime_at_015c:
    xor ax, ax
strftime_at_015e:
    pop dx
    add dx, ax
    lea ax, [bp-02eh]
    add dx, ax
strftime_at_0166:
    push ss
    push dx
    jmp near ptr strftime_at_0305
fmt_m_016b:
    les bx, dword ptr [bp+010h]
    mov ax, word ptr es:[bx+8]
    inc ax
    mov word ptr [bp-6], ax
    push ax
    cmp word ptr [bp-6], 0ah
    jl short strftime_at_0180
    jmp near ptr strftime_at_03d0
strftime_at_0180:
    jmp near ptr strftime_at_03cb
fmt_M_0183:
    les bx, dword ptr [bp+010h]
    mov ax, word ptr es:[bx+2]
    mov word ptr [bp-010h], ax
    push ax
    cmp word ptr [bp-010h], 0ah
    jl short strftime_at_0197
    jmp near ptr strftime_at_03d0
strftime_at_0197:
    jmp near ptr strftime_at_03cb
fmt_p_019a:
    les bx, dword ptr [bp+010h]
    mov ax, word ptr es:[bx+4]
    mov bx, 0ch
    cwd
    idiv bx
    mov cl, 2
    shl ax, cl
    mov bx, ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0BBh
    mov ax,word ptr DGROUP:[bx+_LMonth]
strftime_at_00bf:
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    jmp near ptr strftime_at_0405
fmt_c_00c8:
    push word ptr [bp+012h]
    push word ptr [bp+010h]
    push word ptr [bp-2]
    push word ptr [bp-4]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0B7h
    mov dx,word ptr DGROUP:[bx+_LMonth+2]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0A6h
    mov ax,word ptr DGROUP:[bx+_SMonth]
    jmp short strftime_at_00bf
fmt_B_00ac:
    les bx, dword ptr [bp+010h]
    mov bx, word ptr es:[bx+8]
    mov cl, 2
    shl bx, cl
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0A2h
    mov dx,word ptr DGROUP:[bx+_SMonth+2]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 091h
    mov ax,word ptr DGROUP:[bx+_LWeekday]
    jmp short strftime_at_00bf
fmt_b_0097:
    les bx, dword ptr [bp+010h]
    mov bx, word ptr es:[bx+8]
    mov cl, 2
    shl bx, cl
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 08Dh
    mov dx,word ptr DGROUP:[bx+_LWeekday+2]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 07Ch
    mov ax,word ptr DGROUP:[bx+_SWeekday]
    jmp short strftime_at_00bf
fmt_A_0082:
    les bx, dword ptr [bp+010h]
    mov bx, word ptr es:[bx+0ch]
    mov cl, 2
    shl bx, cl
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 078h
    mov dx,word ptr DGROUP:[bx+_SWeekday+2]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 056h
    mov bx,offset strftime_formats
strftime_at_0059:
    mov ax, word ptr cs:[bx]
    cmp ax, word ptr [bp-0ah]
    je short strftime_at_0069
    add bx, 2
    loop short strftime_at_0059
    jmp near ptr strftime_at_0405
strftime_at_0069:
    jmp word ptr cs:[bx+strftime_switches-strftime_formats]
fmt_a_006d:
    les bx, dword ptr [bp+010h]
    mov bx, word ptr es:[bx+0ch]
    mov cl, 2
    shl bx, cl
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 03Eh
    call _strcpy
    add sp, 8
    inc word ptr [bp+0ch]
    les bx, dword ptr [bp+0ch]
    mov al, byte ptr es:[bx]
    cbw
    mov word ptr [bp-0ah], ax
    mov cx, 016h
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 035h
    mov ax,offset DGROUP:fmt_double_zero
    push ax
    push ss
    lea ax, [bp-02eh]
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 00h
_strftime label far
    push bp
    mov bp, sp
    sub sp, 02eh
    push si
    push di
    lea ax, [bp-02eh]
    mov word ptr [bp-2], ss
    mov word ptr [bp-4], ax
    mov word ptr [bp-8], 1
    jmp near ptr strftime_at_045e
strftime_at_0019:
    les bx, dword ptr [bp+0ch]
    cmp byte ptr es:[bx], 025h
    je short strftime_at_0034
    inc word ptr [bp-8]
    mov al, byte ptr es:[bx]
    les bx, dword ptr [bp+6]
    mov byte ptr es:[bx], al
    inc word ptr [bp+6]
    jmp near ptr strftime_at_0452
strftime_at_0034:
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04E6h
    dw offset fmt_y_03b1 ; ASCII %y
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04E4h
    dw offset fmt_x_025d ; ASCII %x
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04E2h
    dw offset fmt_w_0210 ; ASCII %w
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04E0h
    dw offset fmt_p_019a ; ASCII %p
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04DEh
    dw offset fmt_m_016b ; ASCII %m
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04DCh
    dw offset fmt_j_0137 ; ASCII %j
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04DAh
    dw offset fmt_d_00df ; ASCII %d
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04D8h
    dw offset fmt_c_00c8 ; ASCII %c
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04D6h
    dw offset fmt_b_0097 ; ASCII %b
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04D4h
    dw offset fmt_a_006d ; ASCII %a
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04D2h
    dw offset fmt_Z_03e7 ; ASCII %Z
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04D0h
    dw offset fmt_Y_03d5 ; ASCII %Y
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04CEh
    dw offset fmt_X_030b ; ASCII %X
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04CCh
    dw offset fmt_W_021a ; ASCII %W
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04CAh
    dw offset fmt_U_01ce ; ASCII %U
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04C8h
    dw offset fmt_S_01b8 ; ASCII %S
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04C6h
    dw offset fmt_M_0183 ; ASCII %M
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04C4h
    dw offset fmt_I_010d ; ASCII %I
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04C2h
    dw offset fmt_H_00f6 ; ASCII %H
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04C0h
    dw offset fmt_B_00ac ; ASCII %B
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04BEh
    dw offset fmt_A_0082 ; ASCII %A
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04BCh
strftime_switches label word
    dw offset fmt_pct_03fd ; ASCII %%
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0490h
strftime_formats label word
    dw 37,65,66,72,73,77,83,85,87,88,89 ; original ASCII format classes (WORDs)
    dw 90,97,98,99,100,106,109,112,119,120,121 ; original ASCII format classes (WORDs)
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0441h
    call _strncpy
    add sp, 0ah
    mov ax, word ptr [bp-6]
    add word ptr [bp-8], ax
    add word ptr [bp+6], ax
strftime_at_0452:
    inc word ptr [bp+0ch]
    lea ax, [bp-02eh]
    mov word ptr [bp-2], ss
    mov word ptr [bp-4], ax
strftime_at_045e:
    mov ax, word ptr [bp-8]
    cmp ax, word ptr [bp+0ah]
    jae short strftime_at_0472
    les bx, dword ptr [bp+0ch]
    cmp byte ptr es:[bx], 0
    je short strftime_at_0472
    jmp near ptr strftime_at_0019
strftime_at_0472:
    les bx, dword ptr [bp+6]
    mov byte ptr es:[bx], 0
    les bx, dword ptr [bp+0ch]
    cmp byte ptr es:[bx], 0
    je short strftime_at_0486
    xor ax, ax
    jmp short strftime_at_048a
strftime_at_0486:
    mov ax, word ptr [bp-8]
    dec ax
strftime_at_048a:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0422h
    call _strlen
    pop cx
    pop cx
    jmp short strftime_at_0431
strftime_at_042b:
    mov ax, word ptr [bp+0ah]
    sub ax, word ptr [bp-8]
strftime_at_0431:
    mov word ptr [bp-6], ax
    push ax
    push word ptr [bp-2]
    push word ptr [bp-4]
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 040Bh
    call _strlen
    pop cx
    pop cx
    mov dx, word ptr [bp+0ah]
    sub dx, word ptr [bp-8]
    cmp ax, dx
    jae short strftime_at_042b
    push word ptr [bp-2]
    push word ptr [bp-4]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0400h
    mov word ptr [bp-4],offset DGROUP:fmt_literal_percent
strftime_at_0405:
    push word ptr [bp-2]
    push word ptr [bp-4]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 03FDh
fmt_pct_03fd:
    mov word ptr [bp-2], ds
_TEXT ends
end
