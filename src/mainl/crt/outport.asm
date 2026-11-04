; Reconstructed Borland 16-bit large-model outport.
; Original far ABI, semantic branches and normal assembler source.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _outport,_outportb,_outpw,_outp

_outport:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr [bp + 6]
    mov ax, word ptr [bp + 8]
    out dx, ax
    pop di
    pop si
    pop bp
    retf

_outportb:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr [bp + 6]
    mov al, byte ptr [bp + 8]
    out dx, al
    pop di
    pop si
    pop bp
    retf

_outpw:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr [bp + 6]
    mov ax, word ptr [bp + 8]
    out dx, ax
    pop di
    pop si
    pop bp
    retf

_outp:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr [bp + 6]
    mov al, byte ptr [bp + 8]
    out dx, al
    xor ah, ah
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
