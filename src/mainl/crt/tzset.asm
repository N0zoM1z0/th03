; Borland DOS TZ initialization and DST calculation original 8086 runtime.
; _tzset handles environment TZ, DBCS/ctype, fallback JST default,
; standard/daylight names, timezone offsets and DOS import helpers.
; __ISDST implements original date/leap-week calculations with monthDay.
; Original actual 48-byte DATA includes month cumulative day words,
; two far BSS name pointers, -32400 JST offset, daylight flag and strings.
; BSS stores two 4-byte names, INITDATA contains a real far initializer.
; All CODE blocks are complete named native instructions in actual
; nonoverlapping original address ranges; no executable byte arrays.
.8086
extrn __ctype:byte
extrn _atol:far
extrn _getenv:far
extrn _memset:far
extrn _strcpy:far
extrn _strlen:far
extrn _strncpy:far
extrn N_LXMUL@:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_INIT_ segment word public 'INITDATA'
_INIT_ ends
DGROUP group _DATA,_BSS
public _tzset,__ISDST,__monthDay,__tzname,__timezone,__daylight
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 09h
    mov ax,offset DGROUP:tz_environment_key
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0Dh
    call _getenv
    pop cx
    pop cx
    mov word ptr [bp-4], dx
    mov word ptr [bp-6], ax
    or ax, dx
    jne short timezone_at_021
    jmp near ptr timezone_use_JST_defaults
timezone_at_021:
    push dx
    push word ptr [bp-6]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 025h
    call _strlen
    pop cx
    pop cx
    cmp ax, 4
    jae short timezone_at_034
    jmp near ptr timezone_use_JST_defaults
timezone_at_034:
    les bx, dword ptr [bp-6]
    mov al, byte ptr es:[bx]
    cbw
    mov bx, ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 03Dh
    mov al,byte ptr DGROUP:[bx+__ctype+1]
    mov ah, 0
    test al, 0ch
    je short timezone_use_JST_defaults
    mov bx, word ptr [bp-6]
    mov al, byte ptr es:[bx+1]
    cbw
    mov bx, ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 051h
    mov al,byte ptr DGROUP:[bx+__ctype+1]
    mov ah, 0
    test al, 0ch
    je short timezone_use_JST_defaults
    mov bx, word ptr [bp-6]
    mov al, byte ptr es:[bx+2]
    cbw
    mov bx, ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 065h
    mov al,byte ptr DGROUP:[bx+__ctype+1]
    mov ah, 0
    test al, 0ch
    je short timezone_use_JST_defaults
    mov bx, word ptr [bp-6]
    cmp byte ptr es:[bx+3], 02dh
    je short timezone_at_08e
    cmp byte ptr es:[bx+3], 02bh
    je short timezone_at_08e
    mov al, byte ptr es:[bx+3]
    cbw
    mov bx, ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 087h
    test byte ptr DGROUP:[bx+__ctype+1],2
    je short timezone_use_JST_defaults
timezone_at_08e:
    les bx, dword ptr [bp-6]
    mov al, byte ptr es:[bx+3]
    cbw
    mov bx, ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 098h
    mov al,byte ptr DGROUP:[bx+__ctype+1]
    mov ah, 0
    test al, 2
    jne short timezone_at_0f2
    mov bx, word ptr [bp-6]
    mov al, byte ptr es:[bx+4]
    cbw
    mov bx, ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0ACh
    mov al,byte ptr DGROUP:[bx+__ctype+1]
    mov ah, 0
    test al, 2
    jne short timezone_at_0f2
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0C9h
    mov ax,offset DGROUP:tz_default_zone
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0D5h
    call _strcpy
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0DBh
    mov ax,offset DGROUP:tz_final_null
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0E7h
    call _strcpy
    add sp, 010h
    jmp near ptr timezone_at_1f6
