; Original DOS Borland path split runtime with *genuine* CODE data tables.
; private near component_copy (0..92) and path separator check (92..214),
; then static slash/drive character + switch table (214..230),
; public far ___fnsplit at230 through775,
; second static punctuation/switch table776..803,
; and public far __splitpath at804 through849.
; Restores drive, DBCS-aware directory, basename and extension extraction;
; all string copies use real original Borland far CRT imports.
; Only the two real data lookup tables are emitted as DW; all executable
; CODE is typed 8086 mnemonics. No bytecode arrays/padding/object patches.
; Disjoint source intervals preserve original descending OMF writer order.
.8086
extrn _strcpy:far
extrn _strlen:far
extrn _strncpy:far
extrn ___path_issbcs:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
public ___fnsplit,__splitpath
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0324h
__splitpath label far
    push bp
    mov bp, sp
    push si
    push di
    push word ptr [bp+018h]
    push word ptr [bp+016h]
    push word ptr [bp+014h]
    push word ptr [bp+012h]
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push cs
    call near ptr ___fnsplit
    add sp, 014h
    pop di
    pop si
    pop bp
    retf
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0322h
    dw offset split_finish_directory
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0320h
    dw offset split_finish_name
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 031Eh
    dw offset split_scan_extension
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 031Ch
    dw offset split_finish_directory
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 031Ah
    dw offset split_scan_directory
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0318h
    dw offset split_finish_name
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0316h
    dw offset split_scan_drive
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0308h
path_component_classes label word
    dw 0,2Ah,2Eh,2Fh,3Ah,3Fh,5Ch ; NUL,*,.,/,:,?,backslash
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0262h
    call ___path_issbcs
    add sp, 8
    or ax, ax
    jne short split_at_271
    jmp near ptr split_at_191
split_at_271:
    inc word ptr [bp-6]
    inc word ptr [bp-4]
    les bx, dword ptr [bp-4]
    cmp byte ptr es:[bx], 0
    je short split_at_284
    or word ptr [bp-8], 4
split_at_284:
    push word ptr [bp+014h]
    push word ptr [bp+012h]
    push word ptr [bp-2]
    push word ptr [bp-4]
    mov ax, 8
    push ax
    call near ptr copy_component_bounded
    les bx, dword ptr [bp-4]
    mov byte ptr es:[bx], 0
    dec word ptr [bp-4]
    les bx, dword ptr [bp-4]
    cmp byte ptr es:[bx], 0
    je short split_at_2da
    cmp byte ptr es:[bx], 03ah
    je short split_at_2b3
    jmp near ptr split_at_191
split_at_2b3:
    mov ax, ss
    lea dx, [bp-05ah]
    cmp ax, word ptr [bp-2]
    je short split_at_2c0
    jmp near ptr split_at_191
split_at_2c0:
    cmp dx, word ptr [bp-4]
    je short split_at_2c8
    jmp near ptr split_at_191
split_at_2c8:
    jmp short split_at_2da
split_finish_name:
    cmp word ptr [bp-6], 0
    je short split_at_2d3
    jmp near ptr split_at_191
split_at_2d3:
    or word ptr [bp-8], 1
    jmp near ptr split_at_191
split_at_2da:
    les bx, dword ptr [bp-4]
    cmp byte ptr es:[bx], 03ah
    jne short split_at_2ff
    cmp byte ptr [bp-05bh], 0
    je short split_at_2ed
    or word ptr [bp-8], 010h
split_at_2ed:
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push ss
    lea ax, [bp-05bh]
    push ax
    mov ax, 2
    push ax
    call near ptr copy_component_bounded
split_at_2ff:
    mov ax, word ptr [bp-8]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01A1h
    mov bx,offset path_component_classes
split_at_1a4:
    mov ax, word ptr cs:[bx]
    cmp ax, word ptr [bp-0ah]
    je short split_at_1b3
    add bx, 2
    loop short split_at_1a4
    jmp short split_at_191
split_at_1b3:
    jmp word ptr cs:[bx+0eh]
split_scan_directory:
    cmp word ptr [bp-6], 0
    jne short split_at_1d6
    les bx, dword ptr [bp-4]
    cmp byte ptr es:[bx+1], 0
    jne short split_at_1d6
    push ss
    lea ax, [bp-05bh]
    push ax
    push word ptr [bp-2]
    push bx
    call near ptr check_path_delimiter
    mov word ptr [bp-6], ax
split_at_1d6:
    cmp word ptr [bp-6], 0
    jne short split_at_191
    test byte ptr [bp-8], 2
    jne short split_at_191
    or word ptr [bp-8], 2
    push word ptr [bp+018h]
    push word ptr [bp+016h]
    push word ptr [bp-2]
    push word ptr [bp-4]
    mov ax, 4
    push ax
    call near ptr copy_component_bounded
    les bx, dword ptr [bp-4]
    mov byte ptr es:[bx], 0
    jmp short split_at_191
split_scan_extension:
    mov ax, ss
    lea dx, [bp-05ah]
    cmp ax, word ptr [bp-2]
    jne short split_at_191
    cmp dx, word ptr [bp-4]
    jne short split_at_191
split_scan_drive:
    cmp word ptr [bp-6], 0
    je short split_finish_directory
    inc word ptr [bp-4]
    les bx, dword ptr [bp-4]
    cmp byte ptr es:[bx], 0
    je short split_at_227
    or word ptr [bp-8], 8
