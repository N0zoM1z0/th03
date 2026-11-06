; Original Japanese Borland _abort: complete native runtime/process member.
; Original ABI, argument traversal, callbacks and unchecked behavior are retained.
.8086
extrn ___ErrorMessage:far
extrn __exit:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
termination_message db 'Abnormal program termination',13,10,0
_DATA ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __abort
; Original statement chunks preserve native relocation chronology.

org 16
    call __exit
    add sp, 6
    pop di
    pop si
    retf

org 7
    call ___ErrorMessage
    mov ax, 3
    push ax

org 3
    mov ax,offset DGROUP:termination_message
    push ax

org 0
__abort label far
    push si
    push di
    push ds
_TEXT ends
end
