; Complete Borland large-model __strdate / __strtime formatting member.
; One genuine near Pascal-cleanup ASCII two-digit formatter shared by both
; public far CRT entry points; DOS date and time structs are stack-local.
.8086
extrn __dos_getdate:far,__dos_gettime:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

; Arguments (near): delimiter, first number, second number, third number,
; destination far pointer. In the date path caller supplies year-1900,month,
; day. In time path it supplies hour,minute,second. One unused return slot
; must retain its original 16-bit BP stack layout.
format_three_fields proc near
    push bp
    mov bp,sp
    push si
    push di
    mov cx,[bp+10]
    les bx,dword ptr [bp+12]
    mov al,[bp+4]
    mov byte ptr es:[bx+5],al
    mov byte ptr es:[bx+2],al
    mov byte ptr es:[bx+8],0
    mov ax,cx
    mov bx,10
    cwd
    idiv bx
    cwd
    idiv bx
    add dl,'0'
    mov bx,[bp+12]
    mov es:[bx],dl
    mov ax,cx
    mov bx,10
    cwd
    idiv bx
    add dl,'0'
    mov bx,[bp+12]
    mov es:[bx+1],dl
    mov ax,[bp+8]
    mov bx,10
    cwd
    idiv bx
    cwd
    idiv bx
    add dl,'0'
    mov bx,[bp+12]
    mov es:[bx+3],dl
    mov ax,[bp+8]
    mov bx,10
    cwd
    idiv bx
    add dl,'0'
    mov bx,[bp+12]
    mov es:[bx+4],dl
    mov ax,[bp+6]
    mov bx,10
    cwd
    idiv bx
    cwd
    idiv bx
    add dl,'0'
    mov bx,[bp+12]
    mov es:[bx+6],dl
    mov ax,[bp+6]
    mov bx,10
    cwd
    idiv bx
    add dl,'0'
    mov bx,[bp+12]
    mov es:[bx+7],dl
    mov dx,[bp+14]
    mov ax,[bp+12]
    pop di
    pop si
    pop bp
    ret 12
format_three_fields endp

public __strdate
__strdate proc far
    push bp
    mov bp,sp
    sub sp,6
    push si
    push di
    push ss
    lea ax,[bp-6]
    push ax
    call __dos_getdate
    pop cx
    pop cx
    push word ptr [bp+8]
    push word ptr [bp+6]
    mov al,[bp-5]
    mov ah,0
    push ax
    mov al,[bp-6]
    mov ah,0
    push ax
    mov ax,[bp-4]
    sub ax,1900
    push ax
    mov al,'/'
    push ax
    call format_three_fields
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
__strdate endp

public __strtime
__strtime proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    push ss
    lea ax,[bp-4]
    push ax
    call __dos_gettime
    pop cx
    pop cx
    push word ptr [bp+8]
    push word ptr [bp+6]
    mov al,[bp-4]
    mov ah,0
    push ax
    mov al,[bp-3]
    mov ah,0
    push ax
    mov al,[bp-2]
    mov ah,0
    push ax
    mov al,':'
    push ax
    call format_three_fields
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
__strtime endp
_TEXT ends
end
