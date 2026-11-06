; Original huge-pointer difference, optional paragraph overhead and low-word alignment.
; Original Japanese Borland fcorelft: complete native CRT member.
; Preserve far interfaces, original unchecked arithmetic and ordered relocations.
.8086
extrn __heaptop:dword
extrn __brklvl:dword
extrn N_PSBP@:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _farcoreleft
; Complete disjoint instruction chunks preserve original OMF field chronology.

org 33
    call N_PSBP@
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    cmp word ptr [bp-2], 0
    jb short align_available_bytes
    ja short subtract_heap_overhead
    cmp word ptr [bp-4], 010h
    jbe short align_available_bytes
subtract_heap_overhead:
    sub word ptr [bp-4], 010h
    sbb word ptr [bp-2], 0
align_available_bytes:
    and word ptr [bp-4], 0fff0h
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 29
    mov bx, word ptr DGROUP:__brklvl

org 25
    mov cx, word ptr DGROUP:__brklvl+2

org 22
    mov ax, word ptr DGROUP:__heaptop

org 18
    mov dx, word ptr DGROUP:__heaptop+2

org 0
_farcoreleft label far
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    mov word ptr [bp-2], 0
    mov word ptr [bp-4], 0
_TEXT ends
end
