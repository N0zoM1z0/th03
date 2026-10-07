; Zero-byte segment-order scaffold for carved MAIN_03_TEXT producers.
; It owns no game bytes. Its only purpose is to preserve the historical
; TLINK first-seen segment order when natural boss objects precede main.obj.
.386

_TEXT segment word public 'CODE' use16
_TEXT ends
PLAYFLD_TEXT segment word public 'CODE' use16
PLAYFLD_TEXT ends
CFG_LRES_TEXT segment byte public 'CODE' use16
CFG_LRES_TEXT ends
HITCIRC_TEXT segment word public 'CODE' use16
HITCIRC_TEXT ends
HUD_STAT_TEXT segment byte public 'CODE' use16
HUD_STAT_TEXT ends
PLAYER_M_TEXT segment byte public 'CODE' use16
PLAYER_M_TEXT ends
main_010_TEXT segment word public 'CODE' use16
main_010_TEXT ends
P_SHOT_TEXT segment byte public 'CODE' use16
P_SHOT_TEXT ends
SHARED segment word public 'CODE' use16
SHARED ends
main_03_TEXT segment byte public 'CODE' use16
main_03_TEXT ends
main_04_TEXT segment byte public 'CODE' use16
main_04_TEXT ends
COLLMAP_TEXT segment byte public 'CODE' use16
COLLMAP_TEXT ends
ENEMY_2_TEXT segment byte public 'CODE' use16
ENEMY_2_TEXT ends
HITBOX_TEXT segment byte public 'CODE' use16
HITBOX_TEXT ends
P_COMBO_TEXT segment byte public 'CODE' use16
P_COMBO_TEXT ends
P_GAUGE_TEXT segment byte public 'CODE' use16
P_GAUGE_TEXT ends
E_ENEMY_TEXT segment byte public 'CODE' use16
E_ENEMY_TEXT ends
ENEMY_PUT segment byte public 'CODE' use16
ENEMY_PUT ends
E_EXPL_TEXT segment byte public 'CODE' use16
E_EXPL_TEXT ends

end
