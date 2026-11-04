; Original Japanese MAINL large-model CRT time conversion / formatting.
; Recovered instruction-level semantics. Symbolic original date names, tm
; and timezone helpers; no embedded original CODE or binary object patches.
; Native CODE/DATA/relocation verification is required before exactness claims.
.8086
extrn __ISDST:near,__daylight:word,__timezone:dword,_tzset:far
extrn _sprintf:far,N_LMOD@:near,N_LDIV@:near,N_LXMUL@:near,N_SCOPY@:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _atime,_gmtime,_localtime,_asctime,_ctime,_mktime

; Internal epoch-seconds to static struct tm conversion.
break_time:
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    cmp word ptr [bp + 8], 0
    jg loc_0020
    jl loc_0016
    cmp word ptr [bp + 6], 0
    jae loc_0020
loc_0016:
    mov word ptr [bp + 8], 0
    mov word ptr [bp + 6], 0
loc_0020:
    xor ax, ax
    mov dx, 3ch
    push ax
    push dx
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call N_LMOD@
    mov word ptr DGROUP:ctime_tm, ax
    xor ax, ax
    mov dx, 3ch
    push ax
    push dx
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call N_LDIV@
    mov word ptr [bp + 8], dx
    mov word ptr [bp + 6], ax
    xor ax, ax
    mov dx, 3ch
    push ax
    push dx
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call N_LMOD@
    mov word ptr DGROUP:ctime_tm+2, ax
    xor ax, ax
    mov dx, 3ch
    push ax
    push dx
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call N_LDIV@
    mov word ptr [bp + 8], dx
    mov word ptr [bp + 6], ax
    xor ax, ax
    mov dx, 88f8h
    push ax
    push dx
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call N_LDIV@
    mov dx, ax
    mov cl, 2
    shl ax, cl
    mov word ptr DGROUP:ctime_tm+10, ax
    add word ptr DGROUP:ctime_tm+10, 46h
    mov ax, 5b5h
    imul dx
    mov word ptr [bp - 2], ax
    xor ax, ax
    mov dx, 88f8h
    push ax
    push dx
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call N_LMOD@
    mov word ptr [bp + 8], dx
    mov word ptr [bp + 6], ax
loc_00ae:
    mov cx, 2238h
    test byte ptr DGROUP:ctime_tm+10, 3
    jne loc_00bb
    add cx, 18h
loc_00bb:
    mov ax, cx
    cwd
    cmp dx, word ptr [bp + 8]
    jl loc_00ca
    jg loc_00e4
    cmp ax, word ptr [bp + 6]
    ja loc_00e4
loc_00ca:
    mov ax, cx
    mov bx, 18h
    cwd
    idiv bx
    add word ptr [bp - 2], ax
    inc word ptr DGROUP:ctime_tm+10
    mov ax, cx
    cwd
    sub word ptr [bp + 6], ax
    sbb word ptr [bp + 8], dx
    jmp short loc_00ae
loc_00e4:
    cmp word ptr [bp + 0ah], 0
    je loc_0134
    cmp word ptr DGROUP:__daylight, 0
    je loc_0134
    xor ax, ax
    mov dx, 18h
    push ax
    push dx
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call N_LMOD@
    push ax
    xor ax, ax
    mov dx, 18h
    push ax
    push dx
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call N_LDIV@
    push ax
    xor ax, ax
    push ax
    mov ax, word ptr DGROUP:ctime_tm+10
    add ax, 0ffbah
    push ax
    call __ISDST
    or ax, ax
    je loc_0134
    add word ptr [bp + 6], 1
    adc word ptr [bp + 8], 0
    mov word ptr DGROUP:ctime_tm+16, 1
    jmp short loc_013a
loc_0134:
    mov word ptr DGROUP:ctime_tm+16, 0
loc_013a:
    xor ax, ax
    mov dx, 18h
    push ax
    push dx
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call N_LMOD@
    mov word ptr DGROUP:ctime_tm+4, ax
    xor ax, ax
    mov dx, 18h
    push ax
    push dx
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call N_LDIV@
    mov word ptr [bp + 8], dx
    mov word ptr [bp + 6], ax
    mov word ptr DGROUP:ctime_tm+14, ax
    add ax, 4
    add word ptr [bp - 2], ax
    mov ax, word ptr [bp - 2]
    mov bx, 7
    xor dx, dx
    div bx
    mov word ptr DGROUP:ctime_tm+12, dx
    add word ptr [bp + 6], 1
    adc word ptr [bp + 8], 0
    test byte ptr DGROUP:ctime_tm+10, 3
    jne loc_01bb
    cmp word ptr [bp + 8], 0
    jl loc_01a1
    jg loc_0197
    cmp word ptr [bp + 6], 3ch
    jbe loc_01a1
