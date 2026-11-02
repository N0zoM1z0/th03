; Original Borland DOS fcloseall: close every active FILE stream.
; Begins after the standard five reserved DOS streams, with a far
; cursor into DGROUP:__streams+100 and __nfile slot count.
; Calls the actual far _fclose for allocated streams, returning the
; original count or -1 on a close failure. No defensive changes.
; Disjoint original instruction blocks maintain descending FIXUPPs.
.8086
extrn __streams:word
extrn __nfile:word
extrn _fclose:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
public _fcloseall
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 049h
    cmp ax,word ptr DGROUP:__nfile
    jb short check_next_stream
    cmp word ptr [bp-8], 0
    jge short return_close_count
    mov ax, 0ffffh
    jmp short closeall_exit
return_close_count:
    mov ax, word ptr [bp-8]
closeall_exit:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 02Ah
    call _fclose
    pop cx
    pop cx
    or ax, ax
    je short count_closed_file
    mov word ptr [bp-8], 0d8f1h
    jmp short advance_stream_pointer
count_closed_file:
    inc word ptr [bp-8]
advance_stream_pointer:
    add word ptr [bp-4], 014h
    inc word ptr [bp-6]
test_end_of_streams:
    mov ax, word ptr [bp-6]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 010h
    mov word ptr [bp-4],offset DGROUP:__streams+100
    mov word ptr [bp-8], 0
    jmp short test_end_of_streams
check_next_stream:
    les bx, dword ptr [bp-4]
    cmp byte ptr es:[bx+4], 0
    jl short advance_stream_pointer
    push word ptr [bp-2]
    push bx
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 00h
_fcloseall label far
    push bp
    mov bp, sp
    sub sp, 8
    push si
    push di
    mov word ptr [bp-6], 5
    mov word ptr [bp-2], ds
_TEXT ends
end
