; Zero size becomes one byte; failed allocation retries through the existing FAR handler.
; Original Japanese Borland newf: complete native CRT member.
; Preserve far interfaces, original unchecked arithmetic and ordered relocations.
.8086
extrn _farmalloc:far
extrn __new_handler:dword
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public @$bnew$qul
; Complete disjoint instruction chunks preserve original OMF field chronology.

org 67
    or ax, word ptr DGROUP:__new_handler+2
    jne short invoke_new_handler
allocation_return:
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 64
    mov ax, word ptr DGROUP:__new_handler

org 47
    call _farmalloc
    pop cx
    pop cx
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    or ax, dx
    jne short allocation_return

org 37
invoke_new_handler:
    call dword ptr DGROUP:__new_handler
retry_allocation:
    push word ptr [bp+8]
    push word ptr [bp+6]

org 0
@$bnew$qul label far
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    mov ax, word ptr [bp+6]
    or ax, word ptr [bp+8]
    je short allocate_one_byte
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    jmp short store_allocation_size
allocate_one_byte:
    xor dx, dx
    mov ax, 1
store_allocation_size:
    mov word ptr [bp+8], dx
    mov word ptr [bp+6], ax
    jmp short retry_allocation
_TEXT ends
end
