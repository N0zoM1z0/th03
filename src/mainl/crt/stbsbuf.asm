; Original streambuf::setbuf retains actual setb(buf,buf+n,0) ABI.
.8086
extrn @streambuf@setb$qnct1i:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @streambuf@setbuf$qnci
@streambuf@setbuf$qnci proc far
    push bp
    mov bp,sp
    push si
    push di
    xor ax,ax
    push ax
    mov ax,[bp+10]
    add ax,[bp+14]
    push word ptr [bp+12]
    push ax
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @streambuf@setb$qnct1i
    add sp,14
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    pop bp
    retf
@streambuf@setbuf$qnci endp
_TEXTA ends
end
