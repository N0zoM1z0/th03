; Exact MAIN VS.ASM storage-only owner. No executable CODE is defined.
; The original 8-byte initialized DATA contribution contains a 7-byte
; VSYNC callback/delay/mask state followed by a historical assembler NOP
; alignment byte. The BSS contribution owns the two counters and old vector.
; Counter/interrupt procedures live in the master-library graph, not here.
.386
_TEXT segment word public 'CODE' use16
_TEXT ends
_DATA segment word public 'DATA' use16
public _vsync_Proc, vsync_Proc
_vsync_Proc label dword
vsync_Proc dd 0
public _vsync_Delay, vsync_Delay
_vsync_Delay label word
vsync_Delay dw 0
public vsync_OldMask, _vsync_OldMask
vsync_OldMask label byte
_vsync_OldMask db 0
; This initialized DATA contribution is 7 bytes before alignment.
; The original master-library storage uses the NOP mnemonic for the
; eighth byte. It is DATA alignment, never executable program CODE.
    nop
_DATA ends
_BSS segment word public 'BSS' use16
public _vsync_Count1, vsync_Count1
_vsync_Count1 label word
vsync_Count1 dw ?
public _vsync_Count2, vsync_Count2
_vsync_Count2 label word
vsync_Count2 dw ?
public _vsync_OldVect, vsync_OldVect
_vsync_OldVect label dword
vsync_OldVect dd ?
_BSS ends
DGROUP group _DATA, _BSS
end
