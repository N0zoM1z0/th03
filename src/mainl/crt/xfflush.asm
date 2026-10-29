; Exit-buffer callback deliberately visits only the first four FILE slots.
.8086
include stdio_layout.inc
extrn __streams:byte,_fflush:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __xfflush
__xfflush proc far
    push bp
    mov bp,sp
    sub sp,6
    push si
    push di
    mov word ptr [bp-6],4
    mov [bp-2],ds
    mov word ptr [bp-4],offset DGROUP:__streams
    jmp short exit_stream_test
 exit_stream:
    les bx,[bp-4]
    test byte ptr es:[bx+FILE_FLAGS],F_RDWR
    je exit_stream_visited
    push word ptr [bp-2]
    push bx
    call _fflush
    pop cx
    pop cx
 exit_stream_visited:
    dec word ptr [bp-6]
    add word ptr [bp-4],FILE_BYTES
 exit_stream_test:
    cmp word ptr [bp-6],0
    jne exit_stream
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
__xfflush endp
_TEXT ends
end