loc_0197:
    sub word ptr [bp + 6], 1
    sbb word ptr [bp + 8], 0
    jmp short loc_01bb
loc_01a1:
    cmp word ptr [bp + 8], 0
    jne loc_01bb
    cmp word ptr [bp + 6], 3ch
    jne loc_01bb
    mov word ptr DGROUP:ctime_tm+8, 1
    mov word ptr DGROUP:ctime_tm+6, 1dh
    jmp short loc_01f3
loc_01bb:
    mov word ptr DGROUP:ctime_tm+8, 0
    jmp short loc_01d7
loc_01c3:
    mov bx, word ptr DGROUP:ctime_tm+8
    mov al, byte ptr DGROUP:month_lengths[bx]
    cbw
    cwd
    sub word ptr [bp + 6], ax
    sbb word ptr [bp + 8], dx
    inc word ptr DGROUP:ctime_tm+8
loc_01d7:
    mov bx, word ptr DGROUP:ctime_tm+8
    mov al, byte ptr DGROUP:month_lengths[bx]
    cbw
    cwd
    cmp dx, word ptr [bp + 8]
    jl loc_01c3
    jne loc_01ed
    cmp ax, word ptr [bp + 6]
    jb loc_01c3
loc_01ed:
    mov ax, word ptr [bp + 6]
    mov word ptr DGROUP:ctime_tm+6, ax
loc_01f3:
    mov dx, ds
    mov ax, offset DGROUP:ctime_tm
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Public time conversion interface: _atime
_atime:
    push bp
    mov bp, sp
    push si
    push di
    les bx, dword ptr [bp + 0ah]
    mov ax, word ptr es:[bx + 0ah]
    add ax, 76ch
    push ax
    push word ptr es:[bx]
    push word ptr es:[bx + 2]
    push word ptr es:[bx + 4]
    push word ptr es:[bx + 6]
    mov bx, word ptr es:[bx + 8]
    mov cl, 2
    shl bx, cl
    push word ptr DGROUP:name_table+58[bx]
    push word ptr DGROUP:name_table+56[bx]
    mov bx, word ptr [bp + 0ah]
    mov bx, word ptr es:[bx + 0ch]
    shl bx, cl
    push word ptr DGROUP:name_table+2[bx]
    push word ptr DGROUP:name_table[bx]
    push ds
    mov ax, offset DGROUP:asctime_fmt
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call _sprintf
    add sp, 1ah
    pop di
    pop si
    pop bp
    retf

; Public time conversion interface: _gmtime
_gmtime:
    push bp
    mov bp, sp
    push si
    push di
    xor ax, ax
    push ax
    les bx, dword ptr [bp + 6]
    push word ptr es:[bx + 2]
    push word ptr es:[bx]
    push cs
    call break_time
    add sp, 6
    pop di
    pop si
    pop bp
    retf

; Public time conversion interface: _localtime
_localtime:
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    call _tzset
    les bx, dword ptr [bp + 6]
    mov dx, word ptr es:[bx + 2]
    mov ax, word ptr es:[bx]
    sub ax, word ptr DGROUP:__timezone
    sbb dx, word ptr DGROUP:__timezone+2
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    mov ax, 1
    push ax
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    push cs
    call break_time
    add sp, 6
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Public time conversion interface: _asctime
_asctime:
    push bp
    mov bp, sp
    push si
    push di
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    push ds
    mov ax, offset DGROUP:asctime_text
    push ax
    push cs
    call _atime
    add sp, 8
    mov dx, ax
    mov bx, dx
    mov byte ptr DGROUP:asctime_text[bx], 0ah
    inc dx
    mov bx, dx
    mov byte ptr DGROUP:asctime_text[bx], 0
    mov dx, ds
    mov ax, offset DGROUP:asctime_text
    pop di
    pop si
    pop bp
    retf

; Public time conversion interface: _ctime
_ctime:
    push bp
    mov bp, sp
    push si
    push di
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    push cs
    call _localtime
    pop cx
    pop cx
    push dx
    push ax
    push cs
    call _asctime
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf

; Internal normalized calendar fields to seconds since epoch.
civil_to_epoch:
    push bp
    mov bp, sp
    sub sp, 0ah
    push si
    push di
    cmp word ptr [bp + 4], 46h
    jl loc_0311
    cmp word ptr [bp + 4], 8ah
    jle loc_031a
loc_0311:
    mov dx, 0ffffh
    mov ax, 0ffffh
    jmp near ptr loc_0494
