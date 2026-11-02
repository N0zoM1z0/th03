; Original Borland DOS lsearch/lfind module, two far public functions
; and a single original private near Pascal array search worker.
; The near worker calls the actual far comparator [BP+6], advances
; the element pointer, optionally appends with genuine far _movmem,
; increments the original element count and returns far DX:AX.
; _lsearch inserts; _lfind performs only searching. No extra bounds.
.8086
extrn _movmem:far
public _lsearch,_lfind
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
search_find_or_append label near
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    les bx, dword ptr [bp+0ch]
    mov ax, word ptr es:[bx]
    mov word ptr [bp-2], ax
    jmp short search_have_remaining
search_compare_next:
    push word ptr [bp+012h]
    push word ptr [bp+010h]
    push word ptr [bp+016h]
    push word ptr [bp+014h]
    call dword ptr [bp+6]
    add sp, 8
    or ax, ax
    je short search_return
    mov ax, word ptr [bp+0ah]
    add word ptr [bp+010h], ax
    dec word ptr [bp-2]
search_have_remaining:
    cmp word ptr [bp-2], 0
    jg short search_compare_next
    cmp word ptr [bp+4], 0
    je short search_not_found
    les bx, dword ptr [bp+0ch]
    inc word ptr es:[bx]
    push word ptr [bp+0ah]
    push word ptr [bp+012h]
    push word ptr [bp+010h]
    push word ptr [bp+016h]
    push word ptr [bp+014h]
    call _movmem
    add sp, 0ah
    jmp short search_return
search_not_found:
    mov word ptr [bp+012h], 0
    mov word ptr [bp+010h], 0
search_return:
    mov dx, word ptr [bp+012h]
    mov ax, word ptr [bp+010h]
    pop di
    pop si
    mov sp, bp
    pop bp
    ret 014h
_lsearch label far
    push bp
    mov bp, sp
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
    push word ptr [bp+012h]
    push word ptr [bp+016h]
    push word ptr [bp+014h]
    mov ax, 1
    push ax
    call near ptr search_find_or_append
    pop di
    pop si
    pop bp
    retf
_lfind label far
    push bp
    mov bp, sp
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
    push word ptr [bp+012h]
    push word ptr [bp+016h]
    push word ptr [bp+014h]
    xor ax, ax
    push ax
    call near ptr search_find_or_append
    pop di
    pop si
    pop bp
    retf
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
end
