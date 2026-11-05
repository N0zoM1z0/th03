; Full original Japanese Borland C++ istream method istgstr, real 8086.
; Preserves true streambuf vtable far calls, buffered get-area refill,
; EOF/delimiter/terminator conditions and original ios state flags.
.8086
extrn @ios@setstate$qi:far
extrn @istream@ipfx$qi:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @istream@get$qncic

; Original Borland emits the two real OMF references in reverse order.
org 300
    call @ios@setstate$qi
    add sp,6

istgstr_branch_0134:
    les bx,[bp+10]
    mov byte ptr es:[bx],0
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

org 0

@istream@get$qncic:
    push bp
    mov bp,sp
    sub sp,22
    push si
    push di
    mov ax,1
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @istream@ipfx$qi
    add sp,6
    or ax,ax
    jnz istgstr_branch_0021
    jmp near ptr istgstr_branch_0134

istgstr_branch_0021:
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov [bp-18],dx
    mov [bp-20],ax
    mov word ptr [bp-22],0
    jmp short istgstr_branch_0095

istgstr_branch_0034:
    les bx,[bp+10]
    mov al,[bp-22]
    mov es:[bx],al
    inc word ptr [bp+10]
    les bx,[bp+6]
    inc word ptr es:[bx+4]
    mov bx,es:[bx]
    mov [bp-2],es
    mov [bp-4],bx
    les bx,es:[bx+2]
    mov ax,es:[bx+30]
    les bx,[bp-4]
    les bx,es:[bx+2]
    cmp ax,es:[bx+34]
    jc istgstr_branch_0087
    les bx,[bp+6]
    mov bx,es:[bx]
    mov [bp-6],es
    mov [bp-8],bx
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    les bx,es:[bx+2]
    mov bx,es:[bx]
    call dword ptr [bx+12]
    pop cx
    pop cx
    jmp short istgstr_branch_0095

istgstr_branch_0087:
    les bx,[bp+6]
    mov bx,es:[bx]
    les bx,es:[bx+2]
    inc word ptr es:[bx+30]

istgstr_branch_0095:
    dec word ptr [bp+14]
    jng istgstr_branch_0106
    les bx,[bp+6]
    mov bx,es:[bx]
    mov [bp-10],es
    mov [bp-12],bx
    les bx,es:[bx+2]
    mov ax,es:[bx+30]
    les bx,[bp-12]
    les bx,es:[bx+2]
    cmp ax,es:[bx+34]
    jc istgstr_branch_00dd
    les bx,[bp+6]
    mov bx,es:[bx]
    mov [bp-14],es
    mov [bp-16],bx
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    les bx,es:[bx+2]
    mov bx,es:[bx]
    call dword ptr [bx+12]
    pop cx
    pop cx
    jmp short istgstr_branch_00f0

istgstr_branch_00dd:
    les bx,[bp+6]
    mov bx,es:[bx]
    les bx,es:[bx+2]
    les bx,es:[bx+30]
    mov al,es:[bx]
    mov ah,0

istgstr_branch_00f0:
    mov [bp-22],ax
    push ax
    mov al,[bp+16]
    cbw
    pop dx
    cmp dx,ax
    jz istgstr_branch_0106
    cmp word ptr [bp-22],-1
    jz istgstr_branch_0106
    jmp near ptr istgstr_branch_0034

istgstr_branch_0106:
    cmp word ptr [bp-22],-1
    jnz istgstr_branch_0134
    mov dx,[bp+12]
    mov ax,[bp+10]
    cmp dx,[bp-18]
    jnz istgstr_branch_0121
    cmp ax,[bp-20]
    jnz istgstr_branch_0121
    mov ax,3
    jmp short istgstr_branch_0124

istgstr_branch_0121:
    mov ax,1

istgstr_branch_0124:
    push ax
    les bx,[bp+6]
    push es
    push word ptr es:[bx]

_TEXTA ends
end
