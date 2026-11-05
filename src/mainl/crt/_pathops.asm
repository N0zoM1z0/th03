; Original Japanese Borland path DBCS operations, including actual
; DOS 21h 6300h initialization and CRT INITDATA registration.
; Stores a real far vector and a default zero-terminated DBCS span table.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_INIT_ segment word public 'INITDATA'
_INIT_ ends
DGROUP group _DATA,_BSS

_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
path_dbcs_initializer proc near
    push ax
    push cx
    push dx
    push bx
    push sp
    push bp
    push si
    push di
    push ds
    push es
    mov bp,sp
    mov ax,word ptr DGROUP:___path_dbcs_vector
    or ax,word ptr DGROUP:___path_dbcs_vector+2
    jnz short init_done
    mov si,-1
    push ds
    mov ax,6300h
    clc
    int 21h
    mov ax,ds
    pop ds
    jc short fallback
    mov dx,ds
    cmp ax,dx
    jz short fallback
    cmp si,-1
    jnz short assign_vector
fallback:
    mov si,offset DGROUP:___path_dbcs_default
    mov ax,seg DGROUP:___path_dbcs_vector
assign_vector:
    mov word ptr DGROUP:___path_dbcs_vector,si
    mov word ptr DGROUP:___path_dbcs_vector+2,ax
init_done:
    mov sp,bp
    pop es
    pop ds
    pop di
    pop si
    pop bp
    pop bx
    pop bx
    pop dx
    pop cx
    pop ax
    ret
path_dbcs_initializer endp

public ___path_isdbcsleadbyte
___path_isdbcsleadbyte proc far
    push bp
    mov bp,sp
    push si
    push di
    mov al,[bp+6]
    xor cx,cx
    les bx,dword ptr DGROUP:___path_dbcs_vector
test_range:
    mov dx,word ptr es:[bx]
    or dx,dx
    jz short return_lead
    cmp al,dl
    jb short return_lead
    inc bx
    inc bx
    cmp al,dh
    ja short test_range
    inc cx
return_lead:
    xchg cx,ax
    pop di
    pop si
    pop bp
    retf
___path_isdbcsleadbyte endp

public ___path_issbcs
___path_issbcs proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    xor cx,cx
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-2],dx
    mov [bp-4],ax
read_char:
    les bx,dword ptr [bp-4]
    cmp byte ptr es:[bx],0
    jnz short advance_character
    xor cx,cx
    jmp short check_finished
advance_character:
    cmp cx,1
    jnz short classify_character
    mov cx,2
    jmp short check_range
classify_character:
    les bx,dword ptr [bp-4]
    mov al,byte ptr es:[bx]
    push ax
    push cs
    call near ptr ___path_isdbcsleadbyte
    pop cx
    or ax,ax
    jz short not_lead
    mov cx,1
    jmp short check_range
not_lead:
    xor cx,cx
check_range:
    mov ax,[bp-4]
    cmp ax,[bp+0ah]
    jae short check_finished
    inc word ptr [bp-4]
    jmp short read_char
check_finished:
    or cx,cx
    jnz short is_multibyte
    mov ax,1
    jmp short done
is_multibyte:
    xor ax,ax
done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
___path_issbcs endp
_TEXT ends

_DATA segment word public 'DATA'
public ___path_dbcs_vector,___path_dbcs_default
___path_dbcs_vector dd 0
___path_dbcs_default dw 0,0,0,0,0,0
_DATA ends

_INIT_ segment word public 'INITDATA'
    dw 0f00h
    dw path_dbcs_initializer
    dw 0
_INIT_ ends
end
