; Original Japanese Borland fmemicmp: complete native CRT member.
; Preserve far interfaces, original unchecked arithmetic and ordered relocations.
.8086
extrn __ftoupper:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __fmemicmp
include memicmp_body.inl
MEMORY_CASE_COMPARE __fmemicmp,__ftoupper
_TEXT ends
end
