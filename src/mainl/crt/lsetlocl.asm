; Original Japanese Borland 16-bit large-model locale-library manager.
; Full 11-function locale boss: category dispatch, dynamic locale LIB
; opening/reading, category/environment handling and locale destruction.
; All executable content is symbolic 8086 ASM, not original CODE bytes.
.8086
extrn _sprintf:far,_calloc:far,_free:far,_getenv:far,_lseek:far,_memcpy:far
extrn _memset:far,_strcmp:far,_strcpy:far,_strlen:far,_strncmp:far,_strchr:far
extrn __strcoll:far,__strxfrm:far,__dos_close:far,__dos_open:far,__dos_read:far
extrn __argv:dword,_findfirst:far,_fnmerge:far,_fnsplit:far,_searchpath:far
extrn __llocaleconv:far,___set_c_locale:far,___initialize_locale:far
extrn __LocaleCatNames:byte,__pLocale:dword,__LocaleLibName:byte,N_LDIV@:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __lsetlocale,___open_localelib,___open_locale,___find_localecat,___set_localestring_locale,___locale_error,___read_localecat,___read_localeenv,___find_localelib,___delete_locale,___dup_locale

; Original public locale lifecycle interface +0.
__lsetlocale:
    push bp
    mov bp, sp
    sub sp, 0a2h
    push si
    push di
    mov word ptr [bp - 6], 0
    mov word ptr [bp - 8], 0
    mov ax, 7dh
    push ax
    xor ax, ax
    push ax
    push ss
    lea ax, [bp - 0a2h]
    push ax
    call _memset
    add sp, 8
    les bx,dword ptr DGROUP:__pLocale
    cmp word ptr es:[bx + 24h], 0
    jne loc_008f
    mov ax, word ptr [bp + 8]
    or ax, word ptr [bp + 0ah]
    je loc_0082
    push ds
    mov ax,offset DGROUP:all_C_locale
    push ax
    push word ptr [bp + 0ah]
    push word ptr [bp + 8]
    call _strcmp
    add sp, 8
    or ax, ax
    jne loc_0058
    cmp word ptr [bp + 6], 0
    je loc_0075
loc_0058:
    push ds
    mov ax,offset DGROUP:literal_C
    push ax
    push word ptr [bp + 0ah]
    push word ptr [bp + 8]
    call _strcmp
    add sp, 8
    or ax, ax
    jne loc_0082
    cmp word ptr [bp + 6], 0
    jne loc_0082
loc_0075:
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 4eh
    jmp near ptr loc_06e9
loc_0082:
    call ___initialize_locale
    cmp ax, 0ffffh
    jne loc_008f
    jmp near ptr loc_0500
loc_008f:
    mov ax, word ptr [bp + 8]
    or ax, word ptr [bp + 0ah]
    je loc_00d0
    push ds
    mov ax,offset DGROUP:initial_C_locale
    push ax
    push word ptr [bp + 0ah]
    push word ptr [bp + 8]
    call _strcmp
    add sp, 8
    or ax, ax
    je loc_00c5
    push ds
    mov ax,offset DGROUP:single_C
    push ax
    push word ptr [bp + 0ah]
    push word ptr [bp + 8]
    call _strcmp
    add sp, 8
    or ax, ax
    jne loc_00d0
loc_00c5:
    push word ptr [bp + 6]
    call ___set_c_locale
    jmp near ptr loc_016f
loc_00d0:
    mov ax, word ptr [bp + 8]
    or ax, word ptr [bp + 0ah]
    je loc_00db
    jmp near ptr loc_015e
loc_00db:
    mov bx, word ptr [bp + 6]
    cmp bx, 7
    ja loc_0151
    add bx, bx
    jmp word ptr cs:[bx+locale_dispatch+14]
fmt_00ea:
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 4eh
    jmp short loc_0148
fmt_00f6:
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 160h
    jmp short loc_0148
fmt_0102:
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 130h
    jmp short loc_0148
fmt_010e:
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 1aah
    jmp short loc_0148
fmt_011a:
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 1f6h
    jmp short loc_0148
fmt_0126:
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 23ah
    jmp short loc_0148
fmt_0132:
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 943h
    jmp short loc_0148
fmt_013e:
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 971h
loc_0148:
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
    jmp near ptr loc_06e3
loc_0151:
    mov word ptr [bp - 6], 0
    mov word ptr [bp - 8], 0
    jmp near ptr loc_06e3
loc_015e:
    les bx,dword ptr [bp + 8]
    cmp byte ptr es:[bx], 0
    jne loc_0173
    push word ptr [bp + 6]
    assume cs:NOTHING
    call far ptr ___read_localeenv
    assume cs:_TEXT
loc_016f:
    pop cx
    jmp near ptr loc_06e9
loc_0173:
    mov ax, word ptr [bp + 8]
    or ax, word ptr [bp + 0ah]
    je loc_0195
    mov ax, 3bh
    push ax
    push word ptr [bp + 0ah]
    push word ptr [bp + 8]
    call _strchr
    add sp, 6
    or ax, dx
    je loc_0195
    mov al, 1
    jmp short loc_0197
loc_0195:
    mov al, 0
loc_0197:
    or al, al
    je loc_01c5
    push word ptr [bp + 0ah]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    assume cs:NOTHING
    call far ptr ___set_localestring_locale
    assume cs:_TEXT
    add sp, 6
    cmp ax, 0ffffh
    jne loc_01b4
    jmp near ptr loc_0500
loc_01b4:
    xor ax, ax
    push ax
    push ax
    push word ptr [bp + 6]
    push cs
    call __lsetlocale
    add sp, 6
    jmp near ptr loc_06e9
loc_01c5:
    mov ax, 40h
    push ax
    push word ptr [bp + 0ah]
    push word ptr [bp + 8]
    call _strchr
    add sp, 6
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    or ax, dx
    jne loc_01f4
    mov byte ptr [bp - 2ah], 1
    push word ptr [bp + 0ah]
    push word ptr [bp + 8]
    call _strlen
    pop cx
    pop cx
    jmp short loc_0203
loc_01f4:
    mov byte ptr [bp - 2ah], 0
    mov ax, word ptr [bp - 4]
    xor dx, dx
    sub ax, word ptr [bp + 8]
    sbb dx, 0
