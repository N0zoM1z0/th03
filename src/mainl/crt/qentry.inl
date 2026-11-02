; Original far public qsort front end (the last 44 bytes of qsort.obj).
; The huge near sorting core qsort_core is declared elsewhere in this
; same real TU. Its near Pascal RET 6 is an important caller contract.
public _qsort
_qsort proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+12]
    mov qsort_width,ax
    or ax,ax
    je short qsort_return
    mov dx,[bp+16]
    mov ax,[bp+14]
    mov word ptr qsort_compare+2,dx
    mov word ptr qsort_compare,ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+10]
    call qsort_core
qsort_return:
    pop di
    pop si
    pop bp
    retf
_qsort endp
