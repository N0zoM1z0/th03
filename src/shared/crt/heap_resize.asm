; Shared runtime: complete original bytes, ABI and literal ordered fields.
; Ordinary source spans preserve native record chronology; no storage is filled.
; The pinned compatible emitter keeps all actual near/far call distances intact.
; MAINL CRT heap-break provider, semantic assembly alternative to fbrk.c.
; All pointers use offset:segment words. Public entries are near cdecl;
; grow_break is near callee-pop, setblock is an actual far cdecl external.
; Arithmetic wrapping and failure stores are observable runtime contracts.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
extrn __psp:word
_DATA ends
; External code retains an unknown segment; the call distances remain explicit.
extrn _setblock:far
_DATA segment word public 'DATA'
extrn __heapbase:dword, __heaptop:dword, __brklvl:dword
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
extrn N_PCMP@:near, N_LXLSH@:near, N_PADD@:near
_TEXT segment byte public 'CODE'
assume cs:_TEXT, ds:DGROUP
public __brk, __sbrk

; grow_break(desired): resize DOS allocation when the cached 1-KiB granule
; changes, then commit the requested break. BP+4=offset, BP+6=segment.
; local BP-2 is a count: initially granules, then DOS paragraphs.
; Bind original code labels before scheduling their ordinary instruction spans.
org 0
grow_break label near
org 69
request_resize label near
org 100
commit_break label near
org 118
resize_failed label near
org 134
grow_done label near
; __brk(huge desired), near cdecl: compare both normalized pointer bounds.
org 142
__brk label near
org 198
break_failed label near
org 203
break_succeeded label near
org 205
break_done label near
; __sbrk(long increment), near cdecl: preserve old break at BP-8/-6.
; Desired BP-4/-2 uses signed32 upper bound only; negative sums normalize.
; Failed resize changes heap top from DOS reply, while leaving break unchanged.
org 209
__sbrk label near
org 252
normalize_desired label near
org 332
increment_failed label near
org 340
increment_succeeded label near
org 346
increment_done label near

; Original CODE 310..351.
org 310
    mov ax,word ptr __brklvl
    mov [bp-6],dx
    mov [bp-8],ax
    push word ptr [bp-2]
    push word ptr [bp-4]
    call grow_break
    or ax,ax
    jne increment_succeeded
    mov dx,-1
    mov ax,-1
    jmp short increment_done
    mov dx,[bp-6]
    mov ax,[bp-8]
    pop di
    pop si
    mov sp,bp
    pop bp
    ret

; Original CODE 306..309.
org 306
    mov dx,word ptr __brklvl+2

; Original CODE 301..305.
org 301
    call N_PCMP@
    ja increment_failed

; Original CODE 291..300.
org 291
    mov bx,word ptr __heaptop
    mov dx,[bp-2]
    mov ax,[bp-4]

; Original CODE 287..290.
org 287
    mov cx,word ptr __heaptop+2

; Original CODE 282..286.
org 282
    call N_PCMP@
    jb increment_failed

; Original CODE 278..281.
org 278
    mov bx,word ptr __heapbase

; Original CODE 274..277.
org 274
    mov cx,word ptr __heapbase+2

; Original CODE 265..273.
org 265
    call N_PADD@
    mov [bp-2],dx
    mov [bp-4],ax

; Original CODE 256..264.
org 256
    mov ax,word ptr __brklvl
    mov cx,[bp+6]
    mov bx,[bp+4]

; Original CODE 252..255.
org 252
    mov dx,word ptr __brklvl+2

; Original CODE 227..251.
org 227
    add ax,word ptr __brklvl
    adc dx,0
    add ax,[bp+4]
    adc dx,[bp+6]
    cmp dx,000Fh
    jl normalize_desired
    jg increment_failed
    cmp ax,word ptr 0FFFFh
    ja increment_failed

; Original CODE 224..226.
org 224
    call N_LXLSH@

; Original CODE 217..223.
org 217
    mov ax,word ptr __brklvl+2
    xor dx,dx
    mov cl,4

; Original CODE 180..216.
org 180
    call N_PCMP@
    ja break_failed
    push word ptr [bp+6]
    push word ptr [bp+4]
    call grow_break
    or ax,ax
    jne break_succeeded
    mov ax,-1
    jmp short break_done
    xor ax,ax
    pop di
    pop si
    pop bp
    ret
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di

; Original CODE 170..179.
org 170
    mov bx,word ptr __heaptop
    mov dx,[bp+6]
    mov ax,[bp+4]

; Original CODE 166..169.
org 166
    mov cx,word ptr __heaptop+2

; Original CODE 161..165.
org 161
    call N_PCMP@
    jb break_failed

; Original CODE 151..160.
org 151
    mov bx,word ptr __heapbase
    mov dx,[bp+6]
    mov ax,[bp+4]

; Original CODE 147..150.
org 147
    mov cx,word ptr __heapbase+2

; Original CODE 126..146.
org 126
    mov word ptr __heaptop,0
    xor ax,ax
    pop di
    pop si
    mov sp,bp
    pop bp
    ret 4
    push bp
    mov bp,sp
    push si
    push di

; Original CODE 123..125.
org 123
    mov word ptr __heaptop+2,ax

; Original CODE 118..122.
org 118
    mov ax,__psp
    add ax,dx

; Original CODE 110..117.
org 110
    mov word ptr __brklvl,ax
    mov ax,1
    jmp short grow_done

; Original CODE 106..109.
org 106
    mov word ptr __brklvl+2,dx

; Original CODE 97..105.
org 97
    mov granule_count,ax
    mov dx,[bp+6]
    mov ax,[bp+4]

; Original CODE 76..96.
org 76
    call _setblock
    pop cx
    pop cx
    mov dx,ax
    cmp dx,-1
    jne resize_failed
    mov ax,[bp-2]
    mov cl,6
    shr ax,cl

; Original CODE 72..75.
org 72
    push word ptr __psp

; Original CODE 62..71.
org 62
    sub ax,__psp
    mov [bp-2],ax
    push word ptr [bp-2]

; Original CODE 52..61.
org 52
    add ax,__psp
    cmp ax,dx
    jbe request_resize
    mov ax,dx

; Original CODE 45..51.
org 45
    mov dx,word ptr __heaptop+2
    mov ax,[bp-2]

; Original CODE 34..44.
org 34
    cmp ax,granule_count
    je commit_break
    mov cl,6
    shl word ptr [bp-2],cl

; Original CODE 15..33.
org 15
    mov ax,__psp
    sub [bp-2],ax
    mov ax,[bp-2]
    add ax,word ptr 63
    mov cl,6
    shr ax,cl
    mov [bp-2],ax

; Original CODE 0..14.
org 0
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    mov ax,[bp+6]
    inc ax
    mov [bp-2],ax
_TEXT ends

_DATA segment word public 'DATA'
; Defining data externs in DATA, not CODE, is required for DGROUP fixup frames.
granule_count dw 0
_DATA ends

end
