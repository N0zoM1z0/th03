; Original Borland DOS time setter/getter. Call the actual Borland
; DOS/Unix converters; preserve sampling at date rollovers.
.8086
extrn _dostounix:far
extrn _getdate:far
extrn _gettime:far
extrn _setdate:far
extrn _settime:far
extrn _unixtodos:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _stime,_time

_stime proc far
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    push ss
    lea ax,[bp-8]
    push ax
    push ss
    lea ax,[bp-4]
    push ax
    les bx,dword ptr [bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    call _unixtodos
    push ss
    lea ax,[bp-4]
    push ax
    call _setdate
    push ss
    lea ax,[bp-8]
    push ax
    call _settime
    add sp,14h
    xor ax,ax
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_stime endp

_time proc far
    push bp
    mov bp,sp
    sub sp,10h
    push si
    push di
get_stable_date:
    push ss
    lea ax,[bp-4]
    push ax
    call _getdate
    push ss
    lea ax,[bp-8]
    push ax
    call _gettime
    push ss
    lea ax,[bp-10h]
    push ax
    call _getdate
    add sp,0ch
    mov al,byte ptr [bp-2]
    cmp al,byte ptr [bp-0eh]
    jne short get_stable_date
    push ss
    lea ax,[bp-8]
    push ax
    push ss
    lea ax,[bp-4]
    push ax
    call _dostounix
    add sp,8
    mov [bp-0ah],dx
    mov [bp-0ch],ax
    mov ax,[bp+6]
    or ax,[bp+8]
    je short return_time
    les bx,dword ptr [bp+6]
    mov ax,[bp-0ch]
    mov word ptr es:[bx+2],dx
    mov word ptr es:[bx],ax
return_time:
    mov dx,[bp-0ah]
    mov ax,[bp-0ch]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_time endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