loc_0203:
    mov word ptr [bp - 2ch], ax
    mov dx, word ptr [bp + 0ah]
    mov ax, word ptr [bp + 8]
    mov word ptr [bp - 2eh], dx
    mov word ptr [bp - 30h], ax
    push ss
    lea ax, [bp - 0a2h]
    push ax
    assume cs:NOTHING
    call far ptr ___open_localelib
    assume cs:_TEXT
    pop cx
    pop cx
    or ax, ax
    je loc_0226
    jmp near ptr loc_0500
loc_0226:
    push ss
    lea ax, [bp - 0a2h]
    push ax
    assume cs:NOTHING
    call far ptr ___open_locale
    assume cs:_TEXT
    pop cx
    pop cx
    or ax, ax
    je loc_023a
    jmp near ptr loc_0500
loc_023a:
    push ds
    mov ax,offset DGROUP:__pLocale
    push ax
    push ss
    lea ax, [bp - 29h]
    push ax
    assume cs:NOTHING
    call far ptr ___dup_locale
    assume cs:_TEXT
    add sp, 8
    cmp ax, 0ffffh
    jne loc_0254
    jmp near ptr loc_0500
loc_0254:
    les bx,dword ptr DGROUP:__pLocale
    cmp byte ptr es:[bx + 2ah], 1
    jne loc_0266
    cmp byte ptr es:[bx + 2bh], 1
    je loc_0275
loc_0266:
    push ss
    lea ax, [bp - 29h]
    push ax
    assume cs:NOTHING
    call far ptr ___delete_locale
    assume cs:_TEXT
    pop cx
    pop cx
    jmp near ptr loc_0500
loc_0275:
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 0ch], ax
    mov word ptr [bp - 0ah], 1
    cmp word ptr [bp + 6], 0
    je loc_0289
    jmp near ptr loc_063a
loc_0289:
    mov word ptr [bp - 0ah], 6
    inc word ptr [bp - 0ch]
    jmp near ptr loc_063a
loc_0294:
    push word ptr [bp - 0ch]
    push ss
    lea ax, [bp - 0a2h]
    push ax
    assume cs:NOTHING
    call far ptr ___read_localecat
    assume cs:_TEXT
    add sp, 6
    or ax, ax
    je loc_02be
    xor ax, ax
    push ax
    push ax
    push ss
    lea ax, [bp - 0a2h]
    push ax
    assume cs:NOTHING
    call far ptr ___locale_error
    assume cs:_TEXT
    add sp, 8
    jmp near ptr loc_0500
loc_02be:
    mov bx, word ptr [bp - 0ch]
    inc word ptr [bp - 0ch]
    dec bx
    cmp bx, 6
    jbe loc_02cd
    jmp near ptr loc_0630
loc_02cd:
    add bx, bx
    jmp word ptr cs:[bx+locale_dispatch]
fmt_02d4:
    mov ax, 1
    push ax
    les bx,dword ptr DGROUP:__pLocale
    push word ptr es:[bx + 18eh]
    call _calloc
    pop cx
    pop cx
    mov word ptr [bp - 12h], dx
    mov word ptr [bp - 14h], ax
    or ax, word ptr [bp - 12h]
    jne loc_0308
    xor ax, ax
    push ax
    push ax
    push ss
    lea ax, [bp - 0a2h]
    push ax
    assume cs:NOTHING
    call far ptr ___locale_error
    assume cs:_TEXT
    add sp, 8
    jmp near ptr loc_0500
loc_0308:
    push ss
    lea ax, [bp - 10h]
    push ax
    les bx,dword ptr DGROUP:__pLocale
    mov ax, 101h
    imul word ptr es:[bx + 184h]
    add ax, 101h
    push ax
    push word ptr [bp - 12h]
    push word ptr [bp - 14h]
    push word ptr [bp - 32h]
    call __dos_read
    add sp, 0ch
    or ax, ax
    je loc_0349
    push word ptr [bp - 12h]
    push word ptr [bp - 14h]
    push ss
    lea ax, [bp - 0a2h]
    push ax
    assume cs:NOTHING
    call far ptr ___locale_error
    assume cs:_TEXT
    add sp, 8
    jmp near ptr loc_0500
loc_0349:
    les bx,dword ptr DGROUP:__pLocale
    mov ax, 101h
    imul word ptr es:[bx + 184h]
    add ax, 101h
    mov dx, word ptr [bp - 12h]
    mov bx, word ptr [bp - 14h]
    add bx, ax
    mov word ptr [bp - 22h], dx
    mov word ptr [bp - 24h], bx
    push ss
    lea ax, [bp - 10h]
    push ax
    mov ax, 2
    push ax
    push ss
    lea ax, [bp - 0eh]
    push ax
    push word ptr [bp - 32h]
    call __dos_read
    add sp, 0ch
    or ax, ax
    je loc_039a
    push word ptr [bp - 12h]
    push word ptr [bp - 14h]
    push ss
    lea ax, [bp - 0a2h]
    push ax
    assume cs:NOTHING
    call far ptr ___locale_error
    assume cs:_TEXT
    add sp, 8
    jmp near ptr loc_0500
loc_039a:
    cmp word ptr [bp - 0eh], 0
    je loc_03ec
    mov dx, word ptr [bp - 22h]
    mov ax, word ptr [bp - 24h]
    mov word ptr [bp - 16h], dx
    mov word ptr [bp - 18h], ax
    push ss
    lea ax, [bp - 10h]
    push ax
    mov ax, 52h
    imul word ptr [bp - 0eh]
    push ax
    push word ptr [bp - 16h]
    push word ptr [bp - 18h]
    push word ptr [bp - 32h]
    call __dos_read
    add sp, 0ch
    or ax, ax
    je loc_03e4
    push word ptr [bp - 12h]
    push word ptr [bp - 14h]
    push ss
    lea ax, [bp - 0a2h]
    push ax
    assume cs:NOTHING
    call far ptr ___locale_error
    assume cs:_TEXT
    add sp, 8
    jmp near ptr loc_0500
loc_03e4:
    mov ax, word ptr [bp - 10h]
    add word ptr [bp - 24h], ax
    jmp short loc_03f6
loc_03ec:
    mov word ptr [bp - 16h], 0
    mov word ptr [bp - 18h], 0
