; Borland 16-bit FAR setjmp/longjmp with exception-chain preservation.
; The saved context is a real stack/segment/flags register image.
; longjmp integrates the original global/local C++ unwind procedures.
.8086
extrn __Local_unwind:far
extrn __CurrExcContext:far
extrn __Global_unwind:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _setjmp,_longjmp
_setjmp proc far
    push bp
    mov bp,sp
    push si
    push di
    pushf
    pop bx
    mov dx,es
    mov cx,di
    les di,dword ptr [bp+6]
    cld
    lea ax,[bp+6]
    stosw
    mov ax,ss
    stosw
    xchg bx,ax
    stosw
    mov ax,[bp+4]
    stosw
    mov ax,[bp+2]
    stosw
    mov ax,[bp]
    stosw
    xchg cx,ax
    stosw
    mov ax,dx
    stosw
    xchg si,ax
    stosw
    mov ax,ds
    stosw
    mov ax,word ptr ss:[14h]
    stosw
    push es
    push dx
    push ax
    call __CurrExcContext
    pop cx
    pop dx
    pop es
    stosw
    mov es,dx
    xor ax,ax
    pop di
    pop si
    pop bp
    retf
_setjmp endp

_longjmp proc far
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+0ah]
    cmp dx,1
    adc dx,0
    mov ax,ds
    mov es,ax
    lds si,dword ptr [bp+6]
    cld
    mov di,si
    pushf
    pop bx
    lodsw
    cli
    mov ss,word ptr [si]
    mov sp,ax
    push bx
    popf
    lodsw
    mov ax,[di+14h]
    cmp word ptr ss:[14h],ax
    jz short maybe_local_unwind
    push ds
    push es
    mov bx,es
    mov ds,bx
    les bx,dword ptr [bp+6]
    push word ptr es:[bx+16h]
    push word ptr es:[bx+14h]
    call __Global_unwind
    pop cx
    pop cx
    pop es
    pop ds
    mov ax,[di+14h]
    mov word ptr ss:[14h],ax
maybe_local_unwind:
    push ds
    push es
    mov bx,es
    mov ds,bx
    push ax
    call __CurrExcContext
    pop cx
    pop es
    pop ds
    cmp ax,-1
    jz short restore_registers
    cmp ax,[di+16h]
    jz short restore_registers
    push ds
    push es
    les bx,dword ptr [bp+6]
    push word ptr es:[bx+16h]
    call __Local_unwind
    pop cx
    pop es
    pop ds
restore_registers:
    lodsw
    push ax
    lodsw
    push ax
    lodsw
    push ax
    lodsw
    xchg bp,ax
    lodsw
    xchg di,ax
    lodsw
    mov es,ax
    lodsw
    mov ds,word ptr [si]
    xchg si,ax
    xchg dx,ax
    iret
longjmp_fallback_epilogue:
    pop di
    pop si
    pop bp
    retf
_longjmp endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
