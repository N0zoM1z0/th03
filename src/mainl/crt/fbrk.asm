; MAINL CRT heap-break provider, semantic assembly alternative to fbrk.c.
; All pointers use offset:segment words. Public entries are near cdecl;
; grow_break is near callee-pop, setblock is an actual far cdecl external.
; Arithmetic wrapping and failure stores are observable runtime contracts.
.8086
; Imported far code has unknown segment until link time. Do not bind it to
; _TEXT: doing so lets TASM shorten the call before TLINK sees the relocation.
extrn _setblock:far
_TEXT segment byte public 'CODE'
assume cs:_TEXT, ds:DGROUP
extrn N_PCMP@:near, N_LXLSH@:near, N_PADD@:near
public __brk, __sbrk

; grow_break(desired): resize DOS allocation when the cached 1-KiB granule
; changes, then commit the requested break. BP+4=offset, BP+6=segment.
; local BP-2 is a count: initially granules, then DOS paragraphs.
grow_break proc near
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    mov ax,[bp+6]
    inc ax
    mov [bp-2],ax
    mov ax,__psp
    sub [bp-2],ax
    mov ax,[bp-2]
    add ax,63
    mov cl,6
    shr ax,cl
    mov [bp-2],ax
    cmp ax,granule_count
    je commit_break

    ; Round in unsigned16 arithmetic before clamping to the known heap top.
    mov cl,6
    shl word ptr [bp-2],cl
    mov dx,word ptr __heaptop+2
    mov ax,[bp-2]
    add ax,__psp
    cmp ax,dx
    jbe request_resize
    mov ax,dx
    sub ax,__psp
    mov [bp-2],ax
request_resize:
    push word ptr [bp-2]
    push word ptr __psp
    call _setblock
    pop cx
    pop cx
    mov dx,ax
    cmp dx,-1
    jne resize_failed
    mov ax,[bp-2]
    mov cl,6
    shr ax,cl
    mov granule_count,ax
commit_break:
    mov dx,[bp+6]
    mov ax,[bp+4]
    mov word ptr __brklvl+2,dx
    mov word ptr __brklvl,ax
    mov ax,1
    jmp short grow_done
resize_failed:
    ; Even a failed growth changes heap top using DOS's BX reply. The break
    ; remains unchanged. BX=FFFF collides with success in the wrapper ABI.
    mov ax,__psp
    add ax,dx
    mov word ptr __heaptop+2,ax
    mov word ptr __heaptop,0
    xor ax,ax
grow_done:
    pop di
    pop si
    mov sp,bp
    pop bp
    ret 4
grow_break endp

; int near cdecl _brk(huge desired): both bounds use normalized pointer order.
__brk proc near
    push bp
    mov bp,sp
    push si
    push di
    mov cx,word ptr __heapbase+2
    mov bx,word ptr __heapbase
    mov dx,[bp+6]
    mov ax,[bp+4]
    call N_PCMP@
    jb break_failed
    mov cx,word ptr __heaptop+2
    mov bx,word ptr __heaptop
    mov dx,[bp+6]
    mov ax,[bp+4]
    call N_PCMP@
    ja break_failed
    push word ptr [bp+6]
    push word ptr [bp+4]
    call grow_break
    or ax,ax
    jne break_succeeded
break_failed:
    mov ax,-1
    jmp short break_done
break_succeeded:
    xor ax,ax
break_done:
    pop di
    pop si
    pop bp
    ret
__brk endp

; huge near cdecl _sbrk(long increment): return the previous pointer on success.
; BP-4/-2 holds normalized desired; BP-8/-6 preserves the previous pointer.
__sbrk proc near
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    mov ax,word ptr __brklvl+2
    xor dx,dx
    mov cl,4
    call N_LXLSH@
    add ax,word ptr __brklvl
    adc dx,0
    add ax,[bp+4]
    adc dx,[bp+6]

    ; Signed32 upper bound only. Negative sums deliberately continue through
    ; huge-pointer normalization, including the historical -1-MiB alias.
    cmp dx,000Fh
    jl normalize_desired
    jg increment_failed
    cmp ax,0FFFFh
    ja increment_failed
normalize_desired:
    mov dx,word ptr __brklvl+2
    mov ax,word ptr __brklvl
    mov cx,[bp+6]
    mov bx,[bp+4]
    call N_PADD@
    mov [bp-2],dx
    mov [bp-4],ax
    mov cx,word ptr __heapbase+2
    mov bx,word ptr __heapbase
    call N_PCMP@
    jb increment_failed
    mov cx,word ptr __heaptop+2
    mov bx,word ptr __heaptop
    mov dx,[bp-2]
    mov ax,[bp-4]
    call N_PCMP@
    ja increment_failed
    mov dx,word ptr __brklvl+2
    mov ax,word ptr __brklvl
    mov [bp-6],dx
    mov [bp-8],ax
    push word ptr [bp-2]
    push word ptr [bp-4]
    call grow_break
    or ax,ax
    jne increment_succeeded
increment_failed:
    mov dx,-1
    mov ax,-1
    jmp short increment_done
increment_succeeded:
    mov dx,[bp-6]
    mov ax,[bp-8]
increment_done:
    pop di
    pop si
    mov sp,bp
    pop bp
    ret
__sbrk endp
_TEXT ends

_DATA segment word public 'DATA'
; Defining data externs in DATA, not CODE, is required for DGROUP fixup frames.
extrn __psp:word, __heapbase:dword, __brklvl:dword, __heaptop:dword
granule_count dw 0
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
end
