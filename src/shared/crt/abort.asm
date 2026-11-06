; Raise SIGABRT, then enter the runtime's unconditional abort fallback.
; Keep the original far ABI, including SI/DI preservation on fallback return.
; Emit the fallback continuation first, as in the original literal fixup list.
; Both ordinary instruction spans cover the complete 20-byte function: no gaps.
.8086
extrn _raise:far,__abort:far
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _abort

org 12
abort_fallback:
    call __abort
    pop di
    pop si
    retf

org 0
_abort label far
    push si
    push di
    mov ax,22
    push ax
    call _raise
    pop cx
; Execution falls through to abort_fallback at the end of this span.
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
end
