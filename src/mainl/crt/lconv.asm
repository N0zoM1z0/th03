; Original Borland localeconv FAR ABI, based on the live locale object.
; Initializes ten far string pointers plus eight locale numeric flags.
.8086
extrn __pLocale:dword
extrn __localeconvention:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __llocaleconv
__llocaleconv proc far
    push si
    push di
    mov dx,word ptr DGROUP:__pLocale+2
    mov ax,word ptr DGROUP:__pLocale
    add ax,218h
    mov word ptr DGROUP:__localeconvention+2,dx
    mov word ptr DGROUP:__localeconvention,ax
    mov ax,word ptr DGROUP:__pLocale
    add ax,21ah
    mov word ptr DGROUP:__localeconvention+6,dx
    mov word ptr DGROUP:__localeconvention+4,ax
    mov ax,word ptr DGROUP:__pLocale
    add ax,224h
    mov word ptr DGROUP:__localeconvention+0ah,dx
    mov word ptr DGROUP:__localeconvention+8,ax
    mov ax,word ptr DGROUP:__pLocale
    add ax,1cch
    mov word ptr DGROUP:__localeconvention+0eh,dx
    mov word ptr DGROUP:__localeconvention+0ch,ax
    mov ax,word ptr DGROUP:__pLocale
    add ax,1d1h
    mov word ptr DGROUP:__localeconvention+12h,dx
    mov word ptr DGROUP:__localeconvention+10h,ax
    mov ax,word ptr DGROUP:__pLocale
    add ax,1d6h
    mov word ptr DGROUP:__localeconvention+16h,dx
    mov word ptr DGROUP:__localeconvention+14h,ax
    mov ax,word ptr DGROUP:__pLocale
    add ax,1d8h
    mov word ptr DGROUP:__localeconvention+1ah,dx
    mov word ptr DGROUP:__localeconvention+18h,ax
    mov ax,word ptr DGROUP:__pLocale
    add ax,1ddh
    mov word ptr DGROUP:__localeconvention+1eh,dx
    mov word ptr DGROUP:__localeconvention+1ch,ax
    mov ax,word ptr DGROUP:__pLocale
    add ax,1e2h
    mov word ptr DGROUP:__localeconvention+22h,dx
    mov word ptr DGROUP:__localeconvention+20h,ax
    mov ax,word ptr DGROUP:__pLocale
    add ax,1e7h
    mov word ptr DGROUP:__localeconvention+26h,dx
    mov word ptr DGROUP:__localeconvention+24h,ax
    les bx,dword ptr DGROUP:__pLocale
    mov al,byte ptr es:[bx+1ech]
    mov byte ptr DGROUP:__localeconvention+28h,al
    mov al,byte ptr es:[bx+1edh]
    mov byte ptr DGROUP:__localeconvention+29h,al
    mov al,byte ptr es:[bx+1eeh]
    mov byte ptr DGROUP:__localeconvention+2ah,al
    mov al,byte ptr es:[bx+1efh]
    mov byte ptr DGROUP:__localeconvention+2bh,al
    mov al,byte ptr es:[bx+1f0h]
    mov byte ptr DGROUP:__localeconvention+2ch,al
    mov al,byte ptr es:[bx+1f1h]
    mov byte ptr DGROUP:__localeconvention+2dh,al
    mov al,byte ptr es:[bx+1f2h]
    mov byte ptr DGROUP:__localeconvention+2eh,al
    mov al,byte ptr es:[bx+1f3h]
    mov byte ptr DGROUP:__localeconvention+2fh,al
    mov dx,ds
    mov ax,offset DGROUP:__localeconvention
    pop di
    pop si
    retf
__llocaleconv endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
