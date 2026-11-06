; Original Japanese Borland _stpcpy: complete native CRT member.
; Preserve far interfaces, original unchecked arithmetic and ordered relocations.
.8086
extrn _memcpy:far
extrn _strlen:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __stpcpy
include stpcpy_body.inl
COPY_STRING_END __stpcpy
_TEXT ends
end
