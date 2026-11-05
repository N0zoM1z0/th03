; Original Japanese Borland startup command-line and argv parser.
; Complete 8086 DOS PSP text parsing, DBCS lead-byte escape rules, quote
; control, backslash handling, stack argv table and original C0 startup ABI.
; Two genuinely uninitialized CODE bytes, 10 reserved DATA and sparse INIT.
.8086
extrn __C0argc:word
extrn __C0argv:word
extrn __psp:word
extrn __envseg:word
extrn __envLng:word
extrn __osmajor:word
extrn __abort:far
extrn ___path_isdbcsleadbyte:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_INIT_ segment word public 'INITDATA'
_INIT_ ends
DGROUP group _DATA
; Original BCC absolute PUBDEF startup initializer anchor, not near CODE.
__setargv__ equ 0
public __setargv__
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
setargv_saved_ds dw ?

setargv_start:
    pop word ptr DGROUP:argv_saved_call0
    pop word ptr DGROUP:argv_saved_call1
    pop word ptr DGROUP:argv_saved_call2
    mov cs:word ptr setargv_saved_ds,ds
    mov word ptr DGROUP:argv_saved_si,si
    mov word ptr DGROUP:argv_saved_di,di
    cld
    mov es,word ptr __psp
    mov si,128
    xor ah,ah
    lods byte ptr es:[si]
    inc ax
    mov bp,es
    xchg dx,si
    xchg ax,bx
    mov si,word ptr __envLng
    inc si
    inc si
    mov cx,1
    cmp byte ptr __osmajor,3
    jc argv_branch_004e
    mov es,word ptr __envseg
    mov di,si
    mov cl,127
    xor al,al
    repne scasb
    jcxz argv_branch_0095
    xor cl,127

argv_branch_004e:
    push ax
    mov ax,cx
    add ax,bx
    inc ax
    and ax,65534
    mov di,sp
    sub di,ax
    jc argv_branch_0095
    mov sp,di
    push es
    pop ds
    push ss
    pop es
    push cx
    dec cx
    rep movsb
    xor al,al
    stosb
    mov ds,bp
    xchg si,dx
    xchg bx,cx
    mov ax,bx
    mov dx,ax
    inc bx

argv_branch_0075:
    call setargv_buffer_copy
    ja argv_branch_0085

argv_branch_007a:
    jc setargv_finalize
    cmp al,13
    jz argv_branch_0091
    call setargv_buffer_copy
    ja argv_branch_007a

argv_branch_0085:
    cmp al,32
    jz argv_branch_0091
    cmp al,13
    jz argv_branch_0091
    cmp al,9
    jnz argv_branch_0075

argv_branch_0091:
    xor al,al
    jmp short argv_branch_0075

argv_branch_0095:
    jmp __abort

setargv_buffer_copy:
    or ax,ax
    jz argv_branch_00a5
    inc dx
    stosb
    or al,al
    jnz argv_branch_00a5
    inc bx

argv_branch_00a5:
    xchg ah,al
    xor al,al
    stc
    jcxz argv_branch_00eb
    lodsb
    dec cx
    cmp dh,1
    jz argv_branch_00d1
    xor dh,dh
    push ax
    push bx
    push cx
    push dx
    push ds
    push es
    mov ds,cs:word ptr setargv_saved_ds
    push ax
    call ___path_isdbcsleadbyte
    or ax,ax
    pop cx
    pop es
    pop ds
    pop dx
    pop cx
    pop bx
    pop ax
    jz argv_branch_00d3

argv_branch_00d1:
    inc dh

argv_branch_00d3:
    cmp dh,0
    jnz argv_branch_00e9
    sub al,34
    jz argv_branch_00eb
    add al,34
    cmp al,92
    jnz argv_branch_00e9
    cmp byte ptr [si],34
    jnz argv_branch_00e9
    lodsb
    dec cx

argv_branch_00e9:
    or si,si

argv_branch_00eb:
    ret

setargv_finalize:
    pop cx
    xor dh,dh
    add cx,dx
    mov ds,cs:word ptr setargv_saved_ds
    mov word ptr DGROUP:__argc,bx
    inc bx
    add bx,bx
    add bx,bx
    mov si,sp
    mov bp,sp
    sub bp,bx
    jc argv_branch_0095
    mov sp,bp
    mov word ptr DGROUP:__argv,bp
    mov word ptr DGROUP:__argv+2,ss

argv_branch_0111:
    jcxz argv_branch_0124
    mov [bp+0],si
    mov [bp+2],ss
    add bp,4

argv_branch_011c:
    lods byte ptr ss:[si]
    or al,al
    loopne argv_branch_011c
    jz argv_branch_0111

argv_branch_0124:
    xor ax,ax
    mov [bp+0],ax
    mov [bp+2],ax
    mov ds,cs:word ptr setargv_saved_ds
    mov si,word ptr DGROUP:argv_saved_si
    mov di,word ptr DGROUP:argv_saved_di
    push word ptr DGROUP:argv_saved_call2
    push word ptr DGROUP:argv_saved_call1
    mov ax,word ptr DGROUP:__argc
    mov word ptr __C0argc,ax
    mov ax,word ptr DGROUP:__argv+2
    mov word ptr __C0argv+2,ax
    mov ax,word ptr DGROUP:__argv
    mov word ptr __C0argv,ax
    jmp word ptr DGROUP:argv_saved_call0
_TEXT ends
_DATA segment word public 'DATA'
public __argc,__argv
__argc dw 0
__argv dd 0
argv_saved_call0 dw ?
argv_saved_call1 dw ?
argv_saved_call2 dw ?
argv_saved_si dw ?
argv_saved_di dw ?
_DATA ends
_INIT_ segment word public 'INITDATA'
    dw 1000h
    dw offset _TEXT:setargv_start
    dw ?
_INIT_ ends
end
