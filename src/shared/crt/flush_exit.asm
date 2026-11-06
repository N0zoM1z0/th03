; Exit callback: inspect the first four FILE slots and flush open streams.
; The loop precedes its entry in the emitted record stream, retaining the
; original FAR-call fixup before the stream-table address fixup.
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

remaining      equ -6
stream_offset  equ -4
stream_segment equ -2

_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __xfflush

org 23
exit_stream:
    les bx,[bp+stream_offset]
    test byte ptr es:[bx+FILE_FLAGS],F_RDWR
    je exit_stream_visited
    push word ptr [bp+stream_segment]
    push bx
    call _fflush
    pop cx
    pop cx
exit_stream_visited:
    dec word ptr [bp+remaining]
    add word ptr [bp+stream_offset],FILE_BYTES
exit_stream_test:
    cmp word ptr [bp+remaining],0
    jne exit_stream
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

org 0
__xfflush label far
    push bp
    mov bp,sp
    sub sp,6
    push si
    push di
    mov word ptr [bp+remaining],4
    mov [bp+stream_segment],ds
    mov word ptr [bp+stream_offset],offset DGROUP:__streams
    jmp short exit_stream_test
_TEXT ends
end
