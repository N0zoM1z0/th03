; Original Japanese Borland NTHCTYPE: complete native CRT member.
; Preserve far interfaces, original unchecked arithmetic and ordered relocations.
.8086
extrn __mbctype:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _nthctype
include mb_nth_type.inl
MB_NTH_TYPE _nthctype
_TEXT ends
end