loc_03f6:
    push ss
    lea ax, [bp - 10h]
    push ax
    mov ax, 2
    push ax
    push ss
    lea ax, [bp - 0eh]
    push ax
    push word ptr [bp - 32h]
    call __dos_read
    add sp, 0ch
    or ax, ax
    je loc_042a
    push word ptr [bp - 12h]
    push word ptr [bp - 14h]
    push ss
    lea ax, [bp - 0a2h]
    push ax
    assume cs:NOTHING
    call far ptr ___locale_error
    assume cs:_TEXT
    add sp, 8
    jmp near ptr loc_0500
loc_042a:
    cmp word ptr [bp - 0eh], 0
    je loc_047c
    mov dx, word ptr [bp - 22h]
    mov ax, word ptr [bp - 24h]
    mov word ptr [bp - 1ah], dx
    mov word ptr [bp - 1ch], ax
    push ss
    lea ax, [bp - 10h]
    push ax
    mov ax, 13h
    imul word ptr [bp - 0eh]
    push ax
    push word ptr [bp - 1ah]
    push word ptr [bp - 1ch]
    push word ptr [bp - 32h]
    call __dos_read
    add sp, 0ch
    or ax, ax
    je loc_0474
    push word ptr [bp - 12h]
    push word ptr [bp - 14h]
    push ss
    lea ax, [bp - 0a2h]
    push ax
    assume cs:NOTHING
    call far ptr ___locale_error
    assume cs:_TEXT
    add sp, 8
    jmp near ptr loc_0500
loc_0474:
    mov ax, word ptr [bp - 10h]
    add word ptr [bp - 24h], ax
    jmp short loc_0486
loc_047c:
    mov word ptr [bp - 1ah], 0
    mov word ptr [bp - 1ch], 0
loc_0486:
    push ss
    lea ax, [bp - 10h]
    push ax
    mov ax, 2
    push ax
    push ss
    lea ax, [bp - 0eh]
    push ax
    push word ptr [bp - 32h]
    call __dos_read
    add sp, 0ch
    or ax, ax
    je loc_04b9
    push word ptr [bp - 12h]
    push word ptr [bp - 14h]
    push ss
    lea ax, [bp - 0a2h]
    push ax
    assume cs:NOTHING
    call far ptr ___locale_error
    assume cs:_TEXT
    add sp, 8
    jmp short loc_0500
loc_04b9:
    cmp word ptr [bp - 0eh], 0
    je loc_0507
    mov dx, word ptr [bp - 22h]
    mov ax, word ptr [bp - 24h]
    mov word ptr [bp - 1eh], dx
    mov word ptr [bp - 20h], ax
    push ss
    lea ax, [bp - 10h]
    push ax
    mov ax, 16h
    imul word ptr [bp - 0eh]
    push ax
    push word ptr [bp - 1eh]
    push word ptr [bp - 20h]
    push word ptr [bp - 32h]
    call __dos_read
    add sp, 0ch
    or ax, ax
    je loc_0511
    push word ptr [bp - 12h]
    push word ptr [bp - 14h]
    push ss
    lea ax, [bp - 0a2h]
    push ax
    assume cs:NOTHING
    call far ptr ___locale_error
    assume cs:_TEXT
    add sp, 8
loc_0500:
    xor dx, dx
    xor ax, ax
    jmp near ptr loc_06e9
loc_0507:
    mov word ptr [bp - 1eh], 0
    mov word ptr [bp - 20h], 0
loc_0511:
    les bx,dword ptr DGROUP:__pLocale
    mov word ptr es:[bx + 1a2h], seg __strcoll
    mov word ptr es:[bx + 1a0h], offset __strcoll
    mov word ptr es:[bx + 1a6h], seg __strxfrm
    mov word ptr es:[bx + 1a4h], offset __strxfrm
    mov ax, word ptr es:[bx + 190h]
    or ax, word ptr es:[bx + 192h]
    je loc_054e
    push word ptr es:[bx + 192h]
    push word ptr es:[bx + 190h]
    call _free
    pop cx
    pop cx
loc_054e:
    les bx,dword ptr DGROUP:__pLocale
    mov dx, word ptr [bp - 12h]
    mov ax, word ptr [bp - 14h]
    mov word ptr es:[bx + 192h], dx
    mov word ptr es:[bx + 190h], ax
    mov dx, word ptr [bp - 16h]
    mov ax, word ptr [bp - 18h]
    mov word ptr es:[bx + 196h], dx
    mov word ptr es:[bx + 194h], ax
    mov dx, word ptr [bp - 1ah]
    mov ax, word ptr [bp - 1ch]
    mov word ptr es:[bx + 19ah], dx
    mov word ptr es:[bx + 198h], ax
    mov dx, word ptr [bp - 1eh]
    mov ax, word ptr [bp - 20h]
    mov word ptr es:[bx + 19eh], dx
    mov word ptr es:[bx + 19ch], ax
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 160h
loc_059c:
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
    jmp near ptr loc_063a
fmt_05a5:
    les bx,dword ptr DGROUP:__pLocale
    mov dx, word ptr es:[bx + 154h]
    mov ax, word ptr es:[bx + 152h]
    add ax, 101h
    mov word ptr es:[bx + 158h], dx
    mov word ptr es:[bx + 156h], ax
    mov dx, word ptr es:[bx + 158h]
    mov ax, word ptr es:[bx + 156h]
    add ax, 100h
    mov word ptr es:[bx + 15ch], dx
    mov word ptr es:[bx + 15ah], ax
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 130h
    jmp short loc_059c
fmt_05e3:
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 1aah
    jmp short loc_059c
fmt_05ef:
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 1f6h
    jmp short loc_059c
fmt_05fb:
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 23ah
    jmp short loc_059c
fmt_0607:
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 943h
    jmp short loc_059c
fmt_0613:
    les bx,dword ptr DGROUP:__pLocale
    mov ax, word ptr es:[bx + 993h]
    or ax, word ptr es:[bx + 995h]
    je loc_063a
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 971h
    jmp near ptr loc_059c
loc_0630:
    mov word ptr [bp - 6], 0
    mov word ptr [bp - 8], 0
loc_063a:
    mov ax, word ptr [bp - 0ah]
    dec word ptr [bp - 0ah]
    or ax, ax
    je loc_0647
    jmp near ptr loc_0294
