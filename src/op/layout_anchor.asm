; Source-only layout hypothesis: no bytes, publics, or fixups.
; Existing CODE segments and real GROUP_01 membership only.
.386
OP_01_TEXT segment byte public 'CODE' use16
OP_01_TEXT ends
OP_MUSIC_TEXT segment byte public 'CODE' use16
OP_MUSIC_TEXT ends
OP_MAIN_TEXT segment byte public 'CODE' use16
OP_MAIN_TEXT ends
OP_02_TEXT segment byte public 'CODE' use16
OP_02_TEXT ends
SCOREDAT_TEXT segment byte public 'CODE' use16
SCOREDAT_TEXT ends
OP_SEL_TEXT segment byte public 'CODE' use16
OP_SEL_TEXT ends
GROUP_01 group OP_01_TEXT, OP_MUSIC_TEXT, OP_MAIN_TEXT, OP_02_TEXT, SCOREDAT_TEXT, OP_SEL_TEXT
end
