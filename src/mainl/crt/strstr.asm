; Original large-model far cdecl substring search. The needle and source
; spans are scanned with real DOS string instructions and far segment setup.
; BP holds the temporary needle address after its original value is saved.
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _strstr
_strstr proc far
    push bp
    mov bp,sp
    push si
    push di
    les bx,dword ptr [bp+10]
    cmp byte ptr es:[bx],0
    jne short nonempty_needle
    mov dx,[bp+8]
    mov ax,[bp+6]
    jmp short return_ptr
nonempty_needle:
    push ds
    cld
    les di,dword ptr [bp+6]
    push es
    mov bx,di
    xor ax,ax
    mov cx,0FFFFh
    repne scasb
    not cx
    xchg cx,dx
    les di,dword ptr [bp+10]
    push es
    mov bp,di
    xor ax,ax
    mov cx,0FFFFh
    repne scasb
    inc cx
    not cx
    pop ds
    pop es
scan_next:
    mov si,bp
    lodsb
    xchg di,bx
    xchg cx,dx
    repne scasb
    mov bx,di
    jne short no_match
    cmp cx,dx
    jae short compare_remainder
no_match:
    xor bx,bx
    mov es,bx
    mov bx,1
    jmp short exit_search
compare_remainder:
    xchg cx,dx
    jcxz short exit_search
    mov ax,cx
    dec cx
    repe cmpsb
    mov cx,ax
    jne short scan_next
exit_search:
    pop ds
    mov ax,bx
    dec ax
    mov dx,es
return_ptr:
    pop di
    pop si
    pop bp
    retf
_strstr endp
_TEXT ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
end
