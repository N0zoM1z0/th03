; Shared stdio: physical offsets plus buffered/text-mode position accounting.
; The private near-Pascal helper remains at zero and retains RET 4.
; Emit original logical blocks in literal fixup order; spans cover all 492 bytes.
.8086
include stdio_layout.inc
extrn _fflush:far,_lseek:far,__openfd:word
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
buffered_bytes proc near private
    push bp
    mov bp,sp
    sub sp,6
    push si
    push di
    les bx,[bp+4]
    cmp word ptr es:[bx+FILE_LEVEL],0
    jge input_level
    mov cx,es:[bx+FILE_BSIZE]
    add cx,es:[bx+FILE_LEVEL]
    inc cx
    mov ax,cx
    jmp short level_counted
 input_level:
    les bx,[bp+4]
    mov ax,es:[bx+FILE_LEVEL]
    cwd
    xor ax,dx
    sub ax,dx
    mov cx,ax
 level_counted:
    mov [bp-2],ax
    les bx,[bp+4]
    test byte ptr es:[bx+FILE_FLAGS],F_BIN
    jne count_done
    les bx,[bp+4]
    mov dx,es:[bx+FILE_CURP+2]
    mov ax,es:[bx+FILE_CURP]
    mov [bp-4],dx
    mov [bp-6],ax
    cmp word ptr es:[bx+FILE_LEVEL],0
    jge input_text_test
    jmp short output_text_test
 output_text:
    dec word ptr [bp-6]
    les bx,[bp-6]
    cmp byte ptr es:[bx],10
    jne output_text_test
    inc word ptr [bp-2]
 output_text_test:
    mov ax,cx
    dec cx
    or ax,ax
    jne output_text
    jmp short count_done
 input_text:
    les bx,[bp-6]
    inc word ptr [bp-6]
    cmp byte ptr es:[bx],10
    jne input_text_test
    inc word ptr [bp-2]
 input_text_test:
    mov ax,cx
    dec cx
    or ax,ax
    jne input_text
 count_done:
    mov ax,[bp-2]
    pop di
    pop si
    mov sp,bp
    pop bp
    ret 4
buffered_bytes endp
public _fseek,_ftell
; Define both original exports before scheduling the instruction spans.
_fseek label far
org 267
_ftell label far

org 390
 restore_position:
    xor ax,ax
    push ax
    push word ptr [bp-2]
    push word ptr [bp-4]
    les bx,[bp+6]
    mov al,es:[bx+FILE_FD]
    cbw
    push ax
    call _lseek
    add sp,8
    cmp dx,-1
    jne use_append_end
    cmp ax,word ptr -1
    jne use_append_end
    mov dx,-1
    mov ax,-1
    jmp short tell_done
 use_append_end:
    mov dx,[bp-6]
    mov ax,[bp-8]
    mov [bp-2],dx
    mov [bp-4],ax
 add_pending:
    push word ptr [bp+8]
    push word ptr [bp+6]
    call buffered_bytes
    cwd
    add [bp-4],ax
    adc [bp-2],dx
    jmp short tell_return_position
 tell_input:
    push word ptr [bp+8]
    push word ptr [bp+6]
    call buffered_bytes
    cwd
    sub [bp-4],ax
    sbb [bp-2],dx
 tell_return_position:
    mov dx,[bp-2]
    mov ax,[bp-4]
 tell_done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

org 347
    mov ax,2
    push ax
    xor ax,ax
    push ax
    push ax
    mov bx,[bp+6]
    mov al,es:[bx+FILE_FD]
    cbw
    push ax
    call _lseek
    add sp,8
    mov [bp-6],dx
    mov [bp-8],ax
    cmp dx,-1
    jne restore_position
    cmp ax,word ptr -1
    jne restore_position
    jmp short tell_done

org 331
 tell_output:
    mov al,es:[bx+FILE_FD]
    cbw
    add ax,ax
    mov bx,ax
    test byte ptr DGROUP:__openfd[bx+1],O_APPEND shr 8
    je add_pending

org 267
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    mov ax,1
    push ax
    xor ax,ax
    push ax
    push ax
    les bx,[bp+6]
    mov al,es:[bx+FILE_FD]
    cbw
    push ax
    call _lseek
    add sp,8
    mov [bp-2],dx
    mov [bp-4],ax
    cmp dx,-1
    jne tell_buffered
    cmp ax,word ptr -1
    jne tell_buffered
    jmp tell_return_position
 tell_buffered:
    les bx,[bp+6]
    cmp word ptr es:[bx+FILE_LEVEL],0
    jl tell_output
    jmp tell_input

org 164
 adjust_relative:
    cmp word ptr [bp+14],1
    jne reset_stream
    les bx,[bp+6]
    cmp word ptr es:[bx+FILE_LEVEL],0
    jle reset_stream
    push word ptr [bp+8]
    push bx
    call buffered_bytes
    cwd
    sub [bp+10],ax
    sbb [bp+12],dx
 reset_stream:
    les bx,[bp+6]
    and word ptr es:[bx+FILE_FLAGS],not (F_EOF or F_IN or F_OUT)
    mov word ptr es:[bx+FILE_LEVEL],0
    mov dx,es:[bx+FILE_BUFFER+2]
    mov ax,es:[bx+FILE_BUFFER]
    mov es:[bx+FILE_CURP+2],dx
    mov es:[bx+FILE_CURP],ax
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]
    mov al,es:[bx+FILE_FD]
    cbw
    push ax
    call _lseek
    add sp,8
    cmp dx,-1
    jne seek_success
    cmp ax,word ptr -1
    jne seek_success
    mov ax,-1
    jmp short seek_done
 seek_success:
    xor ax,ax
 seek_done:
    pop di
    pop si
    pop bp
    retf

org 137
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    call _fflush
    pop cx
    pop cx
    or ax,ax
    je adjust_relative
    mov ax,-1
    jmp short seek_done
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
end
