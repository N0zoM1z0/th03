; Original Borland 32-bit LCG random generator with persistent seed.
; Both FAR srand and rand APIs, using the actual native near
; N_LXMUL@ 32-bit multiply and the original 15-bit return mask.
.8086
extrn N_LXMUL@:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _srand,_rand

_srand proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    mov word ptr DGROUP:rand_seed+2,0
    mov word ptr DGROUP:rand_seed,ax
    pop di
    pop si
    pop bp
    retf
_srand endp

_rand proc far
    push si
    push di
    mov cx,word ptr DGROUP:rand_seed+2
    mov bx,word ptr DGROUP:rand_seed
    mov dx,015ah
    mov ax,04e35h
    call N_LXMUL@
    add ax,1
    adc dx,0
    mov word ptr DGROUP:rand_seed+2,dx
    mov word ptr DGROUP:rand_seed,ax
    mov ax,word ptr DGROUP:rand_seed+2
    and ax,7fffh
    pop di
    pop si
    retf
_rand endp
_TEXT ends
_DATA segment word public 'DATA'
rand_seed dd 1
_DATA ends
end
