; Complete original Japanese CRT ctype DATA/metadata owner.
.8086
include char_tables.inl
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
public __ctype
__ctype label byte
CRT_CTYPE_TABLE
_DATA ends
end
