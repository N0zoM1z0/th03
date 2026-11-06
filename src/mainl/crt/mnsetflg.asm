; Original Japanese Borland mnsetflg: complete native stream member.
; Preserve 16-bit near/far/Pascal ABI, original callbacks and unchecked behavior.
.8086
extrn @$bnew$qui:far
extrn @ios@setf$ql:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @setiosflags$ql
include stream_flag_manip_body.inl
STREAM_FLAG_MANIP @setiosflags$ql,@ios@setf$ql
_TEXTA ends
end
