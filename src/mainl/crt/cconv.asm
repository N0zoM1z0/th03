; Reconstructed Japanese original Borland CRT localeconv.
; Original 16-bit ABI, real instructions and symbolic references.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _localeconv
_localeconv proc far
    push si
    push di
    mov dx,ds
    mov ax,offset DGROUP:__localeconvention
    pop di
    pop si
    retf
_localeconv endp
_TEXT ends
_DATA segment word public 'DATA'
public __localeconvention
__localeconvention label byte
    dd DGROUP:locale_decimal_point
    dd DGROUP:locale_empty_50
    dd DGROUP:locale_empty_51
    dd DGROUP:locale_empty_52
    dd DGROUP:locale_empty_53
    dd DGROUP:locale_empty_54
    dd DGROUP:locale_empty_55
    dd DGROUP:locale_empty_56
    dd DGROUP:locale_empty_57
    dd DGROUP:locale_empty_58
    ; Eight original CHAR_MAX sentinel fields for locale numeric formats.
    db 7fh,7fh,7fh,7fh,7fh,7fh,7fh,7fh
locale_decimal_point db '.',0
locale_empty_50 db 0
locale_empty_51 db 0
locale_empty_52 db 0
locale_empty_53 db 0
locale_empty_54 db 0
locale_empty_55 db 0
locale_empty_56 db 0
locale_empty_57 db 0
locale_empty_58 db 0
_DATA ends
end
