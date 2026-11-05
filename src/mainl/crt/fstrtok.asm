; Original far strtok with a real persistent far BSS cursor, delimiter
; scanning, string splitting and the precise Borland segment/offset ABI.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
saved_cursor dd ?
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __fstrtok
__fstrtok proc far
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz short skip_delimiters
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov word ptr DGROUP:saved_cursor+2,dx
    mov word ptr DGROUP:saved_cursor,ax
    jmp short skip_delimiters
scan_one_delimiter:
    mov dx,[bp+0ch]
    mov ax,[bp+0ah]
    mov [bp-2],dx
    mov [bp-4],ax
    jmp short test_delimiter_end
check_single_delimiter:
    les bx,dword ptr [bp-4]
    mov al,byte ptr es:[bx]
    les bx,dword ptr DGROUP:saved_cursor
    cmp al,byte ptr es:[bx]
    jz short delimiter_found
    inc word ptr [bp-4]
test_delimiter_end:
    les bx,dword ptr [bp-4]
    cmp byte ptr es:[bx],0
    jnz short check_single_delimiter
delimiter_found:
    les bx,dword ptr [bp-4]
    cmp byte ptr es:[bx],0
    jz short token_empty_check
    inc word ptr DGROUP:saved_cursor
skip_delimiters:
    les bx,dword ptr DGROUP:saved_cursor
    cmp byte ptr es:[bx],0
    jnz short scan_one_delimiter
token_empty_check:
    les bx,dword ptr DGROUP:saved_cursor
    cmp byte ptr es:[bx],0
    jnz short token_begin
    xor dx,dx
    xor ax,ax
    jmp short done
token_begin:
    mov dx,word ptr DGROUP:saved_cursor+2
    mov ax,word ptr DGROUP:saved_cursor
    mov [bp-6],dx
    mov [bp-8],ax
    jmp short continue_token
scan_token_delimiters:
    mov dx,[bp+0ch]
    mov ax,[bp+0ah]
    mov [bp-2],dx
    mov [bp-4],ax
    jmp short test_token_delimiter_end
compare_token_char:
    les bx,dword ptr [bp-4]
    mov al,byte ptr es:[bx]
    les bx,dword ptr DGROUP:saved_cursor
    cmp al,byte ptr es:[bx]
    jnz short next_token_delimiter
    mov byte ptr es:[bx],0
    inc word ptr DGROUP:saved_cursor
    jmp short return_token
next_token_delimiter:
    inc word ptr [bp-4]
test_token_delimiter_end:
    les bx,dword ptr [bp-4]
    cmp byte ptr es:[bx],0
    jnz short compare_token_char
    inc word ptr DGROUP:saved_cursor
continue_token:
    les bx,dword ptr DGROUP:saved_cursor
    cmp byte ptr es:[bx],0
    jnz short scan_token_delimiters
return_token:
    mov dx,[bp-6]
    mov ax,[bp-8]
done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
__fstrtok endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
