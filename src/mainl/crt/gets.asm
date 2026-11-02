; DOS Borland far-cdecl gets: original stdin FILE global-buffer reader.
; Uses __streams direct buffered fields with far fallback __fgetc.
; Original NUL, newline and EOF handling, far SS destination cursor.
; Source blocks follow genuine descending FIXUPP order, disjoint/no filler.
.8086
extrn __streams:word
extrn __fgetc:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
public _gets
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 06Eh
    test byte ptr DGROUP:__streams+2,10h
    je short return_stdin_buffer
    xor dx, dx
    xor ax, ax
    jmp short gets_return
return_stdin_buffer:
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
gets_return:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 039h
    call __fgetc
    pop cx
    pop cx
inspect_stdin_character:
    mov dx, ax
    cmp ax, 0ffffh
    je short end_stdin_line
    cmp dx, 0ah
    jne short store_stdin_character
end_stdin_line:
    cmp dx, -1
    jne short terminate_stdin_buffer
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    cmp dx, word ptr [bp+8]
    jne short terminate_stdin_buffer
    cmp ax, word ptr [bp+6]
    jne short terminate_stdin_buffer
    xor dx, dx
    xor ax, ax
    jmp short gets_return
terminate_stdin_buffer:
    les bx, dword ptr [bp-4]
    mov byte ptr es:[bx], 0
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 035h
    mov ax,offset DGROUP:__streams
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 029h
    inc word ptr DGROUP:__streams+0Ch
    mov al, byte ptr es:[bx]
    mov ah, 0
    jmp short inspect_stdin_character
fetch_stdin_fallback:
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 025h
    les bx,dword ptr DGROUP:__streams+0Ch
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01Fh
read_stdin:
    dec word ptr DGROUP:__streams
    jl short fetch_stdin_fallback
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 00h
_gets label far
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    jmp short read_stdin
store_stdin_character:
    les bx, dword ptr [bp-4]
    mov byte ptr es:[bx], dl
    inc word ptr [bp-4]
_TEXT ends
end