loc_031a:
    mov ax, word ptr [bp + 0eh]
    mov bx, 3ch
    cwd
    idiv bx
    add word ptr [bp + 0ch], ax
    mov ax, word ptr [bp + 0eh]
    cwd
    idiv bx
    mov word ptr [bp + 0eh], dx
    mov ax, word ptr [bp + 0ch]
    cwd
    idiv bx
    add word ptr [bp + 0ah], ax
    mov ax, word ptr [bp + 0ch]
    cwd
    idiv bx
    mov word ptr [bp + 0ch], dx
    mov ax, word ptr [bp + 0ah]
    mov bx, 18h
    cwd
    idiv bx
    add word ptr [bp + 8], ax
    mov ax, word ptr [bp + 0ah]
    cwd
    idiv bx
    mov word ptr [bp + 0ah], dx
    jmp short loc_037e
loc_0358:
    test byte ptr [bp + 4], 3
    jne loc_0370
    cmp word ptr [bp + 6], 1
    jne loc_0370
    cmp word ptr [bp + 8], 1ch
    jle loc_03a0
    sub word ptr [bp + 8], 1dh
    jmp short loc_037b
loc_0370:
    mov bx, word ptr [bp + 6]
    mov al, byte ptr DGROUP:month_lengths[bx]
    cbw
    sub word ptr [bp + 8], ax
loc_037b:
    inc word ptr [bp + 6]
loc_037e:
    mov ax, word ptr [bp + 6]
    mov bx, 0ch
    cwd
    idiv bx
    add word ptr [bp + 4], ax
    mov ax, word ptr [bp + 6]
    cwd
    idiv bx
    mov word ptr [bp + 6], dx
    mov bx, word ptr [bp + 6]
    mov al, byte ptr DGROUP:month_lengths[bx]
    cbw
    cmp ax, word ptr [bp + 8]
    jle loc_0358
loc_03a0:
    sub word ptr [bp + 4], 46h
    mov ax, word ptr [bp + 4]
    add ax, 2
    mov bx, 4
    cwd
    idiv bx
    mov word ptr [bp - 2], ax
    mov ax, word ptr [bp + 4]
    add ax, 46h
    test al, 3
    jne loc_03c6
    cmp word ptr [bp + 6], 2
    jge loc_03c6
    dec word ptr [bp - 2]
loc_03c6:
    mov ax, word ptr [bp + 4]
    cwd
    push ax
    push dx
    xor dx, dx
    mov ax, 16dh
    pop cx
    pop bx
    call N_LXMUL@
    push ax
    mov ax, word ptr [bp - 2]
    push dx
    cwd
    pop bx
    pop cx
    add cx, ax
    adc bx, dx
    mov si, word ptr [bp + 6]
    add si, si
    mov ax, word ptr DGROUP:month_day_offsets[si]
    cwd
    add cx, ax
    adc bx, dx
    mov ax, word ptr [bp + 8]
    cwd
    add cx, ax
    adc bx, dx
    mov word ptr [bp - 4], bx
    mov word ptr [bp - 6], cx
    mov cx, word ptr [bp - 4]
    mov bx, word ptr [bp - 6]
    mov dx, 1
    mov ax, 5180h
    call N_LXMUL@
    push ax
    mov ax, word ptr [bp + 0ah]
    push dx
    cwd
    push ax
    push dx
    xor dx, dx
    mov ax, 0e10h
    pop cx
    pop bx
    call N_LXMUL@
    pop bx
    pop cx
    add cx, ax
    adc bx, dx
    mov ax, word ptr [bp + 0ch]
    cwd
    push cx
    push bx
    push ax
    push dx
    xor dx, dx
    mov ax, 3ch
    pop cx
    pop bx
    call N_LXMUL@
    pop bx
    pop cx
    add cx, ax
    adc bx, dx
    mov ax, word ptr [bp + 0eh]
    cwd
    add cx, ax
    adc bx, dx
    add cx, word ptr DGROUP:__timezone
    adc bx, word ptr DGROUP:__timezone+2
    mov word ptr [bp - 8], bx
    mov word ptr [bp - 0ah], cx
    cmp word ptr DGROUP:__daylight, 0
    je loc_0478
    push word ptr [bp + 0ah]
    push word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    inc ax
    push ax
    push word ptr [bp + 4]
    call __ISDST
    or ax, ax
    je loc_0478
    sub word ptr [bp - 0ah], 0e10h
    sbb word ptr [bp - 8], 0
loc_0478:
    cmp word ptr [bp - 8], 0
    jl loc_048e
    jg loc_0486
    cmp word ptr [bp - 0ah], 0
    jbe loc_048e
