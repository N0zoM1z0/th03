; Complete original Japanese CRT clower DATA/metadata owner.
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
public __lower
__lower label byte
CRT_CASE_MAP 1
_DATA ends
end
