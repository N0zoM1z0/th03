; Selected Japanese Borland CRT locale initialization/destruction boss.
; Original near/global locale ownership, far allocations and category
; dispatch are reconstructed as real 8086 instructions and labels.
.8086
extrn _sprintf:far,_calloc:far,_free:far,_memcpy:far,_strcmp:far,_strxfrm:far
extrn __ctype:byte,_localeconv:far,__Clocale:byte,__pLocale:dword,__lower:byte,__upper:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public ___initialize_locale,___uninitialize_locale,___set_c_locale

; Original locale lifecycle entry at CODE+0.
___initialize_locale:
    push si
    push di
    les bx,dword ptr DGROUP:__pLocale
    cmp word ptr es:[bx + 24h], 1
    jne loc_0010
    jmp near ptr loc_00b0
loc_0010:
    mov ax, 1
    push ax
    mov ax, 99bh
    push ax
    call _calloc
    pop cx
    pop cx
    mov word ptr DGROUP:__pLocale+2, dx
    mov word ptr DGROUP:__pLocale, ax
    or ax, word ptr DGROUP:__pLocale+2
    jne loc_0038
    mov word ptr DGROUP:__pLocale+2, ds
    mov word ptr DGROUP:__pLocale,offset DGROUP:__Clocale
    jmp short loc_0070
loc_0038:
    les bx,dword ptr DGROUP:__pLocale
    mov word ptr es:[bx + 24h], 1
    mov ax, 1
    push ax
    mov ax, 301h
    push ax
    call _calloc
    pop cx
    pop cx
    les bx,dword ptr DGROUP:__pLocale
    mov word ptr es:[bx + 154h], dx
    mov word ptr es:[bx + 152h], ax
    mov ax, word ptr es:[bx + 152h]
    or ax, word ptr es:[bx + 154h]
    jne loc_0075
    assume cs:NOTHING
    call far ptr ___uninitialize_locale
    assume cs:_TEXT
loc_0070:
    mov ax, 0ffffh
    jmp short loc_00b2
loc_0075:
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
    xor ax, ax
    push ax
    assume cs:NOTHING
    call far ptr ___set_c_locale
    assume cs:_TEXT
    pop cx
loc_00b0:
    xor ax, ax
loc_00b2:
    pop di
    pop si
    retf

; Original locale lifecycle entry at CODE+181.
___uninitialize_locale:
    push si
    push di
    les bx,dword ptr DGROUP:__pLocale
    cmp word ptr es:[bx + 24h], 0
    je loc_0126
    les bx,dword ptr DGROUP:__pLocale
    mov ax, word ptr es:[bx + 190h]
    or ax, word ptr es:[bx + 192h]
    je loc_00e3
    push word ptr es:[bx + 192h]
    push word ptr es:[bx + 190h]
    call _free
    pop cx
    pop cx
loc_00e3:
    les bx,dword ptr DGROUP:__pLocale
    mov ax, word ptr es:[bx + 152h]
    or ax, word ptr es:[bx + 154h]
    je loc_0104
    push word ptr es:[bx + 154h]
    push word ptr es:[bx + 152h]
    call _free
    pop cx
    pop cx
loc_0104:
    mov ax, word ptr DGROUP:__pLocale
    or ax, word ptr DGROUP:__pLocale+2
    je loc_011c
    push word ptr DGROUP:__pLocale+2
    push word ptr DGROUP:__pLocale
    call _free
    pop cx
    pop cx
loc_011c:
    mov word ptr DGROUP:__pLocale+2, ds
    mov word ptr DGROUP:__pLocale,offset DGROUP:__Clocale
loc_0126:
    mov ax, 1
    pop di
    pop si
    retf

; Original locale lifecycle entry at CODE+300.
___set_c_locale:
    push bp
    mov bp, sp
    sub sp, 8
    push si
    push di
    mov word ptr [bp - 6], 0
    mov word ptr [bp - 8], 0
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 2], ax
    mov word ptr [bp - 4], 1
    cmp word ptr [bp + 6], 0
    je loc_0152
    jmp near ptr loc_0313
loc_0152:
    mov word ptr [bp - 4], 6
    inc word ptr [bp - 2]
    jmp near ptr loc_0313
loc_015d:
    mov bx, word ptr [bp - 2]
    inc word ptr [bp - 2]
    dec bx
    cmp bx, 6
    jbe loc_016c
    jmp near ptr loc_0309
loc_016c:
    add bx, bx
    jmp word ptr cs:[bx+locale_dispatch]
loc_0173:
    mov ax, 32h
    push ax
    push ds
    mov ax,offset DGROUP:__Clocale+350
    push ax
    mov ax, word ptr DGROUP:__pLocale
    add ax, 15eh
    push word ptr DGROUP:__pLocale+2
    push ax
    call _memcpy
    add sp, 0ah
    les bx,dword ptr DGROUP:__pLocale
    mov word ptr es:[bx + 1a2h], seg _strcmp
    mov word ptr es:[bx + 1a0h], offset _strcmp
    mov word ptr es:[bx + 1a6h], seg _strxfrm
    mov word ptr es:[bx + 1a4h], offset _strxfrm
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 160h
    jmp short loc_0235