loc_0647:
    push word ptr [bp - 32h]
    call __dos_close
    mov ax, word ptr DGROUP:__pLocale
    add ax, 971h
    push word ptr DGROUP:__pLocale+2
    push ax
    mov ax, word ptr DGROUP:__pLocale
    add ax, 943h
    push word ptr DGROUP:__pLocale+2
    push ax
    mov ax, word ptr DGROUP:__pLocale
    add ax, 23ah
    push word ptr DGROUP:__pLocale+2
    push ax
    mov ax, word ptr DGROUP:__pLocale
    add ax, 1f6h
    push word ptr DGROUP:__pLocale+2
    push ax
    mov ax, word ptr DGROUP:__pLocale
    add ax, 1aah
    push word ptr DGROUP:__pLocale+2
    push ax
    mov ax, word ptr DGROUP:__pLocale
    add ax, 130h
    push word ptr DGROUP:__pLocale+2
    push ax
    mov ax, word ptr DGROUP:__pLocale
    add ax, 160h
    push word ptr DGROUP:__pLocale+2
    push ax
    push ds
    mov ax,offset DGROUP:categories_format
    push ax
    mov ax, word ptr DGROUP:__pLocale
    add ax, 4eh
    push word ptr DGROUP:__pLocale+2
    push ax
    call _sprintf
    add sp, 26h
    cmp word ptr [bp + 6], 0
    jne loc_06ca
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 4eh
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
loc_06ca:
    mov ax, word ptr [bp - 29h]
    or ax, word ptr [bp - 27h]
    je loc_06de
    push ss
    lea ax, [bp - 29h]
    push ax
    assume cs:NOTHING
    call far ptr ___delete_locale
    assume cs:_TEXT
    pop cx
    pop cx
loc_06de:
    call __llocaleconv
loc_06e3:
    mov dx, word ptr [bp - 6]
    mov ax, word ptr [bp - 8]
loc_06e9:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original 15-entry locale format/category dispatcher.
locale_dispatch label word
    dw fmt_02d4
    dw fmt_05a5
    dw fmt_05e3
    dw fmt_05ef
    dw fmt_05fb
    dw fmt_0607
    dw fmt_0613
    dw fmt_00ea
    dw fmt_00f6
    dw fmt_0102
    dw fmt_010e
    dw fmt_011a
    dw fmt_0126
    dw fmt_0132
    dw fmt_013e


; Original public locale lifecycle interface +1805.
___open_localelib:
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    push ds
    mov ax,offset DGROUP:__LocaleLibName
    push ax
    assume cs:NOTHING
    call far ptr ___find_localelib
    assume cs:_TEXT
    pop cx
    pop cx
    cmp ax, 0ffffh
    jne loc_0729
    jmp near ptr loc_07de
loc_0729:
    mov ax, word ptr [bp + 6]
    add ax, 70h
    push word ptr [bp + 8]
    push ax
    mov ax, 8001h
    push ax
    push ds
    mov ax,offset DGROUP:__LocaleLibName
    push ax
    call __dos_open
    add sp, 0ah
    or ax, ax
    je loc_075d
    xor ax, ax
    push ax
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    assume cs:NOTHING
    call far ptr ___locale_error
    assume cs:_TEXT
    add sp, 8
    jmp near ptr loc_07de
loc_075d:
    push ss
    lea ax, [bp - 2]
    push ax
    mov ax, 26h
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 70h]
    call __dos_read
    add sp, 0ch
    or ax, ax
    je loc_0793
    xor ax, ax
    push ax
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    assume cs:NOTHING
    call far ptr ___locale_error
    assume cs:_TEXT
    add sp, 8
    jmp short loc_07de
loc_0793:
    les bx,dword ptr [bp + 6]
    cmp byte ptr es:[bx + 20h], 1
    jne loc_07a8
    cmp byte ptr es:[bx + 21h], 0
    jne loc_07a8
    xor ax, ax
    jmp short loc_07ab
loc_07a8:
    mov ax, 0ffffh
loc_07ab:
    cmp ax, 0ffffh
    jne loc_07c4
    xor ax, ax
    push ax
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    assume cs:NOTHING
    call far ptr ___locale_error
    assume cs:_TEXT
    add sp, 8
    jmp short loc_07de
loc_07c4:
    les bx,dword ptr [bp + 6]
    cmp word ptr es:[bx + 24h], 0
    jne loc_07e3
    xor ax, ax
    push ax
    push ax
    push word ptr [bp + 8]
    push bx
    assume cs:NOTHING
    call far ptr ___locale_error
    assume cs:_TEXT
    add sp, 8
loc_07de:
    mov ax, 0ffffh
    jmp short loc_07e5
loc_07e3:
    xor ax, ax
loc_07e5:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original public locale lifecycle interface +2027.
___open_locale:
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    mov word ptr [bp - 4], 0
    jmp short loc_084e
loc_07fa:
    push ss
    lea ax, [bp - 2]
    push ax
    mov ax, 26h
    push ax
    mov ax, word ptr [bp + 6]
    add ax, 26h
    push word ptr [bp + 8]
    push ax
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 70h]
    call __dos_read
    add sp, 0ch
    or ax, ax
    je loc_0823
    jmp near ptr loc_08a8
loc_0823:
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 76h]
    mov ax, word ptr [bp + 6]
    add ax, 26h
    push word ptr [bp + 8]
    push ax
    push word ptr es:[bx + 74h]
    push word ptr es:[bx + 72h]
    call _strncmp
    add sp, 0ah
    mov word ptr [bp - 6], ax
    or ax, ax
    je loc_085a
    inc word ptr [bp - 4]
loc_084e:
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 24h]
    cmp ax, word ptr [bp - 4]
    ja loc_07fa
loc_085a:
    cmp word ptr [bp - 6], 0
    jne loc_08a8
    xor ax, ax
    push ax
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 4ah]
    push word ptr es:[bx + 48h]
    push word ptr es:[bx + 70h]
    call _lseek
    add sp, 8
    cmp dx, -1
    jne loc_0884
    cmp ax, 0ffffh
    je loc_08a8
