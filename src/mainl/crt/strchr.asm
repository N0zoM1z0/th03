; Borland DOS large-model strchr. Scan with the original alignment-aware
; LODSB/LODSW path; searching for zero returns the first terminator.
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _strchr
_strchr proc far
    push bp
    mov bp,sp
    push si
    push di
    cld
    push ds
    lds si,dword ptr [bp+6]
    mov bl,[bp+10]
    test si,1
    je short aligned
    lodsb
    cmp al,bl
    je short high_byte_found
    and al,al
    je short not_found
aligned:
    lodsw
    cmp al,bl
    je short low_byte_found
    and al,al
    je short not_found
    cmp ah,bl
    je short high_byte_found
    and ah,ah
    jne short aligned
not_found:
    pop ds
    xor dx,dx
    xor ax,ax
    jmp short finish
high_byte_found:
    inc si
low_byte_found:
    lea ax,[si-2]
    mov dx,ds
    pop ds
finish:
    pop di
    pop si
    pop bp
    retf
_strchr endp
_TEXT ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
end
