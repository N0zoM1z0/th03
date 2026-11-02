; Borland DOS large-model far-cdecl strcmp for the Japanese MAINL CRT.
; First far pointer is SS:[BP+6], second far pointer SS:[BP+10].
; The original scans the second string before comparing against the first.
; AL and BL are unsigned byte results; AX/BX were cleared before the scans.
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _strcmp
_strcmp proc far
    push bp
    mov bp,sp
    push si
    push di
    mov dx,ds
    cld
    xor ax,ax
    mov bx,ax
    les di,dword ptr [bp+10]
    mov si,di
    xor al,al
    mov cx,-1
    repne scasb
    not cx
    mov di,si
    lds si,dword ptr [bp+6]
    repe cmpsb
    mov al,[si-1]
    mov bl,es:[di-1]
    sub ax,bx
    mov ds,dx
    pop di
    pop si
    pop bp
    retf
_strcmp endp
_TEXT ends

; Preserve the empty OMF BSS and DATA owners and their native group order.
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
end
