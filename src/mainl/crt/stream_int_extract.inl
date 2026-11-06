; Original integer extraction ABI: four-byte SS temporary, delegated reader,
; stream-state test, then one or two native WORD stores into the far result.
; result_words=1 retains unchecked truncation; =2 also writes the high WORD.
; Each caller owns its original public and complete 61/68-byte CODE extent.
STREAM_INTEGER_EXTRACT macro api_name,wide_reader,result_words
org 19
    call wide_reader
    add sp,8
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    test byte ptr es:[bx+0ah],086h
    jne short integer_extract_return
    les bx,dword ptr [bp+0ah]
if result_words eq 2
    mov dx,word ptr [bp-2]
endif
    mov ax,word ptr [bp-4]
if result_words eq 2
    mov word ptr es:[bx+2],dx
endif
    mov word ptr es:[bx],ax
integer_extract_return:
    mov dx,word ptr [bp+8]
    mov ax,word ptr [bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

org 0
api_name label far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    push ss
    lea ax,[bp-4]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
endm
