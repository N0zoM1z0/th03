; Original Borland DOS far getenv scans the real environment pointer
; vector for NAME=VALUE, preserving caller DS/ES and far DX:AX return.
; It searches for the first '=' after the supplied key, not through an
; emulated process environment or a new host library.
.8086
extrn __environ:dword
public _getenv
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
_getenv label far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    les di,dword ptr [bp+6]
    mov ax,es
    or ax,di
    je short no_match
    mov al,0
    mov ah,byte ptr es:[di]
    mov cx,0FFFFh
    cld
    repne scasb
    not cx
    dec cx
    je short no_match
    les di,dword ptr __environ
    mov word ptr [bp-2],es
    mov bx,es
    or bx,di
    mov word ptr [bp-4],di
    jne short check_environment
no_match:
    xor dx,dx
    xor ax,ax
    jmp short getenv_done
next_environment:
    add word ptr [bp-4],4
    les di,dword ptr [bp-4]
check_environment:
    les di,dword ptr es:[di]
    mov bx,es
    or bx,di
    je short no_match
    mov al,byte ptr es:[di]
    or al,al
    je short no_match
    cmp ah,al
    jne short next_environment
    mov bx,cx
    cmp byte ptr es:[di+bx],3Dh
    jne short next_environment
    ; Prevent TASM ASSUME DS optimizer from treating the live DS save
    ; as a DGROUP memory expression. Both ASSUME lines emit zero bytes.
    assume ds:NOTHING
    push ds
    lds si,dword ptr [bp+6]
    repe cmpsb
    pop ds
    assume ds:DGROUP
    xchg cx,bx
    jne short next_environment
    inc di
    mov ax,di
    mov dx,es
getenv_done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
end