timezone_at_0f2:
    mov ax, 4
    push ax
    xor ax, ax
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0101h
    call _memset
    mov ax, 3
    push ax
    push word ptr [bp-4]
    push word ptr [bp-6]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0118h
    call _strncpy
    add sp, 012h
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0133h
    call _atol
    pop cx
    pop cx
    push ax
    push dx
    xor dx, dx
    mov ax, 0e10h
    pop cx
    pop bx
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0143h
    call N_LXMUL@
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0167h
    test byte ptr DGROUP:[bx+__ctype+1],0ch
    je short timezone_at_1e4
    mov ax, word ptr [bp-6]
    add ax, word ptr [bp-2]
    push word ptr [bp-4]
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0178h
    call _strlen
    pop cx
    pop cx
    cmp ax, 3
    jb short timezone_at_1f6
    mov bx, word ptr [bp-2]
    mov es, word ptr [bp-4]
    add bx, word ptr [bp-6]
    mov al, byte ptr es:[bx+1]
    cbw
    mov bx, ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0194h
    mov al,byte ptr DGROUP:[bx+__ctype+1]
    mov ah, 0
    test al, 0ch
    je short timezone_at_1f6
    mov bx, word ptr [bp-2]
    add bx, word ptr [bp-6]
    mov al, byte ptr es:[bx+2]
    cbw
    mov bx, ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01ABh
    mov al,byte ptr DGROUP:[bx+__ctype+1]
    mov ah, 0
    test al, 0ch
    je short timezone_at_1f6
    mov ax, 3
    push ax
    mov ax, word ptr [bp-6]
    add ax, word ptr [bp-2]
    push word ptr [bp-4]
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01CBh
    call _strncpy
    add sp, 0ah
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0B6h
timezone_use_JST_defaults:
    mov word ptr DGROUP:__daylight,0
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0BCh
    mov word ptr DGROUP:__timezone+2,0ffffh
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0C2h
    mov word ptr DGROUP:__timezone,08170h
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0CDh
    push word ptr DGROUP:__tzname+2
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0D1h
    push word ptr DGROUP:__tzname
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0DFh
    push word ptr DGROUP:__tzname+6
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0E3h
    push word ptr DGROUP:__tzname+4
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0F9h
    push word ptr DGROUP:__tzname+6
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0FDh
    push word ptr DGROUP:__tzname+4
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0110h
    push word ptr DGROUP:__tzname+2
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0114h
    push word ptr DGROUP:__tzname
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0120h
    les bx,dword ptr DGROUP:__tzname
    mov byte ptr es:[bx+3], 0
    mov ax, word ptr [bp-6]
    add ax, 3
    push word ptr [bp-4]
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0146h
    mov word ptr DGROUP:__timezone+2,dx
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 014Ah
    mov word ptr DGROUP:__timezone,ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 014Dh
    mov word ptr DGROUP:__daylight,0
    mov word ptr [bp-2], 3
    jmp near ptr timezone_at_1e7
timezone_at_15b:
    les bx, dword ptr [bp-6]
    add bx, word ptr [bp-2]
    mov al, byte ptr es:[bx]
    cbw
    mov bx, ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01C3h
    push word ptr DGROUP:__tzname+6
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01C7h
    push word ptr DGROUP:__tzname+4
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01D3h
    les bx,dword ptr DGROUP:__tzname+4
    mov byte ptr es:[bx+3], 0
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01DCh
    mov word ptr DGROUP:__daylight,1
    jmp short timezone_at_1f6
timezone_at_1e4:
    inc word ptr [bp-2]
timezone_at_1e7:
    les bx, dword ptr [bp-6]
    add bx, word ptr [bp-2]
    cmp byte ptr es:[bx], 0
    je short timezone_at_1f6
    jmp near ptr timezone_at_15b
timezone_at_1f6:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0232h
    mov ax,word ptr DGROUP:[bx+__monthDay]
    cmp ax, word ptr [bp-2]
    jbe short timezone_at_22a
    jmp short timezone_at_25d
