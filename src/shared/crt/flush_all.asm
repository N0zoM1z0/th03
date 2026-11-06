; Count open FILE slots visited, including slots whose fflush call fails.
; Retain the original postdecrement loop and unchecked 16-bit stream count.
; Emit loop, stream setup, then entry/count setup to preserve all three
; original literal fixups. The three instruction spans have no gaps.
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

visited_count  equ -8
remaining      equ -6
stream_offset  equ -4
stream_segment equ -2

_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _flushall

org 29
next_stream:
    les bx,[bp+stream_offset]
    test byte ptr es:[bx+FILE_FLAGS],F_RDWR
    je stream_visited
    push word ptr [bp+stream_segment]
    push bx
    call _fflush
    pop cx
    pop cx
    inc word ptr [bp+visited_count]
stream_visited:
    add word ptr [bp+stream_offset],FILE_BYTES
next_stream_test:
    mov ax,[bp+remaining]
    dec word ptr [bp+remaining]
    or ax,ax
    jne next_stream
    mov ax,[bp+visited_count]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

org 19
    mov [bp+stream_segment],ds
    mov word ptr [bp+stream_offset],offset DGROUP:__streams
    jmp short next_stream_test

org 0
_flushall label far
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    mov word ptr [bp+visited_count],0
    mov ax,DGROUP:__nfile
    mov [bp+remaining],ax
; Execution falls through to stream setup at +19.
_TEXT ends
end