loc_0884:
    push ss
    lea ax, [bp - 2]
    push ax
    mov ax, 4eh
    push ax
    push word ptr DGROUP:__pLocale+2
    push word ptr DGROUP:__pLocale
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 70h]
    call __dos_read
    add sp, 0ch
    or ax, ax
    je loc_08bf
loc_08a8:
    xor ax, ax
    push ax
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    assume cs:NOTHING
    call far ptr ___locale_error
    assume cs:_TEXT
    add sp, 8
    mov ax, 0ffffh
    jmp short loc_08c1
loc_08bf:
    xor ax, ax
loc_08c1:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original public locale lifecycle interface +2247.
___find_localecat:
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    push ss
    lea ax, [bp - 6]
    push ax
    mov ax, 2
    push ax
    push ss
    lea ax, [bp - 4]
    push ax
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 70h]
    call __dos_read
    add sp, 0ch
    or ax, ax
    je loc_08f3
    jmp near ptr loc_09a9
loc_08f3:
    mov word ptr [bp - 2], 0
    jmp near ptr loc_09c0
loc_08fb:
    push ss
    lea ax, [bp - 6]
    push ax
    mov ax, 24h
    push ax
    mov ax, word ptr [bp + 6]
    add ax, 4ch
    push word ptr [bp + 8]
    push ax
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 70h]
    call __dos_read
    add sp, 0ch
    or ax, ax
    je loc_0924
    jmp near ptr loc_09a9
loc_0924:
    les bx,dword ptr [bp + 6]
    cmp byte ptr es:[bx + 78h], 0
    je loc_095c
    push word ptr es:[bx + 76h]
    mov ax, word ptr [bp + 6]
    add ax, 4eh
    push word ptr [bp + 8]
    push ax
    push word ptr es:[bx + 74h]
    push word ptr es:[bx + 72h]
    call _strncmp
    add sp, 0ah
    or ax, ax
    jne loc_0981
    les bx,dword ptr [bp + 6]
    cmp word ptr es:[bx + 6eh], 0
    je loc_0981
    jmp short loc_097d
loc_095c:
    mov ax, word ptr [bp + 6]
    add ax, 4eh
    push word ptr [bp + 8]
    push ax
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 74h]
    push word ptr es:[bx + 72h]
    call _strcmp
    add sp, 8
    or ax, ax
    jne loc_0981
loc_097d:
    xor ax, ax
    jmp short loc_09ce
loc_0981:
    mov ax, 1
    push ax
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 4ch]
    sub ax, 24h
    xor dx, dx
    push dx
    push ax
    push word ptr es:[bx + 70h]
    call _lseek
    add sp, 8
    cmp dx, -1
    jne loc_09bd
    cmp ax, 0ffffh
    jne loc_09bd
loc_09a9:
    xor ax, ax
    push ax
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    assume cs:NOTHING
    call far ptr ___locale_error
    assume cs:_TEXT
    add sp, 8
    jmp short loc_09cb
loc_09bd:
    inc word ptr [bp - 2]
loc_09c0:
    mov ax, word ptr [bp - 2]
    cmp ax, word ptr [bp - 4]
    jge loc_09cb
    jmp near ptr loc_08fb
loc_09cb:
    mov ax, 0ffffh
loc_09ce:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original public locale lifecycle interface +2516.
___set_localestring_locale:
    push bp
    mov bp, sp
    sub sp, 0eah
    push si
    push di
    mov dx, word ptr [bp + 0ah]
    mov ax, word ptr [bp + 8]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    push dx
    push ax
    push ss
    lea ax, [bp - 0eah]
    push ax
    call _strcpy
    add sp, 8
    lea ax, [bp - 0eah]
    mov word ptr [bp - 2], ss
    mov word ptr [bp - 4], ax
    mov word ptr [bp - 0ah], 1
    jmp short loc_0a7c
loc_0a0a:
    mov ax, 3bh
    push ax
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    call _strchr
    add sp, 6
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
    or ax, dx
    je loc_0a74
    les bx,dword ptr [bp - 8]
    mov byte ptr es:[bx], 0
    cmp word ptr [bp + 6], 0
    jne loc_0a49
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    push word ptr [bp - 0ah]
    push cs
    call __lsetlocale
    add sp, 6
    or ax, dx
    jne loc_0a63
    jmp short loc_0a74
loc_0a49:
    mov ax, word ptr [bp - 0ah]
    cmp ax, word ptr [bp + 6]
    jne loc_0a63
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    push ax
    push cs
    call __lsetlocale
    add sp, 6
    or ax, dx
    je loc_0a74
loc_0a63:
    inc word ptr [bp - 8]
    mov dx, word ptr [bp - 6]
    mov ax, word ptr [bp - 8]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    jmp short loc_0a79
loc_0a74:
    mov ax, 0ffffh
    jmp short loc_0a84
loc_0a79:
    inc word ptr [bp - 0ah]
loc_0a7c:
    cmp word ptr [bp - 0ah], 8
    jl loc_0a0a
    xor ax, ax
loc_0a84:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original public locale lifecycle interface +2698.
___locale_error:
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    les bx,dword ptr [bp + 6]
    cmp word ptr es:[bx + 70h], 0
    je loc_0aa6
    push word ptr es:[bx + 70h]
    call __dos_close
    pop cx
loc_0aa6:
    mov ax, word ptr [bp + 0ah]
    or ax, word ptr [bp + 0ch]
    je loc_0abb
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    call _free
    pop cx
    pop cx
loc_0abb:
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 79h]
    or ax, word ptr es:[bx + 7bh]
    je loc_0ae4
    mov dx, word ptr es:[bx + 7bh]
    mov ax, word ptr es:[bx + 79h]
    mov word ptr DGROUP:__pLocale+2, dx
    mov word ptr DGROUP:__pLocale, ax
loc_0ae4:
    mov ax, word ptr [bp - 4]
    or ax, word ptr [bp - 2]
    je loc_0af8
    push ss
    lea ax, [bp - 4]
    push ax
    assume cs:NOTHING
    call far ptr ___delete_locale
    assume cs:_TEXT
    pop cx
    pop cx
loc_0af8:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original public locale lifecycle interface +2814.
___read_localecat:
    push bp
    mov bp, sp
    sub sp, 10h
    push si
    push di
    mov bx, word ptr [bp + 0ah]
    dec bx
    cmp bx, 6
    jbe loc_0b12
    jmp near ptr loc_0d56
