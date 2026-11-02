; Original Borland DOS large-model far-cdecl fgets, 154 CODE bytes.
; Read into the caller's far buffer, stopping at newline or requested
; count, use the FILE's native buffered stream fields, and fall back to
; the genuine far __fgetc provider. Preserve original EOF/error result.
.8086
extrn __fgetc:far
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _fgets
_fgets proc far
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
    jmp short read_loop
store_character:
    les bx,dword ptr [bp-4]
    mov byte ptr es:[bx],cl
    inc word ptr [bp-4]
read_loop:
    cmp cx,10
    je short read_finished
    dec word ptr [bp+0Ah]
    jle short read_finished
    les bx,dword ptr [bp+0Ch]
    dec word ptr es:[bx]
    jl short get_fresh_character
    mov dx,word ptr es:[bx+0Eh]
    mov si,word ptr es:[bx+0Ch]
    inc word ptr es:[bx+0Ch]
    mov es,dx
    mov al,byte ptr es:[si]
    mov ah,0
    jmp short handle_character
get_fresh_character:
    push word ptr [bp+0Eh]
    push word ptr [bp+0Ch]
    call __fgetc
    pop cx
    pop cx
handle_character:
    mov cx,ax
    cmp ax,0ffffh
    jne short store_character
read_finished:
    cmp cx,-1
    jne short write_terminator
    mov dx,[bp-2]
    mov ax,[bp-4]
    cmp dx,[bp+8]
    jne short write_terminator
    cmp ax,[bp+6]
    jne short write_terminator
    xor dx,dx
    xor ax,ax
    jmp short fgets_done
write_terminator:
    les bx,dword ptr [bp-4]
    mov byte ptr es:[bx],0
    les bx,dword ptr [bp+0Ch]
    test byte ptr es:[bx+2],010h
    je short return_buffer
    xor dx,dx
    xor ax,ax
    jmp short fgets_done
return_buffer:
    mov dx,[bp+8]
    mov ax,[bp+6]
fgets_done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_fgets endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
end
