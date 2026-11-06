; Original Japanese Borland files: complete CRT source owner.
; Preserve segment widths, initialized storage and register/near/far ABI.
.8086
include stdio_tmp.inc
extrn __setupio:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
public __streams
__streams label byte
; Twenty original 20-byte FILE records; only five initial self tokens relocate.
CRT_FILE_RECORD macro initial_flags,descriptor,self_token
    dw 0,initial_flags
    db descriptor,0
    dw 0
    dd 0,0
    dw 0,self_token
endm
org 4*FILE_BYTES
CRT_FILE_RECORD <F_TERM or F_BIN or 2>,4,<offset DGROUP:__streams+4*FILE_BYTES>
org 3*FILE_BYTES
CRT_FILE_RECORD <F_TERM or F_BIN or F_RDWR>,3,<offset DGROUP:__streams+3*FILE_BYTES>
org 2*FILE_BYTES
CRT_FILE_RECORD <F_TERM or 2>,2,<offset DGROUP:__streams+2*FILE_BYTES>
org FILE_BYTES
CRT_FILE_RECORD <F_TERM or F_LBUF or 2>,1,<offset DGROUP:__streams+FILE_BYTES>
org 0
CRT_FILE_RECORD <F_TERM or F_LBUF or 1>,0,<offset DGROUP:__streams>
org 5*FILE_BYTES
rept 15
CRT_FILE_RECORD 0,0,0
endm
_DATA ends
end
