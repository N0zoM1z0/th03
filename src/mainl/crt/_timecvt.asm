; Original Borland DOS large-model time conversion runtime.
; __dostounix converts DOS date/time far pointer to 32-bit time_t;
; __unixtodos converts time_t into far DOS timestamp fields.
; Preserve leap-years, timezone/DST adjustments, long arithmetic
; using real N_LXMUL/N_LDIV/N_LMOD and 12 real month-day DATA bytes.
; Original fixed ABI, far pointers, 16-bit signed/unsigned branches.
; Semantic control flow and DATA symbols, never original CODE bytes.
.8086
extrn __ISDST:near
extrn __daylight:word
extrn __timezone:dword
extrn _tzset:far
extrn N_LXMUL@:near
extrn N_LMOD@:near
extrn N_LDIV@:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
; Original 12 initialized month lengths, non-leap year.
month_lengths db 31,28,31,30,31,30,31,31,30,31,30,31
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
public __dostounix,__unixtodos
; Disjoint semantic blocks emitted in original BCC descending FIXUPP
; writer order. Each ORG is an actual original instruction boundary.
; These directives do not emit or pad executable bytes.
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0310h
read_next_month_length:
    mov al,byte ptr DGROUP:[bx+month_lengths]
    cbw
    cwd
    cmp dx, word ptr [bp+8]
    jl short time_at_2e9
    jne short time_at_322
    cmp ax, word ptr [bp+6]
    jb short time_at_2e9
time_at_322:
    les bx, dword ptr [bp+0ah]
    inc byte ptr es:[bx+3]
    mov al, byte ptr [bp+6]
    mov byte ptr es:[bx+2], al
time_at_330:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 02F3h
read_month_length:
    mov al,byte ptr DGROUP:[bx+month_lengths]
    cbw
    cwd
    sub word ptr [bp+6], ax
    sbb word ptr [bp+8], dx
    mov bx, word ptr [bp+0ah]
    inc byte ptr es:[bx+3]
time_at_306:
    les bx, dword ptr [bp+0ah]
    mov al, byte ptr es:[bx+3]
    cbw
    mov bx, ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0292h
    call N_LDIV@
    mov word ptr [bp+8], dx
    mov word ptr [bp+6], ax
    add word ptr [bp+6], 1
    adc word ptr [bp+8], 0
    les bx, dword ptr [bp+0ah]
    test byte ptr es:[bx], 3
    jne short time_at_2df
    cmp word ptr [bp+8], 0
    jl short time_at_2c4
    jg short time_at_2ba
    cmp word ptr [bp+6], 03ch
    jbe short time_at_2c4
time_at_2ba:
    sub word ptr [bp+6], 1
    sbb word ptr [bp+8], 0
    jmp short time_at_2df
time_at_2c4:
    cmp word ptr [bp+8], 0
    jne short time_at_2df
    cmp word ptr [bp+6], 03ch
    jne short time_at_2df
    les bx, dword ptr [bp+0ah]
    mov byte ptr es:[bx+3], 2
    mov byte ptr es:[bx+2], 01dh
    jmp short time_at_330
time_at_2df:
    les bx, dword ptr [bp+0ah]
    mov byte ptr es:[bx+3], 0
    jmp short time_at_306
time_at_2e9:
    les bx, dword ptr [bp+0ah]
    mov al, byte ptr es:[bx+3]
    cbw
    mov bx, ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 027Bh
    call N_LMOD@
    les bx, dword ptr [bp+0eh]
    mov byte ptr es:[bx+1], al
    xor ax, ax
    mov dx, 018h
    push ax
    push dx
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 025Fh
    call __ISDST
    or ax, ax
    je short time_at_26e
    add word ptr [bp+6], 1
    adc word ptr [bp+8], 0
time_at_26e:
    xor ax, ax
    mov dx, 018h
    push ax
    push dx
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 024Eh
    call N_LDIV@
    push ax
    xor ax, ax
    push ax
    les bx, dword ptr [bp+0ah]
    mov ax, word ptr es:[bx]
    add ax, 0f84eh
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 023Dh
    call N_LMOD@
    push ax
    xor ax, ax
    mov dx, 018h
    push ax
    push dx
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0229h
time_at_229:
    cmp word ptr DGROUP:__daylight,0
    je short time_at_26e
    xor ax, ax
    mov dx, 018h
    push ax
    push dx
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0220h
    call N_LMOD@
check_DST_conversion:
    mov word ptr [bp+8], dx
    mov word ptr [bp+6], ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 020Ah
    call N_LDIV@
    les bx, dword ptr [bp+0ah]
    add word ptr es:[bx], ax
    xor ax, ax
    mov dx, 02238h
    push ax
    push dx
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01D6h
    call N_LMOD@
    mov word ptr [bp+8], dx
    mov word ptr [bp+6], ax
    cmp word ptr [bp+8], 0
    jl short time_at_229
    jne short time_at_1ee
    cmp word ptr [bp+6], 02250h
    jb short time_at_229
