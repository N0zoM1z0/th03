; Original far multibyte string tokenization with a real static far cursor.
; Delegates leading delimiter skip and delimiter search to original CRT,
; preserving MBCS trail treatment and original unchecked far pointer math.
.8086
extrn __mbctype:byte
extrn __fmbspbrk:far
extrn __fmbsspnp:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __fmbstok
__fmbstok proc far
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz short use_saved_cursor
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    jmp short skip_delimiters
use_saved_cursor:
    mov ax,word ptr DGROUP:saved_cursor
    or ax,word ptr DGROUP:saved_cursor+2
    jz short empty_result
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr DGROUP:saved_cursor+2
    push word ptr DGROUP:saved_cursor
skip_delimiters:
    call __fmbsspnp
    add sp,8
    mov [bp-2],dx
    mov [bp-4],ax
    mov ax,[bp-4]
    or ax,[bp-2]
    jz short empty_result
    les bx,dword ptr [bp-4]
    cmp byte ptr es:[bx],0
    jz short empty_result
    mov al,byte ptr es:[bx]
    mov ah,0
    mov bx,ax
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz short find_delimiter
    mov bx,[bp-4]
    cmp byte ptr es:[bx+1],0
    jnz short find_delimiter
empty_result:
    xor dx,dx
    xor ax,ax
    jmp short done
find_delimiter:
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp-2]
    push word ptr [bp-4]
    call __fmbspbrk
    add sp,8
    mov [bp-6],dx
    mov [bp-8],ax
    or ax,[bp-6]
    jz short reset_cursor
    les bx,dword ptr [bp-8]
    cmp byte ptr es:[bx],0
    jnz short have_delimiter
reset_cursor:
    mov word ptr DGROUP:saved_cursor+2,0
    mov word ptr DGROUP:saved_cursor,0
    jmp short return_token
have_delimiter:
    les bx,dword ptr [bp-8]
    mov al,byte ptr es:[bx]
    mov ah,0
    mov bx,ax
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz short terminate_token
    mov bx,[bp-8]
    mov byte ptr es:[bx],0
    inc word ptr [bp-8]
terminate_token:
    les bx,dword ptr [bp-8]
    mov byte ptr es:[bx],0
    inc word ptr [bp-8]
    mov dx,[bp-6]
    mov ax,[bp-8]
    mov word ptr DGROUP:saved_cursor+2,dx
    mov word ptr DGROUP:saved_cursor,ax
return_token:
    mov dx,[bp-2]
    mov ax,[bp-4]
done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
__fmbstok endp
_TEXT ends
_DATA segment word public 'DATA'
saved_cursor dd 0
_DATA ends
end
