; Proved identical original const/mutable regular-expression slice bodies.
; The caller owns its far public entry and separate native _TEXTC segment.
; Retain original hidden result pointer, optional allocation, and return ABI.
STRING_REGEXP_SLICE macro api_name
; Native statement chunks preserve complete original ordered FIXUPPs.

org 163
    call ___ExitExceptBlocks
    pop ax
    pop dx
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 100
    call @$bnew$qui
    pop cx
    mov word ptr [bp-02ch], dx
    mov word ptr [bp-02eh], ax
slice_storage_ready:
    or ax, dx
    je short slice_constructed
    les bx, dword ptr [bp-02eh]
    mov dx, word ptr [bp-028h]
    mov ax, word ptr [bp-02ah]
    mov word ptr es:[bx+2], dx
    mov word ptr es:[bx], ax
    mov ax, word ptr [bp-026h]
    mov word ptr es:[bx+4], ax
    mov ax, word ptr [bp-024h]
    mov word ptr es:[bx+6], ax
slice_constructed:
    mov dx, word ptr [bp-02ch]
    mov ax, word ptr [bp-02eh]
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    push dx
    push ax
    push word ptr [bp-01eh]

org 39
    call @string@find$xqmx7TRegexpnuiui
    add sp, 0eh
    mov word ptr [bp-022h], ax
    mov ax, word ptr [bp-020h]
    mov word ptr [bp-024h], ax
    mov ax, word ptr [bp-022h]
    mov word ptr [bp-026h], ax
    mov dx, word ptr [bp+0ch]
    mov ax, word ptr [bp+0ah]
    mov word ptr [bp-028h], dx
    mov word ptr [bp-02ah], ax
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    mov word ptr [bp-02ch], dx
    mov word ptr [bp-02eh], ax
    or ax, word ptr [bp-02ch]
    je short slice_allocate
    mov ax, word ptr [bp-02eh]
    jmp short slice_storage_ready
slice_allocate:
    mov ax, 8
    push ax

org 14
    call ___InitExceptBlocks
    push word ptr [bp+012h]
    push ss
    lea ax, [bp-020h]
    push ax
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]

org 11
    mov bx,offset _TEXT:string_exception_frame

org 8
    mov ax,seg string_exception_unwind

org 0
api_name proc far
    push bp
    mov bp, sp
    sub sp, 02eh
    push si
    push di
api_name endp
endm