loc_01bb:
    mov ax, 24h
    push ax
    push ds
    mov ax,offset DGROUP:__Clocale+302
    push ax
    mov ax, word ptr DGROUP:__pLocale
    add ax, 12eh
    push word ptr DGROUP:__pLocale+2
    push ax
    call _memcpy
    mov ax, 101h
    push ax
    push ds
    mov ax,offset DGROUP:__ctype
    push ax
    les bx,dword ptr DGROUP:__pLocale
    push word ptr es:[bx + 154h]
    push word ptr es:[bx + 152h]
    call _memcpy
    mov ax, 100h
    push ax
    push ds
    mov ax,offset DGROUP:__lower
    push ax
    les bx,dword ptr DGROUP:__pLocale
    push word ptr es:[bx + 158h]
    push word ptr es:[bx + 156h]
    call _memcpy
    mov ax, 100h
    push ax
    push ds
    mov ax,offset DGROUP:__upper
    push ax
    les bx,dword ptr DGROUP:__pLocale
    push word ptr es:[bx + 15ch]
    push word ptr es:[bx + 15ah]
    call _memcpy
    add sp, 28h
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 130h
loc_0235:
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
    jmp near ptr loc_0313
loc_023e:
    mov ax, 4ch
    push ax
    push ds
    mov ax,offset DGROUP:__Clocale+424
    push ax
    mov ax, word ptr DGROUP:__pLocale
    add ax, 1a8h
    push word ptr DGROUP:__pLocale+2
    push ax
    call _memcpy
    add sp, 0ah
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 1aah
    jmp short loc_0235
loc_0266:
    mov ax, 44h
    push ax
    push ds
    mov ax,offset DGROUP:__Clocale+500
    push ax
    mov ax, word ptr DGROUP:__pLocale
    add ax, 1f4h
    push word ptr DGROUP:__pLocale+2
    push ax
    call _memcpy
    add sp, 0ah
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 1f6h
    jmp short loc_0235
loc_028e:
    mov ax, 709h
    push ax
    push ds
    mov ax,offset DGROUP:__Clocale+568
    push ax
    mov ax, word ptr DGROUP:__pLocale
    add ax, 238h
    push word ptr DGROUP:__pLocale+2
    push ax
    call _memcpy
    add sp, 0ah
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 23ah
    jmp near ptr loc_0235
loc_02b7:
    mov ax, 2eh
    push ax
    push ds
    mov ax,offset DGROUP:__Clocale+2369
    push ax
    mov ax, word ptr DGROUP:__pLocale
    add ax, 941h
    push word ptr DGROUP:__pLocale+2
    push ax
    call _memcpy
    add sp, 0ah
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 943h
    jmp near ptr loc_0235
loc_02e0:
    mov ax, 28h
    push ax
    push ds
    mov ax,offset DGROUP:__Clocale+2415
    push ax
    mov ax, word ptr DGROUP:__pLocale
    add ax, 96fh
    push word ptr DGROUP:__pLocale+2
    push ax
    call _memcpy
    add sp, 0ah
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 971h
    jmp near ptr loc_0235
loc_0309:
    mov word ptr [bp - 6], 0
    mov word ptr [bp - 8], 0
loc_0313:
    mov ax, word ptr [bp - 4]
    dec word ptr [bp - 4]
    or ax, ax
    je loc_0320
    jmp near ptr loc_015d
loc_0320:
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
    mov ax,offset DGROUP:locale_name_format
    push ax
    mov ax, word ptr DGROUP:__pLocale
    add ax, 4eh
    push word ptr DGROUP:__pLocale+2
    push ax
    call _sprintf
    add sp, 24h
    call _localeconv
    cmp word ptr [bp + 6], 0
    jne loc_039c
    mov dx, word ptr DGROUP:__pLocale+2
    mov ax, word ptr DGROUP:__pLocale
    add ax, 4eh
    jmp short loc_03a2
loc_039c:
    mov dx, word ptr [bp - 6]
    mov ax, word ptr [bp - 8]
loc_03a2:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
locale_dispatch label word
    dw loc_0173
    dw loc_01bb
    dw loc_023e
    dw loc_0266
    dw loc_028e
    dw loc_02b7
    dw loc_02e0
_TEXT ends
_DATA segment word public 'DATA'
locale_name_format db '%s;%s;%s;%s;%s;%s;%s;',0
_DATA ends
_EXIT_ segment word public 'EXITDATA'
    db 1,14h
    dd ___uninitialize_locale
_EXIT_ ends
end
