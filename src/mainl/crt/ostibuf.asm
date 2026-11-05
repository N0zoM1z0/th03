; Original Borland C++ ostream << streambuf full transfer operator.
; Retains actual large-model stream/streambuf object graph, virtual vtable
; underflow/overflow, osfx/opfx callbacks and error-state propagation.
.8086
extrn @ios@setstate$qi:far
extrn @ostream@do_opfx$qv:far,@ostream@do_osfx$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ostream@$blsh$qn9streambuf
@ostream@$blsh$qn9streambuf proc far
    push bp
    mov bp,sp
    sub sp,10
    push si
    push di
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    cmp word ptr es:[bx+0eh],0
    jz short prefix_success
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @ostream@do_opfx$qv
    pop cx
    pop cx
    jmp short test_prefix
prefix_success:
    mov ax,1
test_prefix:
    or ax,ax
    jnz short start_transfer
    jmp near ptr transfer_done
start_transfer:
    jmp near ptr next_input

write_character:
    mov cx,[bp-10]
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    mov [bp-2],es
    mov [bp-4],bx
    les bx,dword ptr es:[bx+2]
    mov ax,word ptr es:[bx+12h]
    les bx,dword ptr [bp-4]
    les bx,dword ptr es:[bx+2]
    cmp ax,word ptr es:[bx+16h]
    jc short store_output
    mov al,cl
    mov ah,0
    push ax
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    mov [bp-6],es
    mov [bp-8],bx
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    les bx,dword ptr es:[bx+2]
    mov bx,word ptr es:[bx]
    call dword ptr [bx+18h]
    add sp,6
    jmp short check_output
store_output:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    les bx,dword ptr es:[bx+2]
    mov dx,word ptr es:[bx+14h]
    mov si,word ptr es:[bx+12h]
    inc word ptr es:[bx+12h]
    mov al,cl
    mov es,dx
    mov byte ptr es:[si],al
    mov ah,0
check_output:
    cmp ax,0ffffh
    jnz short next_input
    mov ax,4
    push ax
    les bx,dword ptr [bp+6]
    push es
    push word ptr es:[bx]
    call @ios@setstate$qi
    add sp,6
    jmp short transfer_done

next_input:
    les bx,dword ptr [bp+10]
    mov ax,word ptr es:[bx+1eh]
    cmp ax,word ptr es:[bx+22h]
    jc short fetch_input
    push word ptr [bp+12]
    push bx
    mov bx,word ptr es:[bx]
    call dword ptr [bx+0ch]
    pop cx
    pop cx
    cmp ax,0ffffh
    jnz short fetch_input
    mov ax,0ffffh
    jmp short store_input
fetch_input:
    les bx,dword ptr [bp+10]
    mov dx,word ptr es:[bx+20h]
    mov si,word ptr es:[bx+1eh]
    inc word ptr es:[bx+1eh]
    mov es,dx
    mov al,byte ptr es:[si]
    mov ah,0
store_input:
    mov [bp-10],ax
    cmp ax,0ffffh
    jz short transfer_done
    jmp near ptr write_character

transfer_done:
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    test byte ptr es:[bx+11h],60h
    jz short skip_suffix
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @ostream@do_osfx$qv
    pop cx
    pop cx
    jmp short skip_suffix
skip_suffix:
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@ostream@$blsh$qn9streambuf endp
_TEXTA ends
end
