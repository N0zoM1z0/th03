; Original Borland farheap linked-list memory manager, 16-bit real mode.
; Includes original uninitialized CODE-state words, near/far public allocator,
; free, realloc, rover search/merge, segment growth, and DOS break helpers.
; C++/game code references are not replaced by machine-code data arrays.
.8086
extrn __brk:near,__sbrk:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public ___first,___last,___rover
public _farfree,_free,_malloc,_farmalloc,_realloc,_farrealloc

; Borland allocator's three initialized public segment-link words.
___first dw 0
___last dw 0
___rover dw 0
; These three private state words are uninitialized in the original CODE
; image (no LEDATA coverage at _TEXT+6..11). Do not materialize zeros.
heap_state_6 dw ?
heap_state_8 dw ?
heap_state_a dw ?

farheap_000c:
    cmp dx,cs:[___first]
    jz farheap_004a
    mov ds,dx
    mov ds,word ptr ds:[2]
    cmp word ptr ds:[2],0
    jz farheap_0027
    mov cs:[___last],ds
    jmp short farheap_005f

farheap_0027:
    mov ax,ds
    cmp ax,cs:[___first]
    jz farheap_0045
    mov ax,word ptr ds:[8]
    mov cs:[___last],ax
    push ds
    xor ax,ax
    push ax
    call farheap_00e0
    mov ds,cs:[heap_state_6]
    jmp short farheap_0068

farheap_0045:
    mov dx,cs:[___first]

farheap_004a:
    mov word ptr cs:[___first],0
    mov word ptr cs:[___last],0
    mov word ptr cs:[___rover],0

farheap_005f:
    mov ds,cs:[heap_state_6]
    push dx
    xor ax,ax
    push ax

farheap_0068:
    call __brk
    add sp,4
    ret

farheap_006f:
    mov ds,dx
    push ds
    mov es,word ptr ds:[2]
    mov word ptr ds:[2],0
    mov word ptr ds:[8],es
    cmp dx,cs:[___first]
    jz farheap_00b5
    cmp word ptr es:[2],0
    jnz farheap_00b5
    mov ax,word ptr ds:[0]
    pop bx
    push es
    add word ptr es:[0],ax
    mov cx,es
    add dx,ax
    mov es,dx
    cmp word ptr es:[2],0
    jnz farheap_00ae
    mov word ptr es:[8],cx
    jmp short farheap_00b8

farheap_00ae:
    mov word ptr es:[2],cx
    jmp short farheap_00b8

farheap_00b5:
    call farheap_0109

farheap_00b8:
    pop es
    mov ax,es
    add ax,word ptr es:[0]
    mov ds,ax
    cmp word ptr ds:[2],0
    jz farheap_00ca
    ret

farheap_00ca:
    mov ax,word ptr ds:[0]
    add word ptr es:[0],ax
    mov ax,es
    mov bx,ds
    add bx,word ptr ds:[0]
    mov es,bx
    mov word ptr es:[2],ax

farheap_00e0:
    mov bx,ds
    cmp bx,word ptr ds:[6]
    jz farheap_0101
    mov es,word ptr ds:[6]
    mov ds,word ptr ds:[4]
    mov word ptr ds:[6],es
    mov word ptr es:[4],ds
    mov cs:[___rover],ds
    mov ds,bx
    ret

farheap_0101:
    mov word ptr cs:[___rover],0
    ret

farheap_0109:
    mov ax,cs:[___rover]
    or ax,ax
    jz farheap_0132
    mov bx,ss
    pushf
    cli
    mov ss,ax
    mov es,word ptr ss:[6]
    mov word ptr ss:[6],ds
    mov word ptr ds:[4],ss
    mov ss,bx
    popf
    mov word ptr es:[4],ds
    mov word ptr ds:[6],es
    ret

farheap_0132:
    mov cs:[___rover],ds
    mov word ptr ds:[4],ds
    mov word ptr ds:[6],ds
    ret

; Native segment-level far free implementation, with a shared far/near
; public entry at the exact original offset.
_farfree:
; Original _free and _farfree two aliases share this body.
_free:
    push bp
    mov bp,sp
    push si
    push di
    mov cs:[heap_state_6],ds
    mov dx,[bp+8]
    or dx,dx
    jz farheap_0160
    cmp dx,cs:[___last]
    jnz farheap_015d
    call farheap_000c
    jmp short farheap_0160

