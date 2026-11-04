; Selected original Japanese Borland near/far heap integrity subsystem.
; Complete five multi-public heap diagnostic and free-list operations.
; Symbolic original CS heap roots; no CODE byte initializer or OBJ patch.
.8086
extrn __brk:near,__sbrk:near,___first:word,___last:word,___rover:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _farheapcheck,_heapcheck,_farheapchecknode,_heapchecknode,_farheapfillfree,_heapfillfree,_farheapcheckfree,_heapcheckfree,_farheapwalk,_heapwalk

; Original selected CRT public helper(s) at CODE+0: _farheapcheck, _heapcheck
_farheapcheck:
_heapcheck:
    push si
    push di
    push bp
    push ds
    mov ax, word ptr cs:___first
    or ax, ax
    jne loc_000f
    jmp near ptr loc_00ea
loc_000f:
    xor bx, bx
    push bx
    push bx
    call __sbrk
    add sp, 4
    or ax, ax
    je loc_0020
    jmp near ptr loc_00e5
loc_0020:
    mov bx, word ptr cs:___last
    mov ds, bx
    add bx, word ptr ds:[0]
    cmp bx, dx
    je loc_0032
    jmp near ptr loc_00e5
loc_0032:
    mov ax, word ptr cs:___first
    xor cx, cx
    mov dx, cx
    mov ds, ax
    add ax, word ptr ds:[0]
    mov es, ax
loc_0042:
    cmp word ptr ds:[2], 0
    jne loc_0061
    add cx, word ptr ds:[0]
    mov si, ds
    cmp si, word ptr cs:___last
    je loc_00a5
    cmp word ptr es:[2], 0
    jne loc_0061
    jmp near ptr loc_00e5
loc_0061:
    mov si, ds
    mov di, es
    cmp si, word ptr cs:___last
    je loc_00a5
    cmp si, di
    je loc_00e5
    cmp word ptr ds:[0], 0
    je loc_00e5
    cmp di, word ptr cs:___first
    jbe loc_00e5
    cmp di, word ptr cs:___last
    ja loc_00e5
    cmp word ptr es:[2], 0
    je loc_0094
    cmp word ptr es:[2], si
    jmp short loc_0099
loc_0094:
    cmp word ptr es:[8], si
loc_0099:
    jne loc_00e5
    mov ds, di
    add di, word ptr ds:[0]
    mov es, di
    jmp short loc_0042
loc_00a5:
    mov ax, word ptr cs:___rover
    or ax, ax
    je loc_00ef
    mov ds, ax
    mov si, ax
loc_00b1:
    cmp word ptr ds:[2], 0
    jne loc_00e5
    cmp si, word ptr cs:___first
    jb loc_00e5
    cmp si, word ptr cs:___last
    jae loc_00e5
    add dx, word ptr ds:[0]
    mov es, word ptr ds:[6]
    mov di, es
    cmp di, ax
    je loc_00ef
    cmp si, di
    je loc_00e5
    cmp word ptr es:[4], si
    jne loc_00e5
    mov si, es
    mov ds, si
    jmp short loc_00b1
loc_00e5:
    mov ax, 0ffffh
    jmp short loc_00f6
loc_00ea:
    mov ax, 1
    jmp short loc_00f6
loc_00ef:
    cmp cx, dx
    jne loc_00e5
    mov ax, 2
loc_00f6:
    pop ds
    pop bp
    pop di
    pop si
    retf

; Original selected CRT public helper(s) at CODE+251: _farheapchecknode, _heapchecknode
_farheapchecknode:
_heapchecknode:
    push bp
    mov bp, sp
    push si
    push di
    push ds
    push cs
    call _farheapcheck
    cmp ax, 2
    jne loc_0162
    mov ax, word ptr [bp + 8]
    mov si, word ptr cs:___first
    mov di, word ptr cs:___last
    mov bx, si
loc_0119:
    mov ds, bx
    cmp bx, ax
    je loc_0153
    cmp word ptr ds:[2], 0
    je loc_012e
    cmp word ptr ds:[2], si
    jb loc_0144
    jmp short loc_0134
loc_012e:
    cmp word ptr ds:[8], si
    jb loc_0144
loc_0134:
    cmp bx, di
    je loc_014e
    ja loc_0144
    mov cx, bx
    add bx, word ptr ds:[0]
    cmp bx, cx
    jne loc_0119
