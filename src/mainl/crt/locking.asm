; Original large-model DOS file locking, including the ten-tick wait retry.
; The private near procedure samples DOS time across minute rollover;
; the public far entry selects one of five original DOS lock modes.
.8086
extrn __dos_lock:far,__dos_seek:far,__dos_unlock:far
extrn __dos_gettime:far,_errno:word
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

wait_one_second proc near
    push bp
    mov bp,sp
    sub sp,10
    push si
    push di
    push ss
    lea ax,[bp-4]
    push ax
    call __dos_gettime
    pop cx
    pop cx
    cmp byte ptr [bp-2],59
    jnz short not_last_minute
    mov byte ptr [bp-9],0
    jmp short first_sample
not_last_minute:
    mov al,[bp-2]
    inc al
    mov [bp-9],al
first_sample:
    push ss
    lea ax,[bp-8]
    push ax
    call __dos_gettime
    pop cx
    pop cx
    mov al,[bp-6]
    cmp al,[bp-2]
    jz short first_sample
    jmp short check_second
wait_second:
    push ss
    lea ax,[bp-8]
    push ax
    call __dos_gettime
    pop cx
    pop cx
check_second:
    mov al,[bp-6]
    cmp al,[bp-9]
    jnz short wait_done
    mov al,[bp-5]
    cmp al,[bp-1]
    jc short wait_second
wait_done:
    pop di
    pop si
    mov sp,bp
    pop bp
    ret
wait_one_second endp

public _locking
_locking proc far
    push bp
    mov bp,sp
    sub sp,6
    push si
    push di
    push ss
    lea ax,[bp-6]
    push ax
    mov ax,1
    push ax
    xor ax,ax
    push ax
    push ax
    push word ptr [bp+6]
    call __dos_seek
    add sp,12
    or ax,ax
    jz short select_operation
    jmp near ptr failed
select_operation:
    mov bx,[bp+8]
    cmp bx,4
    jna short valid_operation
    jmp near ptr invalid_operation
valid_operation:
    add bx,bx
    jmp word ptr cs:[bx+offset lock_table]
retry_lock:
    mov word ptr [bp-2],1
    jmp short retry_check
lock_once:
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp-4]
    push word ptr [bp-6]
    push word ptr [bp+6]
    call __dos_lock
    add sp,10
    or ax,ax
    jnz short check_retry_error
    xor ax,ax
    jmp short return_value
check_retry_error:
    cmp word ptr DGROUP:_errno,5
    jz short backoff
    jmp short failed
backoff:
    call wait_one_second
    inc word ptr [bp-2]
retry_check:
    cmp word ptr [bp-2],10
    jng short lock_once
    mov word ptr DGROUP:_errno,24h
    jmp short failed
unlock_once:
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp-4]
    push word ptr [bp-6]
    push word ptr [bp+6]
    call __dos_lock
    add sp,10
    or ax,ax
    jnz short unlock_error
    jmp short unlock_success
unlock_fallback:
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp-4]
    push word ptr [bp-6]
    push word ptr [bp+6]
    call __dos_unlock
    add sp,10
    or ax,ax
    jnz short unlock_error
unlock_success:
    xor ax,ax
    jmp short return_after_unlock
unlock_error:
    mov ax,0FFFFh
return_after_unlock:
    jmp short return_value
invalid_operation:
    mov word ptr DGROUP:_errno,13h
failed:
    mov ax,0FFFFh
return_value:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_locking endp

; Original jump table is a relocatable code data region, not instructions.
lock_table label word
    dw offset unlock_fallback, offset retry_lock, offset unlock_once
    dw offset retry_lock, offset unlock_once
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
end