farheap_015d:
    call farheap_006f

farheap_0160:
    mov ds,cs:[heap_state_6]
    pop di
    pop si
    pop bp
    retf

farheap_0169:
    push ax
    mov ds,cs:[heap_state_6]
    xor ax,ax
    push ax
    push ax
    call __sbrk
    add sp,4
    and ax,15
    jz farheap_0192
    mov dx,16
    sub dx,ax
    xor ax,ax
    mov ds,cs:[heap_state_6]
    push ax
    push dx
    call __sbrk
    add sp,4

farheap_0192:
    pop ax
    push ax
    xor bx,bx
    mov bl,ah
    mov cl,4
    shr bx,cl
    shl ax,cl
    mov ds,cs:[heap_state_6]
    push bx
    push ax
    call __sbrk
    add sp,4
    pop bx
    cmp ax,65535
    jz farheap_01c9
    mov cs:[___first],dx
    mov cs:[___last],dx
    mov ds,dx
    mov word ptr ds:[0],bx
    mov word ptr ds:[2],dx
    mov ax,4
    ret

farheap_01c9:
    xor ax,ax
    cwd
    ret

farheap_01cd:
    push ax
    mov ds,cs:[heap_state_6]
    xor ax,ax
    push ax
    push ax
    call __sbrk
    pop bx
    pop bx
    and ax,15
    jz farheap_01f5
    mov dx,16
    sub dx,ax
    xor ax,ax
    mov ds,cs:[heap_state_6]
    push ax
    push dx
    call __sbrk
    add sp,4

farheap_01f5:
    pop ax
    push ax
    xor bx,bx
    mov bl,ah
    mov cl,4
    shr bx,cl
    shl ax,cl
    mov ds,cs:[heap_state_6]
    push bx
    push ax
    call __sbrk
    add sp,4
    pop bx
    cmp ax,65535
    jz farheap_024c
    and ax,15
    jnz farheap_0231

farheap_0219:
    mov cx,cs:[___last]
    mov cs:[___last],dx
    mov ds,dx
    mov word ptr ds:[0],bx
    mov word ptr ds:[2],cx
    mov ax,4
    ret

farheap_0231:
    push bx
    push dx
    neg ax
    add ax,16
    xor bx,bx
    push bx
    push ax
    call __sbrk
    add sp,4
    pop dx
    pop bx
    cmp ax,65535
    jz farheap_024c
    inc dx
    jmp short farheap_0219

farheap_024c:
    xor ax,ax
    cwd
    ret

farheap_0250:
    mov bx,dx
    sub word ptr ds:[0],ax
    add dx,word ptr ds:[0]
    mov ds,dx
    mov word ptr ds:[0],ax
    mov word ptr ds:[2],bx
    mov bx,dx
    add bx,word ptr ds:[0]
    mov ds,bx
    mov word ptr ds:[2],dx
    mov ax,4
    ret

; Near-pointer malloc wrapper. Original DX=0 path enters far allocator.
_malloc:
    push bp
    mov bp,sp
    xor dx,dx
    mov ax,[bp+6]
    jmp short farheap_0286

; Far allocation body: rover scan, splitting and extending heap blocks.
_farmalloc:
    push bp
    mov bp,sp
    mov dx,[bp+8]
    mov ax,[bp+6]

farheap_0286:
    mov cx,ax
    or cx,dx
    push si
    push di
    mov cs:[heap_state_6],ds
    jz farheap_02f1
    add ax,19
    adc dx,0
    jc farheap_02dc
    test dx,65520
    jnz farheap_02dc
    mov cl,4
    shr ax,cl
    shl dx,cl
    or ah,dl
    mov dx,cs:[___first]
    or dx,dx
    jz farheap_02d2
    mov dx,cs:[___rover]
    or dx,dx
    jz farheap_02cd
    mov bx,dx

farheap_02bd:
    mov ds,dx
    cmp word ptr ds:[0],ax
    jnc farheap_02e1
    mov dx,word ptr ds:[6]
    cmp dx,bx
    jnz farheap_02bd

farheap_02cd:
    call farheap_01cd
    jmp short farheap_02f1

farheap_02d2:
    call farheap_0169
    jmp short farheap_02f1

