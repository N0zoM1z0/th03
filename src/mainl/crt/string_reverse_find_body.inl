; Original last-of / last-not-of algorithm; only the membership branch differs.
; Each TU keeps its own native far API and CODE extent. Original start=0 and
; decrement/test loop semantics are preserved, including the index-0 behavior.
; CBW sign-extends the original signed input byte before the real strchr call.
STRING_REVERSE_FIND macro api_name,skip_condition
; Native instruction chunks retain original FIXUPP enumeration.

org 141
    call ___ExitExceptBlocks
    pop ax
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 107
    call @strchr$qnxci
    add sp, 6
    or ax, dx
    skip_condition short reverse_step
    mov ax, word ptr [bp+0eh]
    jmp short reverse_result_ready
reverse_step:
    dec word ptr [bp+0eh]
    mov ax, word ptr [bp+0eh]
    or ax, ax
    ja short reverse_scan
reverse_not_found:
    mov ax, 0ffffh
reverse_result_ready:
    push ax
    push word ptr [bp-01eh]

org 14
    call ___InitExceptBlocks
    cmp word ptr [bp+0eh], 0
    je short reverse_not_found
    les bx, dword ptr [bp+6]
    les bx, dword ptr es:[bx]
    mov ax, word ptr es:[bx+6]
    cmp ax, word ptr [bp+0eh]
    jae short reverse_start_in_range
    mov word ptr [bp+0eh], ax
    jmp short reverse_prepare
reverse_start_in_range:
    inc word ptr [bp+0eh]
reverse_prepare:
    les bx, dword ptr [bp+0ah]
    les bx, dword ptr es:[bx]
    mov dx, word ptr es:[bx+4]
    mov ax, word ptr es:[bx+2]
    mov word ptr [bp-020h], dx
    mov word ptr [bp-022h], ax
    les bx, dword ptr [bp+6]
    les bx, dword ptr es:[bx]
    mov dx, word ptr es:[bx+4]
    mov ax, word ptr es:[bx+2]
    mov word ptr [bp-024h], dx
    mov word ptr [bp-026h], ax
    jmp short reverse_step
reverse_scan:
    les bx, dword ptr [bp-026h]
    add bx, word ptr [bp+0eh]
    mov al, byte ptr es:[bx]
    cbw
    push ax
    push word ptr [bp-020h]
    push word ptr [bp-022h]

org 11
    mov bx,offset _TEXT:string_exception_frame

org 8
    mov ax,seg string_exception_unwind

org 0
api_name proc far
    push bp
    mov bp, sp
    sub sp, 026h
    push si
    push di
api_name endp
endm
