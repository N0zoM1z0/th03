; Original Japanese Borland isteush: complete stream member.
; Original 16-bit ABI, result/state behavior and ordered relocation are retained.
.8086
extrn @istream@$brsh$qmul:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @istream@$brsh$qmus
include stream_int_extract.inl
STREAM_INTEGER_EXTRACT @istream@$brsh$qmus,@istream@$brsh$qmul,1
_TEXTA ends
end
