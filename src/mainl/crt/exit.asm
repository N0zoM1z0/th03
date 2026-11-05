; Original Borland CRT process-exit lifecycle: atexit LIFO callbacks,
; cleanup/restore/termination, three dynamic FAR handlers in DATA,
; and four public FAR process exit interfaces.
.8086
extrn __atexitcnt:word
extrn __atexittbl:byte
extrn __terminate:far
extrn __cleanup:far
extrn __checknull:far
extrn __restorezero:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

exit_noop_callback proc far
    push si
    push di
    pop di
    pop si
    retf
exit_noop_callback endp

; Original near CRT exit engine: three caller-popped words.
exit_engine proc near
    push bp
    mov bp,sp
    push si
    push di
    cmp word ptr [bp+8],0
    jne short restore_runtime_state
    jmp short check_at_exit
run_atexit:
    dec word ptr DGROUP:__atexitcnt
    mov bx,word ptr DGROUP:__atexitcnt
    mov cl,2
    shl bx,cl
    call dword ptr DGROUP:__atexittbl[bx]
check_at_exit:
    cmp word ptr DGROUP:__atexitcnt,0
    jne short run_atexit
    call __cleanup
    call dword ptr DGROUP:__exitbuf
restore_runtime_state:
    call __restorezero
    call __checknull
    cmp word ptr [bp+6],0
    jne short exit_engine_return
    cmp word ptr [bp+8],0
    jne short terminate_process
    call dword ptr DGROUP:__exitfopen
    call dword ptr DGROUP:__exitopen
terminate_process:
    push word ptr [bp+4]
    call __terminate
    pop cx
exit_engine_return:
    pop di
    pop si
    pop bp
    ret 6
exit_engine endp

public _exit,__exit,__cexit,__c_exit
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

_DATA segment word public 'DATA'
public __exitbuf,__exitfopen,__exitopen
; Emit the genuine three symbolic FAR callbacks in original Borland
; reverse DATA-FIXUPP chronology, not as raw 12-byte target data.
org 8
__exitopen dd exit_noop_callback
org 4
__exitfopen dd exit_noop_callback
org 0
__exitbuf dd exit_noop_callback
_DATA ends
end