loc_0b12:
    add bx, bx
    jmp word ptr cs:[bx+category_dispatch]
locale_0b19:
    mov cx, 1
    les bx,dword ptr DGROUP:__pLocale
    mov dx, word ptr es:[bx + 38h]
    mov ax, word ptr es:[bx + 36h]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 182h
    mov word ptr [bp - 0ah], dx
    mov word ptr [bp - 0ch], ax
    mov word ptr [bp - 0eh], 0eh
    mov ax, word ptr DGROUP:__pLocale
    add ax, 15eh
    jmp short loc_0b7f
locale_0b4b:
    mov cx, 2
    les bx,dword ptr DGROUP:__pLocale
    mov dx, word ptr es:[bx + 34h]
    mov ax, word ptr es:[bx + 32h]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    mov dx, word ptr es:[bx + 154h]
    mov ax, word ptr es:[bx + 152h]
    mov word ptr [bp - 0ah], dx
    mov word ptr [bp - 0ch], ax
    mov word ptr [bp - 0eh], 301h
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 12eh
loc_0b7f:
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
    les bx,dword ptr DGROUP:__pLocale
    test word ptr es:[bx + 30h], cx
    je loc_0b92
    jmp near ptr loc_0cac
loc_0b92:
    jmp near ptr loc_0d56
locale_0b95:
    mov cx, 4
    les bx,dword ptr DGROUP:__pLocale
    mov dx, word ptr es:[bx + 40h]
    mov ax, word ptr es:[bx + 3eh]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 1cch
    mov word ptr [bp - 0ah], dx
    mov word ptr [bp - 0ch], ax
    mov word ptr [bp - 0eh], 28h
    mov ax, word ptr DGROUP:__pLocale
    add ax, 1a8h
    jmp short loc_0b7f
locale_0bc7:
    mov cx, 8
    les bx,dword ptr DGROUP:__pLocale
    mov dx, word ptr es:[bx + 44h]
    mov ax, word ptr es:[bx + 42h]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 218h
    mov word ptr [bp - 0ah], dx
    mov word ptr [bp - 0ch], ax
    mov word ptr [bp - 0eh], 20h
    mov ax, word ptr DGROUP:__pLocale
    add ax, 1f4h
    jmp short loc_0b7f
locale_0bf9:
    mov cx, 10h
    les bx,dword ptr DGROUP:__pLocale
    mov dx, word ptr es:[bx + 3ch]
    mov ax, word ptr es:[bx + 3ah]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 25ch
    mov word ptr [bp - 0ah], dx
    mov word ptr [bp - 0ch], ax
    mov word ptr [bp - 0eh], 6e5h
    mov ax, word ptr DGROUP:__pLocale
    add ax, 238h
    jmp near ptr loc_0b7f
locale_0c2c:
    mov cx, 20h
    les bx,dword ptr DGROUP:__pLocale
    mov dx, word ptr es:[bx + 48h]
    mov ax, word ptr es:[bx + 46h]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 965h
    mov word ptr [bp - 0ah], dx
    mov word ptr [bp - 0ch], ax
    mov word ptr [bp - 0eh], 0ah
    mov ax, word ptr DGROUP:__pLocale
    add ax, 941h
    jmp near ptr loc_0b7f
locale_0c5f:
    mov cx, 40h
    les bx,dword ptr DGROUP:__pLocale
    mov dx, word ptr es:[bx + 4ch]
    mov ax, word ptr es:[bx + 4ah]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    mov ax, word ptr es:[bx + 993h]
    or ax, word ptr es:[bx + 995h]
    jne loc_0c83
    jmp near ptr loc_0d56
loc_0c83:
    les bx,dword ptr DGROUP:__pLocale
    mov dx, word ptr es:[bx + 995h]
    mov ax, word ptr es:[bx + 993h]
    mov word ptr [bp - 0ah], dx
    mov word ptr [bp - 0ch], ax
    mov word ptr [bp - 0eh], 0
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 96fh
    jmp near ptr loc_0b7f
    jmp near ptr loc_0d56
loc_0cac:
    xor ax, ax
    push ax
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 70h]
    call _lseek
    add sp, 8
    cmp dx, -1
    jne loc_0ce1
    cmp ax, 0ffffh
    jne loc_0ce1
    xor ax, ax
    push ax
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    push cs
    call ___locale_error
    add sp, 8
    jmp short loc_0d56
loc_0ce1:
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    push cs
    call ___find_localecat
    pop cx
    pop cx
    or ax, ax
    jne loc_0d56
    cmp word ptr [bp + 0ah], 7
    jne loc_0d04
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx + 4ch]
    sub ax, 20h
    mov word ptr [bp - 0eh], ax
loc_0d04:
    push ss
    lea ax, [bp - 10h]
    push ax
    push word ptr [bp - 0eh]
    push word ptr [bp - 0ah]
    push word ptr [bp - 0ch]
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 70h]
    call __dos_read
    add sp, 0ch
    or ax, ax
    je loc_0d38
    xor ax, ax
    push ax
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    push cs
    call ___locale_error
    add sp, 8
    jmp short loc_0d56
loc_0d38:
    mov ax, 24h
    push ax
    mov ax, word ptr [bp + 6]
    add ax, 4ch
    push word ptr [bp + 8]
    push ax
    push word ptr [bp - 6]
    push word ptr [bp - 8]
    call _memcpy
    add sp, 0ah
    jmp short loc_0d5b
loc_0d56:
    mov ax, 0ffffh
    jmp short loc_0d5d
loc_0d5b:
    xor ax, ax
loc_0d5d:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original seven-entry locale category search dispatcher.
category_dispatch label word
    dw locale_0b19
    dw locale_0b4b
    dw locale_0b95
    dw locale_0bc7
    dw locale_0bf9
    dw locale_0c2c
    dw locale_0c5f


