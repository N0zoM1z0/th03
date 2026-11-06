; FAR table chain: load ES:BX from the argument and each base-table link.
; Original Japanese Borland fddvt: complete native CRT member.
; Preserve far interfaces, original unchecked arithmetic and ordered relocations.
.8086
extrn _abort:far
FDDVT_TEXT segment word public 'CODE'
FDDVT_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
FDDVT_TEXT segment word public 'CODE'
assume cs:FDDVT_TEXT,ds:DGROUP
public @_DDVTdispatchNULL$qnvi
public @_DDVTdispatch$qnvi
; Complete disjoint instruction chunks preserve original OMF field chronology.
; FAR fallback slots are inline metadata, not instructions.
null_dispatch_slot dd 0
abort_dispatch_slot dd _abort

org 8
@_DDVTdispatchNULL$qnvi label far
    mov ax,offset null_dispatch_slot
    jmp short dispatch_lookup

org 13
@_DDVTdispatch$qnvi label far
    mov ax,offset abort_dispatch_slot
dispatch_lookup:
    push bp
    mov bp, sp
    push si
    push di
    push ax
    les bx, dword ptr [bp+6]
    std
search_dispatch_table:
    mov cx, word ptr es:[bx-6]
    jcxz short search_base_table
    mov dx, cx
    mov ax, word ptr [bp+0ah]
    lea di, [bx-8]
    repne scasw
    je short dispatch_entry_found
search_base_table:
    les bx, dword ptr es:[bx-4]
    mov ax, es
    or ax, bx
    jne short search_dispatch_table
    pop ax
    mov dx, cs
    jmp short dispatch_return
dispatch_entry_found:
    shl dx, 1
    sub bx, dx
    shl cx, 1
    sub dx, cx
    shl dx, 1
    add dx, 6
    sub bx, dx
    pop ax
    mov ax, bx
    mov dx, es
dispatch_return:
    cld
    pop di
    pop si
    pop bp
    retf
FDDVT_TEXT ends
end
