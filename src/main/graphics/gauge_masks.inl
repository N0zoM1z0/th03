; Existing 16-WORD table at DS:064C (load1DBAC), included in the retained
; root DATA contribution. No additional allocation or alignment directive.
; PC-98 pixels run MSB-first within each byte. Construct a leftmost-width mask
; in pixel order, then swap bytes for a little-endian WORD VRAM store.
; Index0 intentionally means all16 pixels, NOT an empty mask.
public _hud_gauge_left_masks
_hud_gauge_left_masks label word
        dw 0FFFFh
GAUGE_MASK_WIDTH = 1
rept 15
GAUGE_MASK_BITS = ((0FFFFh shl (16 - GAUGE_MASK_WIDTH)) and 0FFFFh)
        dw ((GAUGE_MASK_BITS shr 8) or ((GAUGE_MASK_BITS and 0FFh) shl 8))
GAUGE_MASK_WIDTH = GAUGE_MASK_WIDTH + 1
endm