farheap_02d7:
    call farheap_0250
    jmp short farheap_02f1

farheap_02dc:
    xor ax,ax
    cwd
    jmp short farheap_02f1

farheap_02e1:
    ja farheap_02d7
    call farheap_00e0
    mov bx,word ptr ds:[8]
    mov word ptr ds:[2],bx
    mov ax,4

farheap_02f1:
    mov ds,cs:[heap_state_6]
    pop di
    pop si
    pop bp
    retf

farheap_02fa:
    push bx
    mov si,cs:[heap_state_8]
    push si
    mov si,cs:[heap_state_a]
    push si
    push cs
    call _farmalloc
    add sp,4
    or dx,dx
    jnz farheap_0314
    pop bx
    ret

farheap_0314:
    pop ds
    mov es,dx
    push es
    push ds
    push bx
    mov dx,word ptr ds:[0]
    cld
    dec dx
    mov di,4
    mov si,di
    mov cx,6
    rep movsw
    or dx,dx
    jz farheap_0365
    mov ax,es
    inc ax
    mov es,ax
    mov ax,ds
    inc ax
    mov ds,ax

farheap_0338:
    xor di,di
    mov si,di
    mov cx,dx
    cmp cx,4096
    jna farheap_0347
    mov cx,4096

farheap_0347:
    shl cx,1
    shl cx,1
    shl cx,1
    rep movsw
    sub dx,4096
    jna farheap_0365
    mov ax,es
    add ax,4096
    mov es,ax
    mov ax,ds
    add ax,4096
    mov ds,ax
    jmp short farheap_0338

farheap_0365:
    mov ds,cs:[heap_state_6]
    push cs
    call _farfree
    add sp,4
    pop dx
    mov ax,4
    ret

farheap_0376:
    cmp bx,cs:[___last]
    jz farheap_03c2
    mov di,bx
    add di,ax
    mov es,di
    mov si,cx
    sub si,ax
    mov word ptr es:[0],si
    mov word ptr es:[2],bx
    push es
    push ax
    mov es,bx
    mov word ptr es:[0],ax
    mov dx,bx
    add dx,cx
    mov es,dx
    cmp word ptr es:[2],0
    jz farheap_03ae
    mov word ptr es:[2],di
    jmp short farheap_03b3

farheap_03ae:
    mov word ptr es:[8],di

farheap_03b3:
    mov si,bx
    push cs
    call _farfree
    add sp,4
    mov dx,si
    mov ax,4
    ret

farheap_03c2:
    push bx
    mov es,bx
    mov word ptr es:[0],ax
    add bx,ax
    push bx
    xor ax,ax
    push ax
    call __brk
    add sp,4
    pop dx
    mov ax,4
    ret

; Near realloc wrapper shares the far realloc common path.
_realloc:
    push bp
    mov bp,sp
    xor dx,dx
    jmp short farheap_03e7

; Far realloc body: shrink in place, move block or allocate/free.
_farrealloc:
    push bp
    mov bp,sp
    mov dx,[bp+12]

farheap_03e7:
    mov ax,[bp+10]
    mov bx,[bp+8]
    push si
    push di
    mov cs:[heap_state_6],ds
    mov cs:[heap_state_8],dx
    mov cs:[heap_state_a],ax
    or bx,bx
    jz farheap_043b
    mov cx,ax
    or cx,dx
    jz farheap_0446
    add ax,19
    adc dx,0
    jc farheap_044f
    test dx,65520
    jnz farheap_044f
    mov cl,4
    shr ax,cl
    shl dx,cl
    or ah,dl
    mov es,bx
    mov cx,word ptr es:[0]
    cmp cx,ax
    jc farheap_0436
    ja farheap_0431
    mov dx,bx
    mov ax,4
    jmp short farheap_0452

farheap_0431:
    call farheap_0376
    jmp short farheap_0452

farheap_0436:
    call farheap_02fa
    jmp short farheap_0452

farheap_043b:
    push dx
    push ax
    push cs
    call _farmalloc
    add sp,4
    jmp short farheap_0452

farheap_0446:
    push bx
    push ax
    push cs
    call _farfree
    add sp,4

farheap_044f:
    xor ax,ax
    cwd

farheap_0452:
    mov ds,cs:[heap_state_6]
    pop di
    pop si
    pop bp
    retf

_TEXT ends
end
