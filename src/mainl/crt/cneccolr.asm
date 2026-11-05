; Original NEC PC-98 text color and attribute runtime.
; Four sixteen-WORD lookup tables are real initialized DATA, not code
; payloads. The two background modes retain their original video ABI.
.8086
extrn __video:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
; Match Borland's original DATA-first DGROUP record; TASM preserves its
; 08ff02ff03 order with the completed SEGDEFs and this declaration.
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

public ___nec_textcolor
___nec_textcolor proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    test byte ptr DGROUP:__video+8,4
    jz short default_text_color
    and word ptr DGROUP:__video+4,0f81fh
    mov bx,ax
    and bx,15
    jmp short color_lookup
default_text_color:
    and word ptr DGROUP:__video+4,1fh
    mov bx,ax
    and bx,7
color_lookup:
    add bx,bx
    mov ax,word ptr DGROUP:foreground_palette[bx]
    or word ptr DGROUP:__video+4,ax
    pop di
    pop si
    pop bp
    retf
___nec_textcolor endp

public ___nec_textbackground
___nec_textbackground proc far
    push bp
    mov bp,sp
    push si
    push di
    test byte ptr DGROUP:__video+8,4
    jz short background_done
    and word ptr DGROUP:__video+4,0cffh
    mov bx,[bp+6]
    and bx,15
    add bx,bx
    mov ax,word ptr DGROUP:background_palette[bx]
    or word ptr DGROUP:__video+4,ax
background_done:
    pop di
    pop si
    pop bp
    retf
___nec_textbackground endp

public ___nec_textattr
___nec_textattr proc far
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+6]
    test byte ptr DGROUP:__video+8,4
    jz short monochrome_attr
    mov bx,dx
    and bx,15
    add bx,bx
    mov ax,word ptr DGROUP:foreground_palette[bx]
    mov bx,dx
    mov cl,4
    sar bx,cl
    and bx,15
    add bx,bx
    or ax,word ptr DGROUP:background_palette[bx]
    mov bx,dx
    mov cl,8
    sar bx,cl
    and bx,31
    jmp short insert_special_attr
monochrome_attr:
    mov bx,dx
    and bx,7
    add bx,bx
    mov ax,word ptr DGROUP:foreground_palette[bx]
    mov bx,dx
    mov cl,8
    sar bx,cl
    and bx,15
insert_special_attr:
    add bx,bx
    or ax,word ptr DGROUP:attribute_palette[bx]
    mov word ptr DGROUP:__video+4,ax
    pop di
    pop si
    pop bp
    retf
___nec_textattr endp

public ___nec_highvideo
___nec_highvideo proc far
    push si
    push di
    test byte ptr DGROUP:__video+8,4
    jz short high_done
    or word ptr DGROUP:__video+4,0400h
high_done:
    pop di
    pop si
    retf
___nec_highvideo endp

public ___nec_lowvideo
___nec_lowvideo proc far
    push si
    push di
    test byte ptr DGROUP:__video+8,4
    jz short low_done
    and word ptr DGROUP:__video+4,0fbffh
low_done:
    pop di
    pop si
    retf
___nec_lowvideo endp

public ___nec_normvideo
___nec_normvideo proc far
    push si
    push di
    mov ax,word ptr DGROUP:__video+6
    mov word ptr DGROUP:__video+4,ax
    pop di
    pop si
    retf
___nec_normvideo endp
_TEXT ends

_DATA segment word public 'DATA'
; Each 16-word set encodes original PC-98 text-plane color/attribute bits.
foreground_palette label word
    dw 0001h,0021h,0081h,00a1h,0041h,0061h,00c1h,00e1h
    dw 0401h,0421h,0481h,04a1h,0441h,0461h,04c1h,04e1h
background_palette label word
    dw 0001h,1001h,2001h,3001h,4001h,5001h,6001h,7001h
    dw 8001h,9001h,0a001h,0b001h,0c001h,0d001h,0e001h,0f001h
attribute_palette label word
    dw 0000h,0002h,0004h,0006h,0008h,000ah,000ch,000eh
    dw 0010h,0012h,0014h,0016h,0018h,001ah,001ch,001eh
alternate_attribute_palette label word
    dw 0800h,0802h,0804h,0806h,0808h,080ah,080ch,080eh
    dw 0810h,0812h,0814h,0816h,0818h,081ah,081ch,081eh
_DATA ends
end
