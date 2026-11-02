; High-address Borland DOS quicksort native 8086 reconstruction.
; Genuine far pointer arithmetic helpers and original partition algorithm.
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
extrn N_PADD@:near
extrn N_LXMUL@:near
extrn N_PADA@:near
extrn N_PCMP@:near
extrn N_PSBA@:near
extrn N_PSUB@:near
extrn N_PSBP@:near
extrn N_LDIV@:near
include qswap.inl
include hqcore.inl
include hqentry.inl
_TEXT ends
end
