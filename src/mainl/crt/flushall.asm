; Return number of open streams visited, even when an individual fflush fails.
.8086
include stdio_layout.inc
extrn __streams:byte,__nfile:word,_fflush:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _flushall
_flushall proc far
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    mov word ptr [bp-8],0
    mov ax,DGROUP:__nfile
    mov [bp-6],ax
    mov [bp-2],ds
    mov word ptr [bp-4],offset DGROUP:__streams
    jmp short next_stream_test
 next_stream:
    les bx,[bp-4]
    test byte ptr es:[bx+FILE_FLAGS],F_RDWR
    je stream_visited
    push word ptr [bp-2]
    push bx
    call _fflush
    pop cx
    pop cx
    inc word ptr [bp-8]
 stream_visited:
    add word ptr [bp-4],FILE_BYTES
 next_stream_test:
    mov ax,[bp-6]
    dec word ptr [bp-6]
    or ax,ax
    jne next_stream
    mov ax,[bp-8]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_flushall endp
_TEXT ends
end
