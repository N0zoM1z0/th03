; Skip the five standard streams; count successful closes with a nonzero FILE temp number.
; Original Japanese Borland rmtmp: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
include stdio_tmp.inc
extrn __streams:byte
extrn __nfile:word
extrn _fclose:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _rmtmp
; Complete disjoint instruction chunks preserve original native field order.

org 66
    cmp ax, word ptr DGROUP:__nfile
    jb short inspect_temporary_stream
    mov ax, word ptr [bp-8]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 42
    call _fclose
    pop cx
    pop cx
    or ax, ax
    jne short advance_stream
    inc word ptr [bp-8]
advance_stream:
    add word ptr [bp-4], FILE_BYTES
    inc word ptr [bp-6]
test_stream_limit:
    mov ax, word ptr [bp-6]

org 16
    mov word ptr [bp-4],offset DGROUP:__streams+5*FILE_BYTES
    mov word ptr [bp-8], 0
    jmp short test_stream_limit
inspect_temporary_stream:
    les bx, dword ptr [bp-4]
    cmp word ptr es:[bx+FILE_TMPNUM], 0
    je short advance_stream
    push word ptr [bp-2]
    push bx

org 0
_rmtmp label far
    push bp
    mov bp, sp
    sub sp, 8
    push si
    push di
    mov word ptr [bp-6], 5
    mov word ptr [bp-2], ds
_TEXT ends
end