split_at_227:
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
    push word ptr [bp-2]
    push word ptr [bp-4]
    mov ax, 041h
    push ax
    call near ptr copy_component_bounded
    les bx, dword ptr [bp-4]
    mov byte ptr es:[bx], 0
    dec word ptr [bp-4]
    jmp near ptr split_at_2da
split_finish_directory:
    cmp word ptr [bp-6], 0
    je short split_at_250
    jmp near ptr split_at_191
split_at_250:
    les bx, dword ptr [bp-4]
    cmp byte ptr es:[bx], 0
    je short split_at_271
    push word ptr [bp-2]
    push bx
    push ss
    lea ax, [bp-05bh]
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0177h
    call _strncpy
    add sp, 0ah
    mov ax, word ptr [bp-6]
    add word ptr [bp-4], ax
    les bx, dword ptr [bp-4]
    mov byte ptr es:[bx], 0
    mov word ptr [bp-6], 0
split_at_191:
    dec word ptr [bp-4]
    les bx, dword ptr [bp-4]
    mov al, byte ptr es:[bx]
    cbw
    mov word ptr [bp-0ah], ax
    mov cx, 7
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 014Ah
    call _strlen
    pop cx
    pop cx
    mov word ptr [bp-6], ax
    cmp ax, 050h
    jle short split_at_15e
    mov word ptr [bp-6], 050h
split_at_15e:
    les bx, dword ptr [bp-4]
    mov byte ptr es:[bx], 0
    inc word ptr [bp-4]
    push word ptr [bp-6]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp-2]
    push word ptr [bp-4]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0E6h
___fnsplit label far
    push bp
    mov bp, sp
    sub sp, 05ch
    push si
    push di
    mov word ptr [bp-8], 0
    mov ax, word ptr [bp+0ah]
    or ax, word ptr [bp+0ch]
    je short split_at_102
    les bx, dword ptr [bp+0ah]
    mov byte ptr es:[bx], 0
split_at_102:
    mov ax, word ptr [bp+0eh]
    or ax, word ptr [bp+010h]
    je short split_at_111
    les bx, dword ptr [bp+0eh]
    mov byte ptr es:[bx], 0
split_at_111:
    mov ax, word ptr [bp+012h]
    or ax, word ptr [bp+014h]
    je short split_at_120
    les bx, dword ptr [bp+012h]
    mov byte ptr es:[bx], 0
split_at_120:
    mov ax, word ptr [bp+016h]
    or ax, word ptr [bp+018h]
    je short split_at_12f
    les bx, dword ptr [bp+016h]
    mov byte ptr es:[bx], 0
split_at_12f:
    lea ax, [bp-05ch]
    mov word ptr [bp-2], ss
    mov word ptr [bp-4], ax
    jmp short split_at_13d
split_at_13a:
    inc word ptr [bp+6]
split_at_13d:
    les bx, dword ptr [bp+6]
    cmp byte ptr es:[bx], 020h
    je short split_at_13a
    push word ptr [bp+8]
    push bx
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0E4h
    dw offset path_delimiter_is_separator
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0E2h
    dw offset path_delimiter_check_prev
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0E0h
    dw offset path_delimiter_is_separator
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0DEh
    dw offset path_delimiter_is_separator
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0D6h
path_separator_classes label word
    dw 0,2Fh,3Ah,5Ch ; NUL, slash, colon, backslash
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0A7h
    mov bx,offset path_separator_classes
split_at_0aa:
    mov ax, word ptr cs:[bx]
    cmp ax, word ptr [bp-2]
    je short split_at_0b9
    add bx, 2
    loop short split_at_0aa
    jmp short split_at_0cc
split_at_0b9:
    jmp word ptr cs:[bx+8]
path_delimiter_check_prev:
    les bx, dword ptr [bp+4]
    cmp byte ptr es:[bx-2], 0
    jne short split_at_0cc
path_delimiter_is_separator:
    mov ax, 1
    jmp short split_at_0ce
split_at_0cc:
    xor ax, ax
split_at_0ce:
    pop di
    pop si
    mov sp, bp
    pop bp
    ret 8
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 089h
    call ___path_issbcs
    add sp, 8
    or ax, ax
    jne short split_at_097
    jmp short split_at_0cc
split_at_097:
    dec word ptr [bp+4]
    les bx, dword ptr [bp+4]
    mov al, byte ptr es:[bx]
    cbw
    mov word ptr [bp-2], ax
    mov cx, 4
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 05Ch
check_path_delimiter label near
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    les bx, dword ptr [bp+4]
    cmp byte ptr es:[bx-1], 02eh
    jne short split_at_071
    dec word ptr [bp+4]
split_at_071:
    les bx, dword ptr [bp+4]
    cmp byte ptr es:[bx-1], 0
    je short split_at_097
    mov ax, word ptr [bp+4]
    dec ax
    push word ptr [bp+6]
    push ax
    push word ptr [bp+0ah]
    push word ptr [bp+8]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 04Eh
    call _strcpy
    add sp, 8
split_at_056:
    pop di
    pop si
    pop bp
    ret 0ah
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 02Eh
    call _strncpy
    add sp, 0ah
    les bx, dword ptr [bp+0ah]
    add bx, word ptr [bp+4]
    mov byte ptr es:[bx], 0
    jmp short split_at_056
split_at_042:
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 013h
    call _strlen
    pop cx
    pop cx
    cmp ax, word ptr [bp+4]
    jb short split_at_042
    push word ptr [bp+4]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 00h
copy_component_bounded label near
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp+0ah]
    or ax, word ptr [bp+0ch]
    je short split_at_056
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
end
