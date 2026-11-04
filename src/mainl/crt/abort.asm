; Borland abort: raise SIGABRT (22), then invoke the runtime abort fallback.
; The original far entry preserves callee-saved SI/DI even on the fallback path.
.8086
extrn _raise:far,__abort:far
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _abort
_abort proc far
    push si
    push di
    mov ax,22
    push ax
    call _raise
    pop cx
    call __abort
    pop di
    pop si
    retf
_abort endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
end
