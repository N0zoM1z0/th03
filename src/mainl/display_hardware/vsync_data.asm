; VSync storage alignment compatibility, not a code-function extent.
; ReC98 287d7ea554cc33cf3fe7067f491210c63954e8c0 documents
; replacing the original trailing NOP with zero through DATA EVEN.
; Preserve its word-alignment intent using a mnemonic, never a raw byte.
; origin is a zero-storage label at this DATA contribution's aligned start.
mainl_vsync_storage_even macro origin
    if (($ - origin) and 1)
        nop
    endif
endm

	public _vsync_Proc,vsync_Proc
vsync_Proc label dword
_vsync_Proc	dd	0

	public _vsync_Delay,vsync_Delay
vsync_Delay label word
_vsync_Delay	dw	0

	public vsync_OldMask,_vsync_OldMask
_vsync_OldMask label byte
vsync_OldMask	db	0
    mainl_vsync_storage_even mainl_data_origin