; Original public locale lifecycle interface +3441.
___read_localeenv:
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    push word ptr DGROUP:__LocaleCatNames+2
    push word ptr DGROUP:__LocaleCatNames
    call _getenv
    pop cx
    pop cx
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    or ax, dx
    jne loc_0dd4
    cmp word ptr [bp + 6], 1
    jl loc_0dbe
    cmp word ptr [bp + 6], 7
    jg loc_0dbe
    mov bx, word ptr [bp + 6]
    mov cl, 2
    shl bx, cl
    push word ptr DGROUP:__LocaleCatNames[bx+2]
    push word ptr DGROUP:__LocaleCatNames[bx]
    call _getenv
    pop cx
    pop cx
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    or ax, dx
    jne loc_0dd4
loc_0dbe:
    push ds
    mov ax,offset DGROUP:env_LANG
    push ax
    call _getenv
    pop cx
    pop cx
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    or ax, dx
    je loc_0de6
loc_0dd4:
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    push word ptr [bp + 6]
    push cs
    call __lsetlocale
    add sp, 6
    jmp short loc_0def
loc_0de6:
    push word ptr [bp + 6]
    call ___set_c_locale
    pop cx
loc_0def:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original public locale lifecycle interface +3573.
___find_localelib:
    push bp
    mov bp, sp
    sub sp, 12ah
    push si
    push di
    xor ax, ax
    push ax
    push ss
    lea ax, [bp - 12ah]
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call _findfirst
    add sp, 0ah
    or ax, ax
    jne loc_0e22
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    jmp near ptr loc_0ed7
loc_0e22:
    push ss
    lea ax, [bp - 0ah]
    push ax
    push ss
    lea ax, [bp - 13h]
    push ax
    push ss
    lea ax, [bp - 55h]
    push ax
    push ss
    lea ax, [bp - 58h]
    push ax
    les bx,dword ptr DGROUP:__argv
    push word ptr es:[bx + 2]
    push word ptr es:[bx]
    call _fnsplit
    push ss
    lea ax, [bp - 5eh]
    push ax
    push ss
    lea ax, [bp - 67h]
    push ax
    push ss
    lea ax, [bp - 0a9h]
    push ax
    push ss
    lea ax, [bp - 0ach]
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call _fnsplit
    add sp, 28h
    push ss
    lea ax, [bp - 5eh]
    push ax
    push ss
    lea ax, [bp - 67h]
    push ax
    push ss
    lea ax, [bp - 55h]
    push ax
    push ss
    lea ax, [bp - 58h]
    push ax
    push ss
    lea ax, [bp - 0feh]
    push ax
    call _fnmerge
    add sp, 14h
    xor ax, ax
    push ax
    push ss
    lea ax, [bp - 12ah]
    push ax
    push ss
    lea ax, [bp - 0feh]
    push ax
    call _findfirst
    add sp, 0ah
    or ax, ax
    jne loc_0ebc
    push ss
    lea ax, [bp - 0feh]
    push ax
    push ds
    mov ax,offset DGROUP:__LocaleLibName
    push ax
    call _strcpy
    add sp, 8
    jmp short loc_0ee4
loc_0ebc:
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call _searchpath
    pop cx
    pop cx
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    or ax, dx
    je loc_0ee8
    push dx
    push word ptr [bp - 4]
loc_0ed7:
    push ds
    mov ax,offset DGROUP:__LocaleLibName
    push ax
    call _strcpy
    add sp, 8
loc_0ee4:
    xor ax, ax
    jmp short loc_0eeb
loc_0ee8:
    mov ax, 0ffffh
loc_0eeb:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original public locale lifecycle interface +3825.
___delete_locale:
    push bp
    mov bp, sp
    push si
    push di
    les bx,dword ptr [bp + 6]
    les bx,dword ptr es:[bx]
    cmp word ptr es:[bx + 24h], 0
    je loc_0f71
    les bx,dword ptr [bp + 6]
    les bx,dword ptr es:[bx]
    mov ax, word ptr es:[bx + 190h]
    or ax, word ptr es:[bx + 192h]
    je loc_0f26
    push word ptr es:[bx + 192h]
    push word ptr es:[bx + 190h]
    call _free
    pop cx
    pop cx
loc_0f26:
    les bx,dword ptr [bp + 6]
    les bx,dword ptr es:[bx]
    mov ax, word ptr es:[bx + 152h]
    or ax, word ptr es:[bx + 154h]
    je loc_0f49
    push word ptr es:[bx + 154h]
    push word ptr es:[bx + 152h]
    call _free
    pop cx
    pop cx
loc_0f49:
    les bx,dword ptr [bp + 6]
    mov ax, word ptr es:[bx]
    or ax, word ptr es:[bx + 2]
    je loc_0f63
    push word ptr es:[bx + 2]
    push word ptr es:[bx]
    call _free
    pop cx
    pop cx
loc_0f63:
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx + 2], 0
    mov word ptr es:[bx], 0
loc_0f71:
    mov ax, 1
    pop di
    pop si
    pop bp
    retf

; Original public locale lifecycle interface +3960.
___dup_locale:
    push bp
    mov bp, sp
    sub sp, 24h
    push si
    push di
    mov ax, 1
    push ax
    mov ax, 99bh
    push ax
    call _calloc
    pop cx
    pop cx
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx + 2], dx
    mov word ptr es:[bx], ax
    mov ax, word ptr es:[bx]
    or ax, word ptr es:[bx + 2]
    jne loc_0fa5
    jmp near ptr loc_11ad
loc_0fa5:
    mov ax, 99bh
    push ax
    les bx,dword ptr [bp + 0ah]
    push word ptr es:[bx + 2]
    push word ptr es:[bx]
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 2]
    push word ptr es:[bx]
    call _memcpy
    add sp, 0ah
    les bx,dword ptr [bp + 6]
    les bx,dword ptr es:[bx]
    mov word ptr es:[bx + 24h], 1
    les bx,dword ptr [bp + 0ah]
    les bx,dword ptr es:[bx]
    cmp word ptr es:[bx + 18eh], 0
    ja loc_0fe2
    jmp near ptr loc_1176
loc_0fe2:
    mov ax, 1
    push ax
    push word ptr es:[bx + 18eh]
    call _calloc
    pop cx
    pop cx
    les bx,dword ptr [bp + 6]
    les bx,dword ptr es:[bx]
    mov word ptr es:[bx + 192h], dx
    mov word ptr es:[bx + 190h], ax
    mov ax, word ptr es:[bx + 190h]
    or ax, word ptr es:[bx + 192h]
    jne loc_101d
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    push cs
    call ___delete_locale
    pop cx
    pop cx
    jmp near ptr loc_11ad
