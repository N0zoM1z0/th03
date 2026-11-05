; Original empty Borland string constructor-generated cleanup helper.
; No public symbol; the retained unused import is part of the real ABI.
.8086
extrn @__RefDestructorCount$qv:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_TEXTC segment byte public 'CODE'
_TEXTC ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT
constructor_helper:
    push si
    push di
    pop di
    pop si
    retf
_TEXT ends
end
