; Original Japanese Borland environment initializer, CL.LIB member 364.
; Rebuild the real startup _INIT_ record, far environ ownership and
; DOS environment-string scanning; no initialized fake BSS/file bytes.
.8086
extrn _malloc:far,__abort:far
extrn __envseg:word,__envLng:word,__envSize:word,__C0environ:dword
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_INIT_ segment word public 'INITDATA'
_INIT_ ends
DGROUP group _DATA
; The original BCC object exports an *absolute* linker PUBDEF at frame 0,
; distinct from the near initialization routine and ordinary DATA public.
__setenvp__ equ 0
public __setenvp__
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

setenvp_init:
    push si
    push di
    mov es,word ptr __envseg
    xor di,di
    push es
    push word ptr __envSize
    call _malloc
    pop bx
    mov bx,ax
    pop es
    mov word ptr DGROUP:__environ,ax
    mov word ptr DGROUP:__environ+2,dx
    push ds
    mov ds,dx
    or ax,dx
    jnz have_env_list
    jmp __abort

have_env_list:
    xor ax,ax
    mov cx,-1

scan_environment:
    cmp byte ptr es:[di],0
    jz environment_terminated
store_environment_entry:
    mov [bx],di
    mov [bx+2],es
    add bx,4
    repne scasb
    cmp byte ptr es:[di],al
    jnz store_environment_entry

environment_terminated:
    mov [bx],ax
    mov [bx+2],ax
    pop ds
    pop di
    pop si
    ; The original commit direction updates the program's C0environ from
    ; the startup list, preserving the two distinct relocation targets.
    mov ax,word ptr DGROUP:__environ+2
    mov word ptr __C0environ+2,ax
    mov ax,word ptr DGROUP:__environ
    mov word ptr __C0environ,ax
    ret
_TEXT ends

_DATA segment word public 'DATA'
public __environ
__environ dd 0
_DATA ends

; Turbo C++ init-list entry: priority 1000h, relocatable code offset,
; trailing 16-bit state genuinely uninitialized in the original OMF.
_INIT_ segment word public 'INITDATA'
    dw 1000h
    dw offset _TEXT:setenvp_init
    dw ?
_INIT_ ends
end