time_at_1ee:
    sub word ptr [bp+6], 02250h
    sbb word ptr [bp+8], 0
    les bx, dword ptr [bp+0ah]
    inc word ptr es:[bx]
    xor ax, ax
    mov dx, 02238h
    push ax
    push dx
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01B9h
    call N_LDIV@
    mov cl, 2
    shl ax, cl
    add ax, 07bch
    les bx, dword ptr [bp+0ah]
    mov word ptr es:[bx], ax
    xor ax, ax
    mov dx, 088f8h
    push ax
    push dx
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01A3h
    call N_LDIV@
    mov word ptr [bp+8], dx
    mov word ptr [bp+6], ax
    xor ax, ax
    mov dx, 088f8h
    push ax
    push dx
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 018Dh
    call N_LMOD@
    les bx, dword ptr [bp+0eh]
    mov byte ptr es:[bx], al
    xor ax, ax
    mov dx, 03ch
    push ax
    push dx
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0177h
    call N_LDIV@
    mov word ptr [bp+8], dx
    mov word ptr [bp+6], ax
    xor ax, ax
    mov dx, 03ch
    push ax
    push dx
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0160h
month_from_days:
    call N_LMOD@
    les bx, dword ptr [bp+0eh]
    mov byte ptr es:[bx+3], al
    xor ax, ax
    mov dx, 03ch
    push ax
    push dx
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 013Bh
    mov ax,word ptr DGROUP:__timezone
    add ax, 0a600h
    adc dx, 012ceh
    sub word ptr [bp+6], ax
    sbb word ptr [bp+8], dx
    les bx, dword ptr [bp+0eh]
    mov byte ptr es:[bx+2], 0
    xor ax, ax
    mov dx, 03ch
    push ax
    push dx
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0137h
load_timezone_offset:
    mov dx,word ptr DGROUP:__timezone+2
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0132h
    call _tzset
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 012Dh
__unixtodos label far
    push bp
    mov bp, sp
    push si
    push di
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 010Ah
    call N_LXMUL@
    les bx, dword ptr [bp+0ah]
    mov bl, byte ptr es:[bx+3]
    mov bh, 0
    add ax, bx
    adc dx, 0
    add word ptr [bp-4], ax
    adc word ptr [bp-2], dx
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    pop di
    pop si
    mov sp, bp
    pop bp
return_unix_time:
    retf
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0F0h
    call N_LXMUL@
    add word ptr [bp-4], ax
    adc word ptr [bp-2], dx
    les bx, dword ptr [bp+0ah]
    mov al, byte ptr es:[bx]
    mov ah, 0
    xor cx, cx
    xor dx, dx
    push ax
    mov ax, 03ch
    pop bx
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0D9h
    call __ISDST
    or ax, ax
    je short add_hour_seconds
    dec word ptr [bp-8]
add_hour_seconds:
    mov ax, word ptr [bp-8]
    cwd
    push ax
    push dx
    xor dx, dx
    mov ax, 0e10h
    pop cx
    pop bx
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0BDh
    cmp word ptr DGROUP:__daylight,0
    je short add_hour_seconds
convert_dst_rule:
    mov al, byte ptr es:[bx+1]
    mov ah, 0
    push ax
    push cx
    xor ax, ax
    push ax
    les bx, dword ptr [bp+6]
    mov ax, word ptr es:[bx]
    add ax, 0f84eh
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 084h
    mov al,byte ptr DGROUP:[bx+month_lengths]
    cbw
    add cx, ax
check_next_month:
    cmp word ptr [bp-6], 0
    jg short add_previous_month
    les bx, dword ptr [bp+6]
    mov al, byte ptr es:[bx+2]
    cbw
    dec ax
    add cx, ax
    cmp byte ptr es:[bx+3], 2
    jle short calculate_total_hours
    test byte ptr es:[bx], 3
    jne short calculate_total_hours
    inc cx
calculate_total_hours:
    mov ax, 018h
    imul cx
    les bx, dword ptr [bp+0ah]
    mov dl, byte ptr es:[bx+1]
    mov dh, 0
    add ax, dx
    mov word ptr [bp-8], ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 056h
    call N_LXMUL@
    add word ptr [bp-4], ax
    adc word ptr [bp-2], dx
    test byte ptr [bp-6], 3
    je short sum_prior_months
    add word ptr [bp-4], 05180h
    adc word ptr [bp-2], 1
sum_prior_months:
    xor cx, cx
    les bx, dword ptr [bp+6]
    mov al, byte ptr es:[bx+3]
    cbw
    dec ax
    mov word ptr [bp-6], ax
    jmp short check_next_month
add_previous_month:
    dec word ptr [bp-6]
    mov bx, word ptr [bp-6]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 03Ch
    call N_LXMUL@
    add word ptr [bp-4], ax
    adc word ptr [bp-2], dx
    mov ax, word ptr [bp-6]
    and ax, 3
    cwd
    push ax
    push dx
    mov dx, 01e1h
    mov ax, 03380h
    pop cx
    pop bx
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 011h
    mov ax,word ptr DGROUP:__timezone
    add ax, 0a600h
    adc dx, 012ceh
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    les bx, dword ptr [bp+6]
    mov ax, word ptr es:[bx]
    add ax, 0f844h
    mov word ptr [bp-6], ax
    mov cl, 2
    sar ax, cl
    cwd
    push ax
    push dx
    mov dx, 0786h
    mov ax, 01f80h
    pop cx
    pop bx
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0Dh
    mov dx,word ptr DGROUP:__timezone+2
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 08h
    call _tzset
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 00h
__dostounix label far
    push bp
    mov bp, sp
    sub sp, 8
    push si
    push di
_TEXT ends
end
