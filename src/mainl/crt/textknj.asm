; Borland console Kanji output mode setter: full original API and
; direct framed reference to its named global word.
.8086
extrn __wkanji:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _textkanji
_textkanji:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    mov DGROUP:__wkanji,ax
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
