; Original Borland large-model utime. Convert 32-bit epoch/tz fields
; to DOS calendar/time and update a file via native DOS service ABI.
; Real symbolic month lengths and near 32-bit arithmetic helpers.
.8086
extrn __ISDST:near,__dos_close:far,__dos_getdate:far,__dos_gettime:far
extrn __dos_open:far,__dos_setftime:far,__daylight:word,__timezone:dword
extrn _tzset:far,N_LMOD@:near,N_LDIV@:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _utime

; Far entry with caller file path and optional times pointer.
_utime:
    push bp
    mov bp, sp
    sub sp, 16h
    push si
    push di
    push ss
    lea ax, [bp - 16h]
    push ax
    mov ax, 2
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call __dos_open
    add sp, 0ah
    or ax, ax
    je loc_0029
    mov ax, 0ffffh
    jmp near ptr loc_0288
loc_0029:
    mov ax, word ptr [bp + 0ah]
    or ax, word ptr [bp + 0ch]
    jne loc_004b
    push ss
    lea ax, [bp - 0ah]
    push ax
    call __dos_getdate
    push ss
    lea ax, [bp - 0eh]
    push ax
    call __dos_gettime
    add sp, 8
    jmp near ptr loc_0220

; Local epoch conversion and timezone/daylight normalization.
loc_004b:
    les bx,dword ptr [bp + 0ah]
    mov dx, word ptr es:[bx + 6]
    mov ax, word ptr es:[bx + 4]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    call _tzset
    mov dx, word ptr DGROUP:__timezone+2
    mov ax, word ptr DGROUP:__timezone
    add ax, 0a600h
    adc dx, 12ceh
    sub word ptr [bp - 4], ax
    sbb word ptr [bp - 2], dx
    xor ax, ax
    mov dx, 3ch
    push ax
    push dx
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    call N_LMOD@
    mov byte ptr [bp - 0ch], al
    xor ax, ax
    mov dx, 3ch
    push ax
    push dx
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    call N_LDIV@
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    xor ax, ax
    mov dx, 3ch
    push ax
    push dx
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    call N_LMOD@
    mov byte ptr [bp - 0dh], al
    xor ax, ax
    mov dx, 3ch
    push ax
    push dx
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    call N_LDIV@
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    xor ax, ax
    mov dx, 88f8h
    push ax
    push dx
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    call N_LDIV@
    mov cl, 2
    shl ax, cl
    add ax, 7bch
    mov word ptr [bp - 8], ax
    xor ax, ax
    mov dx, 88f8h
    push ax
    push dx
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    call N_LMOD@
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    cmp word ptr [bp - 2], 0
    jl loc_013b
    jne loc_0106
    cmp word ptr [bp - 4], 2250h
    jb loc_013b
loc_0106:
    sub word ptr [bp - 4], 2250h
    sbb word ptr [bp - 2], 0
    inc word ptr [bp - 8]
    xor ax, ax
    mov dx, 2238h
    push ax
    push dx
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    call N_LDIV@
    add word ptr [bp - 8], ax
    xor ax, ax
    mov dx, 2238h
    push ax
    push dx
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    call N_LMOD@
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
loc_013b:
    cmp word ptr DGROUP:__daylight, 0
    je loc_017d
    xor ax, ax
    mov dx, 18h
    push ax
    push dx
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    call N_LMOD@
    push ax
    xor ax, ax
    mov dx, 18h
    push ax
    push dx
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    call N_LDIV@
    push ax
    xor ax, ax
    push ax
    mov ax, word ptr [bp - 8]
    sub ax, 7b2h
    push ax
    call __ISDST
    or ax, ax
    je loc_017d
    add word ptr [bp - 4], 1
    adc word ptr [bp - 2], 0
loc_017d:
    xor ax, ax
    mov dx, 18h
    push ax
    push dx
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    call N_LMOD@
    mov byte ptr [bp - 0eh], al
    xor ax, ax
    mov dx, 18h
    push ax
    push dx
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    call N_LDIV@
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    add word ptr [bp - 4], 1
    adc word ptr [bp - 2], 0
    test byte ptr [bp - 8], 3
    jne loc_01e2
    cmp word ptr [bp - 2], 0
    jl loc_01cc
    jg loc_01c2
    cmp word ptr [bp - 4], 3ch
    jbe loc_01cc
loc_01c2:
    sub word ptr [bp - 4], 1
    sbb word ptr [bp - 2], 0
    jmp short loc_01e2
loc_01cc:
    cmp word ptr [bp - 2], 0
    jne loc_01e2
    cmp word ptr [bp - 4], 3ch
    jne loc_01e2
    mov byte ptr [bp - 9], 2
    mov byte ptr [bp - 0ah], 1dh
    jmp short loc_0220
loc_01e2:
    mov byte ptr [bp - 9], 0
    jmp short loc_01fe
loc_01e8:
    mov al, byte ptr [bp - 9]
    mov ah, 0
    mov bx, ax
    mov al, byte ptr DGROUP:month_lengths[bx]
    cbw
    cwd
    sub word ptr [bp - 4], ax
    sbb word ptr [bp - 2], dx
    inc byte ptr [bp - 9]
loc_01fe:
    mov al, byte ptr [bp - 9]
    mov ah, 0
    mov bx, ax
    mov al, byte ptr DGROUP:month_lengths[bx]
    cbw
    cwd
    cmp dx, word ptr [bp - 2]
    jl loc_01e8
    jne loc_0217
    cmp ax, word ptr [bp - 4]
    jb loc_01e8
loc_0217:
    inc byte ptr [bp - 9]
    mov al, byte ptr [bp - 4]
    mov byte ptr [bp - 0ah], al

; Use DOS system date/time for absent time pointer.
loc_0220:
    mov al, byte ptr [bp - 0ch]
    mov ah, 0
    shr ax, 1
    mov dl, byte ptr [bp - 0dh]
    mov dh, 0
    mov cl, 5
    shl dx, cl
    or ax, dx
    mov dl, byte ptr [bp - 0eh]
    mov dh, 0
    mov cl, 0bh
    shl dx, cl
    or ax, dx
    mov word ptr [bp - 12h], ax
    mov al, byte ptr [bp - 0ah]
    mov ah, 0
    mov dl, byte ptr [bp - 9]
    mov dh, 0
    mov cl, 5
    shl dx, cl
    or ax, dx
    mov dx, word ptr [bp - 8]
    sub dx, 7bch
    mov cl, 9
    shl dx, cl
    or ax, dx
    mov word ptr [bp - 10h], ax
    push word ptr [bp - 12h]
    push ax
    push word ptr [bp - 16h]
    call __dos_setftime
    add sp, 6
    mov word ptr [bp - 14h], ax
    push word ptr [bp - 16h]
    call __dos_close
    pop cx
    cmp word ptr [bp - 14h], 0
    jne loc_0285
    xor ax, ax
    jmp short loc_0288
loc_0285:
    mov ax, 0ffffh
loc_0288:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
_DATA segment word public 'DATA'
month_lengths db 31,28,31,30,31,30,31,31,30,31,30,31
_DATA ends
end
