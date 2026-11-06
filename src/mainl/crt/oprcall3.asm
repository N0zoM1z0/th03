; Original Japanese Borland mutable string regular-expression slice overload.
; Preserve both native CODE segments, control metadata, far ABI and literal fields.
.8086
extrn @$bnew$qui:far
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn @string@find$xqmx7TRegexpnuiui:far
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
assume cs:_TEXT,ds:DGROUP
include string_empty_unwind.inl
_TEXT ends
_TEXTC segment byte public 'CODE'
assume cs:_TEXTC,ds:DGROUP
public @string@$bcall$qmx7TRegexpui
include string_regexp_slice_body.inl
STRING_REGEXP_SLICE @string@$bcall$qmx7TRegexpui
_TEXTC ends
end
