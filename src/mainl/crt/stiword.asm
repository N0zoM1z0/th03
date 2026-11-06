; Original ios::iword(int): FAR long user-slot lookup with genuine
; ios::usersize expansion, original 4-byte static invalid-slot sentinel.
.8086
extrn @ios@usercount:word
extrn @ios@usersize$qi:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ios@iword$qi
@ios@iword$qi proc far
    push bp
    mov bp,sp
    push si
    push di
    cmp word ptr [bp+0ah],1
    jl short invalid_iword_slot
    mov ax,word ptr DGROUP:@ios@usercount
    cmp ax,word ptr [bp+0ah]
    jge short check_allocated_slots
invalid_iword_slot:
    mov dx,ds
    mov ax,offset DGROUP:invalid_slot
    jmp short iword_done
check_allocated_slots:
    les bx,dword ptr [bp+6]
    mov ax,word ptr es:[bx+26h]
    cmp ax,word ptr [bp+0ah]
    jge short check_new_size
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push bx
    call @ios@usersize$qi
    add sp,6
check_new_size:
    les bx,dword ptr [bp+6]
    mov ax,word ptr es:[bx+26h]
    cmp ax,word ptr [bp+0ah]
    jge short have_iword_slot
    mov dx,ds
    mov ax,offset DGROUP:invalid_slot
    jmp short iword_done
have_iword_slot:
    les bx,dword ptr [bp+6]
    mov dx,word ptr es:[bx+24h]
    mov ax,word ptr es:[bx+22h]
    mov bx,word ptr [bp+0ah]
    dec bx
    mov cl,2
    shl bx,cl
    add ax,bx
iword_done:
    pop di
    pop si
    pop bp
    retf
@ios@iword$qi endp
_TEXTA ends
_DATA segment word public 'DATA'
invalid_slot dd 0
_DATA ends
end
