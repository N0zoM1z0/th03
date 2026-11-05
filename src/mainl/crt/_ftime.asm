; Original Japanese Borland ftime(), with private DOS 21h date/time
; helpers, timezone and daylight adjustment, near 32-bit divide helper.
.8086
extrn __daylight:word
extrn __timezone:dword
extrn _tzset:far
extrn _dostounix:far
extrn __ISDST:near
extrn N_LDIV@:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
; Private far DOS date reader (CX=year, DH=month, DL=day).
dos_read_date proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ah,2ah
    int 21h
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx],cx
    mov word ptr es:[bx+2],dx
    pop di
    pop si
    pop bp
    retf
dos_read_date endp

; Private far DOS time reader (CH=hour, CL=minute, DH=second, DL=1/100).
dos_read_clock proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ah,2ch
    int 21h
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx],cx
    mov word ptr es:[bx+2],dx
    pop di
    pop si
    pop bp
    retf
dos_read_clock endp

public __ftime
__ftime proc far
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    call _tzset
    push ss
    lea ax,[bp-4]
    push ax
    push cs
    call near ptr dos_read_date
    push ss
    lea ax,[bp-8]
    push ax
    push cs
    call near ptr dos_read_clock
    add sp,8
    cmp byte ptr [bp-7],0
    jnz short have_dos_clock
    cmp byte ptr [bp-8],0
    jnz short have_dos_clock
    push ss
    lea ax,[bp-4]
    push ax
    push cs
    call near ptr dos_read_date
    pop cx
    pop cx
have_dos_clock:
    xor ax,ax
    mov dx,60
    push ax
    push dx
    push word ptr DGROUP:__timezone+2
    push word ptr DGROUP:__timezone
    call N_LDIV@
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+6],ax
    cmp word ptr DGROUP:__daylight,0
    jz short no_summer_time
    mov al,[bp-7]
    mov ah,0
    push ax
    mov al,[bp-2]
    cbw
    push ax
    mov al,[bp-1]
    cbw
    push ax
    mov ax,[bp-4]
    add ax,0f84eh
    push ax
    call __ISDST
    or ax,ax
    jz short no_summer_time
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+8],1
    jmp short have_dst_status
no_summer_time:
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+8],0
have_dst_status:
    push ss
    lea ax,[bp-8]
    push ax
    push ss
    lea ax,[bp-4]
    push ax
    call _dostounix
    add sp,8
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+2],dx
    mov word ptr es:[bx],ax
    mov al,[bp-6]
    mov ah,0
    push ax
    mov ax,10
    pop dx
    imul dx
    mov word ptr es:[bx+4],ax
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
__ftime endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