loc_0486:
    mov dx, word ptr [bp - 8]
    mov ax, word ptr [bp - 0ah]
    jmp short loc_0494
loc_048e:
    mov dx, 0ffffh
    mov ax, 0ffffh
loc_0494:
    pop di
    pop si
    mov sp, bp
    pop bp
    ret

; Public time conversion interface: _mktime
_mktime:
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    les bx, dword ptr [bp + 6]
    push word ptr es:[bx]
    push word ptr es:[bx + 2]
    push word ptr es:[bx + 4]
    mov ax, word ptr es:[bx + 6]
    dec ax
    push ax
    push word ptr es:[bx + 8]
    push word ptr es:[bx + 0ah]
    call civil_to_epoch
    add sp, 0ch
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    cmp word ptr [bp - 2], -1
    jne loc_04d6
    cmp word ptr [bp - 4], -1
    je loc_04f2
loc_04d6:
    push ss
    lea ax, [bp - 4]
    push ax
    push cs
    call _localtime
    pop cx
    pop cx
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    mov ax, offset DGROUP:ctime_tm
    push ds
    push ax
    mov cx, 12h
    call N_SCOPY@
loc_04f2:
    mov dx, word ptr [bp - 2]
    mov ax, word ptr [bp - 4]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends

; Initialized far name array: 7 abbreviated and 7 full weekdays,
; 12 abbreviated and 12 full months, then two AM/PM markers.
_DATA segment word public 'DATA'
public _SWeekday,_LWeekday,_SMonth,_LMonth,_AmPm
_SWeekday label dword
name_table label dword
    dd day3_Sun
    dd day3_Mon
    dd day3_Tue
    dd day3_Wed
    dd day3_Thu
    dd day3_Fri
    dd day3_Sat
_LWeekday label dword
    dd dayfull_Sunday
    dd dayfull_Monday
    dd dayfull_Tuesday
    dd dayfull_Wednesday
    dd dayfull_Thursday
    dd dayfull_Friday
    dd dayfull_Saturday
_SMonth label dword
    dd mon3_Jan
    dd mon3_Feb
    dd mon3_Mar
    dd mon3_Apr
    dd mon3_May
    dd mon3_Jun
    dd mon3_Jul
    dd mon3_Aug
    dd mon3_Sep
    dd mon3_Oct
    dd mon3_Nov
    dd mon3_Dec
_LMonth label dword
    dd monfull_January
    dd monfull_February
    dd monfull_March
    dd monfull_April
    dd monfull_May
    dd monfull_June
    dd monfull_July
    dd monfull_August
    dd monfull_September
    dd monfull_October
    dd monfull_November
    dd monfull_December
_AmPm label dword
    dd ampm_AM
    dd ampm_PM
month_lengths db 31,28,31,30,31,30,31,31,30,31,30,31
month_day_offsets dw 0,31,59,90,120,151,181,212,243,273,304,334
day3_Sun db 'Sun',0
day3_Mon db 'Mon',0
day3_Tue db 'Tue',0
day3_Wed db 'Wed',0
day3_Thu db 'Thu',0
day3_Fri db 'Fri',0
day3_Sat db 'Sat',0
dayfull_Sunday db 'Sunday',0
dayfull_Monday db 'Monday',0
dayfull_Tuesday db 'Tuesday',0
dayfull_Wednesday db 'Wednesday',0
dayfull_Thursday db 'Thursday',0
dayfull_Friday db 'Friday',0
dayfull_Saturday db 'Saturday',0
mon3_Jan db 'Jan',0
mon3_Feb db 'Feb',0
mon3_Mar db 'Mar',0
mon3_Apr db 'Apr',0
mon3_May db 'May',0
mon3_Jun db 'Jun',0
mon3_Jul db 'Jul',0
mon3_Aug db 'Aug',0
mon3_Sep db 'Sep',0
mon3_Oct db 'Oct',0
mon3_Nov db 'Nov',0
mon3_Dec db 'Dec',0
monfull_January db 'January',0
monfull_February db 'February',0
monfull_March db 'March',0
monfull_April db 'April',0
monfull_May db 'May',0
monfull_June db 'June',0
monfull_July db 'July',0
monfull_August db 'August',0
monfull_September db 'September',0
monfull_October db 'October',0
monfull_November db 'November',0
monfull_December db 'December',0
ampm_AM db 'AM',0
ampm_PM db 'PM',0
asctime_fmt db '%s %s %02d %02d:%02d:%02d %4d',0
_DATA ends
_BSS segment word public 'BSS'
asctime_text db 26 dup (?)
ctime_tm dw 9 dup (?)
_BSS ends
end
