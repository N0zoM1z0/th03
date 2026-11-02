; Natural 8086 qsort reconstructed from original swap/partition/entry ABI.
; No embedded original machine-code bytes or post-link object patches.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
qsort_compare dd ?
qsort_width dw ?
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
extrn N_LXMUL@:near
extrn N_LDIV@:near
include qswap.inl
include qcore.inl
include qentry.inl
_TEXT ends
end