loc_101d:
    les bx,dword ptr [bp + 0ah]
    les bx,dword ptr es:[bx]
    mov word ptr [bp - 2], es
    mov word ptr [bp - 4], bx
    push word ptr es:[bx + 18eh]
    push word ptr es:[bx + 192h]
    push word ptr es:[bx + 190h]
    les bx,dword ptr [bp + 6]
    les bx,dword ptr es:[bx]
    push word ptr es:[bx + 192h]
    push word ptr es:[bx + 190h]
    call _memcpy
    add sp, 0ah
    les bx,dword ptr [bp + 0ah]
    les bx,dword ptr es:[bx]
    mov ax, word ptr es:[bx + 194h]
    or ax, word ptr es:[bx + 196h]
    je loc_10b2
    xor ax, ax
    mov dx, 52h
    push ax
    push dx
    les bx,dword ptr [bp + 0ah]
    les bx,dword ptr es:[bx]
    mov word ptr [bp - 6], es
    mov word ptr [bp - 8], bx
    mov ax, word ptr es:[bx + 194h]
    xor dx, dx
    sub ax, word ptr es:[bx + 190h]
    sbb dx, 0
    push dx
    push ax
    call N_LDIV@
    push ax
    mov ax, 52h
    pop dx
    imul dx
    les bx,dword ptr [bp + 6]
    mov dx, word ptr es:[bx + 2]
    mov word ptr [bp - 0ah], dx
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 0ch], bx
    add ax, bx
    add ax, 190h
    mov es, word ptr [bp - 0ah]
    mov word ptr es:[bx + 196h], dx
    mov word ptr es:[bx + 194h], ax
loc_10b2:
    les bx,dword ptr [bp + 0ah]
    les bx,dword ptr es:[bx]
    mov ax, word ptr es:[bx + 198h]
    or ax, word ptr es:[bx + 19ah]
    je loc_1114
    xor ax, ax
    mov dx, 13h
    push ax
    push dx
    les bx,dword ptr [bp + 0ah]
    les bx,dword ptr es:[bx]
    mov word ptr [bp - 0eh], es
    mov word ptr [bp - 10h], bx
    mov ax, word ptr es:[bx + 198h]
    xor dx, dx
    sub ax, word ptr es:[bx + 190h]
    sbb dx, 0
    push dx
    push ax
    call N_LDIV@
    push ax
    mov ax, 13h
    pop dx
    imul dx
    les bx,dword ptr [bp + 6]
    mov dx, word ptr es:[bx + 2]
    mov word ptr [bp - 12h], dx
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 14h], bx
    add ax, bx
    add ax, 198h
    mov es, word ptr [bp - 12h]
    mov word ptr es:[bx + 19ah], dx
    mov word ptr es:[bx + 198h], ax
loc_1114:
    les bx,dword ptr [bp + 0ah]
    les bx,dword ptr es:[bx]
    mov ax, word ptr es:[bx + 19ch]
    or ax, word ptr es:[bx + 19eh]
    je loc_1176
    xor ax, ax
    mov dx, 16h
    push ax
    push dx
    les bx,dword ptr [bp + 0ah]
    les bx,dword ptr es:[bx]
    mov word ptr [bp - 16h], es
    mov word ptr [bp - 18h], bx
    mov ax, word ptr es:[bx + 19ch]
    xor dx, dx
    sub ax, word ptr es:[bx + 190h]
    sbb dx, 0
    push dx
    push ax
    call N_LDIV@
    push ax
    mov ax, 16h
    pop dx
    imul dx
    les bx,dword ptr [bp + 6]
    mov dx, word ptr es:[bx + 2]
    mov word ptr [bp - 1ah], dx
    mov bx, word ptr es:[bx]
    mov word ptr [bp - 1ch], bx
    add ax, bx
    add ax, 19ch
    mov es, word ptr [bp - 1ah]
    mov word ptr es:[bx + 19eh], dx
    mov word ptr es:[bx + 19ch], ax
loc_1176:
    mov ax, 1
    push ax
    mov ax, 301h
    push ax
    call _calloc
    pop cx
    pop cx
    les bx,dword ptr [bp + 6]
    les bx,dword ptr es:[bx]
    mov word ptr es:[bx + 154h], dx
    mov word ptr es:[bx + 152h], ax
    mov ax, word ptr es:[bx + 152h]
    or ax, word ptr es:[bx + 154h]
    jne loc_11b2
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    push cs
    call ___delete_locale
    pop cx
    pop cx
loc_11ad:
    mov ax, 0ffffh
    jmp short loc_1226
loc_11b2:
    mov ax, 301h
    push ax
    les bx,dword ptr [bp + 0ah]
    les bx,dword ptr es:[bx]
    push word ptr es:[bx + 154h]
    push word ptr es:[bx + 152h]
    les bx,dword ptr [bp + 6]
    les bx,dword ptr es:[bx]
    push word ptr es:[bx + 154h]
    push word ptr es:[bx + 152h]
    call _memcpy
    add sp, 0ah
    les bx,dword ptr [bp + 6]
    les bx,dword ptr es:[bx]
    mov word ptr [bp - 1eh], es
    mov word ptr [bp - 20h], bx
    mov dx, word ptr es:[bx + 154h]
    mov ax, word ptr es:[bx + 152h]
    add ax, 101h
    mov word ptr es:[bx + 158h], dx
    mov word ptr es:[bx + 156h], ax
    les bx,dword ptr [bp + 6]
    les bx,dword ptr es:[bx]
    mov word ptr [bp - 22h], es
    mov word ptr [bp - 24h], bx
    mov dx, word ptr es:[bx + 158h]
    mov ax, word ptr es:[bx + 156h]
    add ax, 100h
    mov word ptr es:[bx + 15ch], dx
    mov word ptr es:[bx + 15ah], ax
    xor ax, ax
loc_1226:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
_DATA segment word public 'DATA'
all_C_locale db 'C;C;C;C;C;C;;',0
literal_C db 'C',0
initial_C_locale db 'C;C;C;C;C;C;;',0
single_C db 'C',0
categories_format db '%s;%s;%s;%s;%s;%s;%s;',0
env_LANG db 'LANG',0
_DATA ends
end
