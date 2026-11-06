; Original Japanese Borland istasn2: complete stream member.
; Original 16-bit ABI, result/state behavior and ordered relocation are retained.
.8086
extrn @ios@init$qn9streambuf:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @istream_withassign@$basg$qn9streambuf
include stream_buf_assign.inl
STREAM_BUFFER_ASSIGNMENT @istream_withassign@$basg$qn9streambuf
_TEXTA ends
end
