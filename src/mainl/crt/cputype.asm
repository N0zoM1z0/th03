; Original Japanese Borland cputype: complete platform/runtime member.
; Preserve register ABI, interrupt behavior, storage and native relocation order.
.386
_TEXT segment byte use16 public 'CODE'
_TEXT ends
_DATA segment word use16 public 'DATA'
_DATA ends
_INIT_ segment word use16 public 'INITDATA'
_INIT_ ends
DGROUP group _DATA
_DATA segment word use16 public 'DATA'
public __8086
__8086 dw 0
_DATA ends
_INIT_ segment word use16 public 'INITDATA'
; Native near startup record; its unused segment word is uninitialized.
db 0,16
dw offset detect_cpu
dw ?
_INIT_ ends
_TEXT segment byte use16 public 'CODE'
assume cs:_TEXT,ds:DGROUP
; Complete disjoint instruction chunks follow original OMF field chronology.

org 17
    mov word ptr DGROUP:__8086, 0
    je short cpu_detect_return
    or bx, 0f000h
    push bx
    popf
    pushf
    pop ax
    and ax, 0f000h

org 36
    mov word ptr DGROUP:__8086, 2
    je short cpu_detect_return
    mov edx, esp
    and sp, 0fffch
    pushfd
    pop eax
    mov ecx, eax
    xor eax, 040000h
    push eax
    popfd
    pushfd
    pop eax
    xor eax, ecx

org 74
    mov word ptr DGROUP:__8086, 3
    mov esp, edx
    je short cpu_detect_return

org 85
    mov word ptr DGROUP:__8086, 4
cpu_detect_return:
    ret

org 0
; FLAGS high bits distinguish 8086/286; AC toggling distinguishes 386/486.
; Save full ESP before aligning SP for the dword FLAGS temporary.
detect_cpu:
    pushf
    pop bx
    mov ax, 0fffh
    and ax, bx
    push ax
    popf
    pushf
    pop ax
    and ax, 0f000h
    cmp ax, 0f000h
_TEXT ends
end
