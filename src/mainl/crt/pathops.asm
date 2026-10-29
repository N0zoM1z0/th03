; DOS DBCS lead-range acquisition and path-byte classification.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
public ___path_dbcs_vector,___path_dbcs_default
___path_dbcs_vector dw 0,0
; Empty fallback range list: six lower/upper BYTE pairs, first pair terminates.
___path_dbcs_default dw 0,0,0,0,0,0
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
path_initialize proc near
    ; Original8086 save sequence includes PUSH SP and discards it via POP BX.
    push ax
    push cx
    push dx
    push bx
    push sp
    push bp
    push si
    push di
    push ds
    push es
    mov bp,sp
    mov ax,DGROUP:___path_dbcs_vector
    or ax,DGROUP:___path_dbcs_vector+2
    jne initialization_done
    mov si,0ffffh
    push ds
    mov ax,6300h
    clc
    int 21h
    mov ax,ds
    pop ds
    jc fallback_ranges
    mov dx,ds
    cmp ax,dx
    je fallback_ranges
    cmp si,-1
    jne save_ranges
 fallback_ranges:
    mov si,offset DGROUP:___path_dbcs_default
    mov ax,seg DGROUP:___path_dbcs_default
 save_ranges:
    mov DGROUP:___path_dbcs_vector,si
    mov DGROUP:___path_dbcs_vector+2,ax
 initialization_done:
    mov sp,bp
    pop es
    pop ds
    pop di
    pop si
    pop bp
    pop bx
    pop bx
    pop dx
    pop cx
    pop ax
    ret
path_initialize endp
public ___path_isdbcsleadbyte,___path_issbcs
___path_isdbcsleadbyte proc far
    push bp
    mov bp,sp
    push si
    push di
    mov al,[bp+6]
    xor cx,cx
    les bx,dword ptr DGROUP:___path_dbcs_vector
 next_lead_range:
    mov dx,es:[bx]
    or dx,dx
    je lead_classified
    cmp al,dl
    jb lead_classified
    inc bx
    inc bx
    cmp al,dh
    ja next_lead_range
    inc cx
 lead_classified:
    xchg cx,ax
    pop di
    pop si
    pop bp
    retf
___path_isdbcsleadbyte endp
; Scan from start through candidate offset. State0=SBCS,1=lead,2=trail;
; a NUL clears the state. Comparison deliberately uses only the offset WORD.
___path_issbcs proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    xor cx,cx
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-2],dx
    mov [bp-4],ax
 classify_byte:
    les bx,[bp-4]
    cmp byte ptr es:[bx],0
    jne classify_nonzero
    xor cx,cx
    jmp short byte_classified
 classify_nonzero:
    cmp cx,1
    jne classify_lead
    mov cx,2
    jmp short compare_candidate
 classify_lead:
    les bx,[bp-4]
    mov al,es:[bx]
    push ax
    push cs
    call near ptr ___path_isdbcsleadbyte
    pop cx
    or ax,ax
    je classify_sbcs
    mov cx,1
    jmp short compare_candidate
 classify_sbcs:
    xor cx,cx
 compare_candidate:
    mov ax,[bp-4]
    cmp ax,[bp+10]
    jae byte_classified
    inc word ptr [bp-4]
    jmp short classify_byte
 byte_classified:
    or cx,cx
    jne is_dbcs
    mov ax,1
    jmp short sbcs_done
 is_dbcs:
    xor ax,ax
 sbcs_done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
___path_issbcs endp
_TEXT ends
_INIT_ segment word public 'INITDATA'
    db 0,15
    dw offset path_initialize
    dw 0
_INIT_ ends
end
