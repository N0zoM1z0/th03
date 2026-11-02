; Borland DOS large-model far cdecl memchr. Search a counted far byte
; span forward; return its matching address as DX:AX or 0000:0000.
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _memchr
_memchr proc far
    push bp
    mov bp,sp
    push si
    push di
    les di,dword ptr [bp+6]
    mov cx,[bp+12]
    jcxz short no_match
    mov al,[bp+10]
    cld
    repne scasb
    je short match
no_match:
    xor di,di
    mov es,di
    mov di,1
match:
    dec di
    mov ax,di
    mov dx,es
    pop di
    pop si
    pop bp
    retf
_memchr endp
_TEXT ends
; BSS-before-DATA is also observable for the two zero-length owners.
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
end
