; Original Japanese Borland ostskpos: complete native stream member.
; Preserve 16-bit near/far/Pascal ABI, original callbacks and unchecked behavior.
.8086
extrn @ios@setstate$qi:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ostream@seekp$ql
include stream_seek_position_body.inl
STREAM_SEEK_POSITION @ostream@seekp$ql,2
_TEXTA ends
end