timezone_at_23d:
    mov bx, word ptr [bp+6]
    dec bx
    add bx, bx
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0243h
    mov ax,word ptr DGROUP:[bx+__monthDay]
    add word ptr [bp+8], ax
    cmp word ptr [bp+6], 3
    jbe short timezone_at_25d
    mov ax, word ptr [bp+4]
    add ax, 046h
    test al, 3
    jne short timezone_at_25d
    inc word ptr [bp+8]
timezone_at_25d:
    cmp word ptr [bp+6], 4
    jb short return_standard_time
    je short timezone_at_26d
    cmp word ptr [bp+6], 0ah
    ja short return_standard_time
    jne short return_in_dst
timezone_at_26d:
    mov bx, word ptr [bp+6]
    shl bx, 1
    cmp word ptr [bp+4], 010h
    jle short timezone_at_287
    cmp word ptr [bp+6], 4
    jne short timezone_at_287
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 027Eh
    mov cx,word ptr DGROUP:[bx+__monthDay-2]
    add cx, 7
    jmp short timezone_at_28b
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0287h
timezone_at_287:
    mov cx,word ptr DGROUP:[bx+__monthDay]
timezone_at_28b:
    mov bx, word ptr [bp+4]
    add bx, 07b2h
    test bl, 3
    je short timezone_at_298
    dec cx
timezone_at_298:
    mov bx, word ptr [bp+4]
    inc bx
    sar bx, 1
    sar bx, 1
    add bx, cx
    mov ax, 016dh
    mul word ptr [bp+4]
    add ax, bx
    add ax, 4
    xor dx, dx
    mov bx, 7
    div bx
    sub cx, dx
    mov ax, word ptr [bp+8]
    cmp word ptr [bp+6], 4
    jne short timezone_at_2cd
    cmp ax, cx
    ja short return_in_dst
    jne short return_standard_time
    cmp byte ptr [bp+0ah], 2
    jb short return_standard_time
    jmp short return_in_dst
timezone_at_2cd:
    cmp ax, cx
    jb short return_in_dst
    jne short return_standard_time
    cmp byte ptr [bp+0ah], 1
    ja short return_standard_time
return_in_dst:
    mov ax, 1
    jmp short timezone_at_2e0
return_standard_time:
    xor ax, ax
timezone_at_2e0:
    pop di
    pop si
    mov sp, bp
    pop bp
    ret 8
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 00h
_tzset label far
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01FCh
__ISDST label near
check_summer_time:
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    cmp word ptr [bp+6], 0
    jne short timezone_at_23d
    mov ax, word ptr [bp+8]
    mov word ptr [bp-2], ax
    cmp word ptr [bp+8], 03bh
    jb short timezone_at_223
    mov ax, word ptr [bp+4]
    add ax, 046h
    test al, 3
    jne short timezone_at_223
    dec word ptr [bp-2]
timezone_at_223:
    mov word ptr [bp+6], 0
    jmp short timezone_at_22d
timezone_at_22a:
    inc word ptr [bp+6]
timezone_at_22d:
    mov bx, word ptr [bp+6]
    add bx, bx
_TEXT ends
_DATA segment word public 'DATA'
__monthDay dw 0,31,59,90,120,151,181,212,243,273,304,334,365
__tzname label dword
    dd DGROUP:tz_buf_standard
    dd DGROUP:tz_buf_daylight
__timezone dd 0FFFF8170h ; original timezone -32400 seconds JST
__daylight dw 0
tz_environment_key db 'TZ',0
tz_default_zone db 'JST',0
tz_final_null db 0
_DATA ends
_BSS segment word public 'BSS'
tz_buf_standard db 4 dup(?)
tz_buf_daylight db 4 dup(?)
_BSS ends
_INIT_ segment word public 'INITDATA'
tzset_initializer db 1,01Eh
    dd _tzset
_INIT_ ends
end
