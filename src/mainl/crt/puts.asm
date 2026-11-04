; Borland large-model puts: write a far NUL-terminated string to stdout,
; then append LF, accounting for a failed bulk write or final character.
.8086
include stdio_layout.inc
extrn __streams:byte,_fputc:far,_strlen:far,__FPUTN:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _puts
_puts proc far
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jne string_present
    xor ax,ax
    jmp short result
string_present:
    push word ptr [bp+8]
    push word ptr [bp+6]
    call _strlen
    pop cx
    pop cx
    mov [bp-2],ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    push ax
    push ds
    mov ax,offset DGROUP:__streams+FILE_BYTES
    push ax
    call __FPUTN
    cmp ax,[bp-2]
    je newline
    mov ax,-1
    jmp short result
newline:
    push ds
    mov ax,offset DGROUP:__streams+FILE_BYTES
    push ax
    mov ax,10
    push ax
    call _fputc
    add sp,6
    cmp ax,10
    je success
    mov ax,-1
    jmp short result
success:
    mov ax,10
result:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_puts endp
_TEXT ends
end
