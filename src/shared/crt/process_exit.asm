; Process termination: original LIFO callbacks and quick/returning variants.
; The private near engine removes its three argument words with RET 6.
; Public wrappers precede DATA callbacks, followed by the returning wrappers.
.8086
extrn __atexitcnt:word, __atexittbl:byte, __terminate:far
extrn __cleanup:far, __checknull:far, __restorezero:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
exit_noop_callback proc far private
    push si
    push di
    pop di
    pop si
    retf
exit_noop_callback endp
exit_engine label near
; Bind the backward loop before emitting its separately ordered test span.
org 18
run_atexit label near
org 80
terminate_process:
    push word ptr [bp+4]
    call __terminate
    pop cx
exit_engine_return:
    pop di
    pop si
    pop bp
    ret 6
org 76
    call dword ptr DGROUP:__exitopen
org 72
    call dword ptr DGROUP:__exitfopen
org 55
    call __checknull
    cmp word ptr [bp+6],0
    jne short exit_engine_return
    cmp word ptr [bp+8],0
    jne short terminate_process
org 50
restore_runtime_state:
    call __restorezero
org 46
    call dword ptr DGROUP:__exitbuf
org 41
    call __cleanup
org 34
check_at_exit:
    cmp word ptr DGROUP:__atexitcnt,0
    jne short run_atexit
org 30
    call dword ptr DGROUP:__atexittbl[bx]
org 22
    mov bx,word ptr DGROUP:__atexitcnt
    mov cl,2
    shl bx,cl
org 18
    dec word ptr DGROUP:__atexitcnt
org 5
    push bp
    mov bp,sp
    push si
    push di
    cmp word ptr [bp+8],0
    jne short restore_runtime_state
    jmp short check_at_exit
org 95
public _exit
_exit proc far
    push bp
    mov bp,sp
    push si
    push di
    xor ax,ax
    push ax
    push ax
    push word ptr [bp+6]
    call near ptr exit_engine
    pop di
    pop si
    pop bp
    retf
_exit endp
org 114
public __exit
__exit proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,1
    push ax
    xor ax,ax
    push ax
    push word ptr [bp+6]
    call near ptr exit_engine
    pop di
    pop si
    pop bp
    retf
__exit endp
_TEXT ends
_DATA segment word public 'DATA'
public __exitbuf
__exitbuf label dword
org 4
public __exitfopen
__exitfopen label dword
org 8
public __exitopen
__exitopen label dword
; Genuine symbolic FAR pointers, initialized in original fixup chronology.
org 8
    dd exit_noop_callback
org 4
    dd exit_noop_callback
org 0
    dd exit_noop_callback
_DATA ends
_TEXT segment byte public 'CODE'
org 136
public __cexit
__cexit proc far
    push si
    push di
    xor ax,ax
    push ax
    mov ax,1
    push ax
    xor ax,ax
    push ax
    call near ptr exit_engine
    pop di
    pop si
    retf
__cexit endp
org 154
public __c_exit
__c_exit proc far
    push si
    push di
    mov ax,1
    push ax
    push ax
    xor ax,ax
    push ax
    call near ptr exit_engine
    pop di
    pop si
    retf
__c_exit endp
_TEXT ends
end
