; Entire original Borland @filebuf@overflow$qi implementation.
; True streambuf put-area, setp/setg, far virtual output, binary/text DOS
; write behavior and failure/EOF handling. Native symbolic 8086 code.
.8086
extrn _write:far
extrn @streambuf@setp$qnct1:far
extrn @streambuf@setg$qnct1t1:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @filebuf@overflow$qi

; Original Borland far-import FIXUPP emission block at CODE+243.
org 243
    call @streambuf@setg$qnct1t1
    add sp,28
    cmp word ptr [bp+10],-1
    jz filebuf_overflow_0144
    mov cx,[bp+10]
    les bx,[bp+6]
    mov ax,es:[bx+18]
    cmp ax,es:[bx+22]
    jc filebuf_overflow_0125
    mov al,cl
    mov ah,0
    push ax
    push word ptr [bp+8]
    push bx
    mov bx,es:[bx]
    call dword ptr [bx+24]
    add sp,6
    jmp short filebuf_overflow_013d

filebuf_overflow_0125:
    les bx,[bp+6]
    mov dx,es:[bx+20]
    mov si,es:[bx+18]
    inc word ptr es:[bx+18]
    mov al,cl
    mov es,dx
    mov es:[si],al
    mov ah,0

filebuf_overflow_013d:
    les bx,[bp+6]
    inc word ptr es:[bx+30]

filebuf_overflow_0144:
    mov ax,1

filebuf_overflow_0147:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Original Borland far-import FIXUPP emission block at CODE+209.
org 209
    call @streambuf@setp$qnct1
    mov ax,[bp-8]
    add ax,[bp-4]
    mov [bp-2],ax
    push word ptr [bp-6]
    push ax
    push word ptr [bp-6]
    push ax
    push word ptr [bp-6]
    push word ptr [bp-8]
    push word ptr [bp+8]
    push word ptr [bp+6]

; Original Borland far-import FIXUPP emission block at CODE+0.
org 0

@filebuf@overflow$qi:
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    les bx,[bp+6]
    cmp word ptr es:[bx+42],0
    jz filebuf_overflow_0078
    mov ax,es:[bx+40]
    and ax,3
    cmp ax,1
    jz filebuf_overflow_0078
    les bx,[bp+6]
    cmp word ptr es:[bx+4],0
    jnz filebuf_overflow_0032
    mov ax,es:[bx+6]
    or ax,es:[bx+8]
    jnz filebuf_overflow_0063

filebuf_overflow_0032:
    cmp word ptr [bp+10],-1
    jnz filebuf_overflow_003b
    jmp near ptr filebuf_overflow_0144

filebuf_overflow_003b:
    mov al,[bp+10]
    mov [bp-3],al
    mov ax,1
    push ax
    push ss
    lea ax,[bp-3]
    push ax
    les bx,[bp+6]
    push word ptr es:[bx+38]
    call _write
    add sp,8
    cmp ax,1
    jnz filebuf_overflow_0061
    jmp near ptr filebuf_overflow_0144

filebuf_overflow_0061:
    jmp short filebuf_overflow_0078

filebuf_overflow_0063:
    push word ptr [bp+8]
    push word ptr [bp+6]
    les bx,[bp+6]
    mov bx,es:[bx]
    call dword ptr [bx+36]
    pop cx
    pop cx
    or ax,ax
    jz filebuf_overflow_007e

filebuf_overflow_0078:
    mov ax,65535
    jmp near ptr filebuf_overflow_0147

filebuf_overflow_007e:
    les bx,[bp+6]
    mov ax,es:[bx+10]
    xor dx,dx
    sub ax,es:[bx+6]
    sbb dx,0
    cmp ax,8
    jng filebuf_overflow_0098
    mov ax,4
    jmp short filebuf_overflow_009b

filebuf_overflow_0098:
    mov ax,1

filebuf_overflow_009b:
    mov [bp-4],ax
    les bx,[bp+6]
    mov dx,es:[bx+8]
    mov ax,es:[bx+6]
    mov [bp-6],dx
    mov [bp-8],ax
    mov ax,es:[bx+10]
    xor dx,dx
    sub ax,es:[bx+6]
    sbb dx,0
    add ax,[bp-8]
    push word ptr [bp-6]
    push ax
    mov ax,[bp-8]
    add ax,[bp-4]
    push word ptr [bp-6]
    push ax
    push word ptr [bp+8]
    push bx
_TEXTA ends
end
