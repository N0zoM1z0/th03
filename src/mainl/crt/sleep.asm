; Original Borland DOS sleep: three real FAR _gettime calls, native
; time edge clamp and second rollover polling under original 16-bit ABI.
.8086
extrn _gettime:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _sleep
_sleep proc far
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    push ss
    lea ax,[bp-4]
    push ax
    call _gettime
    pop cx
    pop cx
    cmp byte ptr [bp-2],5ah
    jbe short sleep_keep_start
    mov ax,5ah
    jmp short sleep_start_done
sleep_keep_start:
    mov al,byte ptr [bp-2]
    mov ah,0
sleep_start_done:
    mov word ptr [bp-8],ax
    jmp short sleep_count
sleep_next_second:
    mov al,byte ptr [bp-1]
    mov ah,0
    mov word ptr [bp-6],ax
sleep_wait_second:
    push ss
    lea ax,[bp-4]
    push ax
    call _gettime
    pop cx
    pop cx
    mov al,byte ptr [bp-1]
    mov ah,0
    cmp ax,word ptr [bp-6]
    je short sleep_wait_second
sleep_count:
    mov ax,[bp+6]
    dec word ptr [bp+6]
    or ax,ax
    jne short sleep_next_second
sleep_final_clock:
    push ss
    lea ax,[bp-4]
    push ax
    call _gettime
    pop cx
    pop cx
    mov al,byte ptr [bp-2]
    mov ah,0
    cmp ax,word ptr [bp-8]
    jl short sleep_final_clock
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_sleep endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