loc_0144:
    mov ax, 0ffffh
    jmp short loc_0162
    mov ax, 1
    jmp short loc_0162
loc_014e:
    mov ax, 0fffeh
    jmp short loc_0162
loc_0153:
    cmp word ptr ds:[2], 0
    jne loc_015f
    mov ax, 3
    jmp short loc_0162
loc_015f:
    mov ax, 4
loc_0162:
    pop ds
    pop di
    pop si
    pop bp
    retf

; Original selected CRT public helper(s) at CODE+359: _farheapfillfree, _heapfillfree
_farheapfillfree:
_heapfillfree:
    push bp
    mov bp, sp
    push si
    push di
    push cs
    call _farheapcheck
    cmp ax, 2
    jne loc_01bd
    mov bx, word ptr cs:___rover
    or bx, bx
    je loc_01ba
    cld
    mov ax, word ptr [bp + 6]
loc_0182:
    mov es, bx
    mov dx, word ptr es:[0]
    mov si, word ptr es:[6]
    mov di, 0ah
    mov cx, 3
loc_0194:
    rep stosw
    xor di, di
    mov cx, 8
    inc bx
    mov es, bx
    dec dx
    jne loc_0194
    cmp si, word ptr cs:___rover
    je loc_01ba
    or si, si
    je loc_01b0
    mov bx, si
    jmp short loc_0182
loc_01b0:
    mov ax, 0ffffh
    jmp short loc_01bd
    mov ax, 1
    jmp short loc_01bd
loc_01ba:
    mov ax, 2
loc_01bd:
    pop di
    pop si
    pop bp
    retf

; Original selected CRT public helper(s) at CODE+449: _farheapcheckfree, _heapcheckfree
_farheapcheckfree:
_heapcheckfree:
    push bp
    mov bp, sp
    push si
    push di
    push cs
    call _farheapcheck
    cmp ax, 2
    jne loc_021e
    mov bx, word ptr cs:___rover
    or bx, bx
    je loc_021b
    mov ax, word ptr [bp + 6]
    cld
loc_01dc:
    mov es, bx
    mov dx, word ptr es:[0]
    mov si, word ptr es:[6]
    mov di, 0ah
    mov cx, 3
loc_01ee:
    repe scasw
    jne loc_020c
    xor di, di
    mov cx, 8
    inc bx
    mov es, bx
    dec dx
    jne loc_01ee
    cmp si, word ptr cs:___rover
    je loc_021b
    or si, si
    je loc_0211
    mov bx, si
    jmp short loc_01dc
loc_020c:
    mov ax, 0fffdh
    jmp short loc_021e
loc_0211:
    mov ax, 0ffffh
    jmp short loc_021e
    mov ax, 1
    jmp short loc_021e
loc_021b:
    mov ax, 2
loc_021e:
    pop di
    pop si
    pop bp
    retf

; Original selected CRT public helper(s) at CODE+546: _farheapwalk, _heapwalk
_farheapwalk:
_heapwalk:
    push bp
    mov bp, sp
    push si
    push di
    mov di, word ptr [bp + 6]
    push ds
    mov bx, word ptr [bp + 8]
    cmp di, -10h
    jb loc_0237
    inc bx
    sub di, 10h
loc_0237:
    mov ds, bx
    mov bx, word ptr [di + 2]
    or bx, bx
    je loc_024b
    cmp bx, word ptr cs:___last
    je loc_0291
    or bx, bx
    jne loc_0258
loc_024b:
    mov bx, word ptr cs:___first
    or bx, bx
    je loc_028c
    mov es, bx
    jmp short loc_0261
loc_0258:
    mov es, bx
    add bx, word ptr es:[0]
    mov es, bx
loc_0261:
    mov word ptr [di + 2], es
    mov word ptr [di], 4
    mov ax, word ptr es:[0]
    mov bx, 10h
    mul bx
    mov word ptr [di + 4], ax
    mov word ptr [di + 6], dx
    mov word ptr [di + 8], 0
    cmp word ptr es:[2], 0
    je loc_0287
    inc word ptr [di + 8]
loc_0287:
    mov ax, 2
    jmp short loc_0294
loc_028c:
    mov ax, 1
    jmp short loc_0294
loc_0291:
    mov ax, 5
loc_0294:
    pop ds
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
