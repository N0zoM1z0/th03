; Default sixteen-color RGB palette, tone and resident/notebook state.
public _PaletteTone,PaletteTone
PaletteTone label word
_PaletteTone dw 100
public _PalettesInit,PalettesInit
PalettesInit label byte
_PalettesInit label byte
palette_color = 0
REPT 16
    palette_gray = 0
    IF palette_color LT 8
        palette_level = 0ffh
    ELSE
        palette_level = 0aah
    ENDIF
    IF palette_color EQ 8
        palette_level = 0
        palette_gray = 077h
    ENDIF
    DB (((palette_color SHR 1) AND 1) * palette_level) OR palette_gray
    DB (((palette_color SHR 2) AND 1) * palette_level) OR palette_gray
    DB ((palette_color AND 1) * palette_level) OR palette_gray
    palette_color = palette_color + 1
ENDM
public _PaletteNote,PaletteNote
PaletteNote label word
_PaletteNote dw 0
public _ResPalSeg,ResPalSeg
ResPalSeg label word
_ResPalSeg dw 0
public _SdiExists,SdiExists
SdiExists label word
_SdiExists dw 0
