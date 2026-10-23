; MAIN A3FA..A44C: existing random-ring and collision reset primitives.
; The included owners retain their full bytes and their original near ABIs.
.386
.model use16 large _TEXT
locals
RANDRING_SIZE=256
COLLMAP_SIZE=((288/2)/8)*(368/2)
PLAYER_COUNT=2
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
extrn _randring:byte,_randring_p:byte,_collmap:byte
_BSS ends
DGROUP group _DATA,_BSS
PLAYFLD_TEXT segment word public 'CODE' use16
PLAYFLD_TEXT ends
CFG_LRES_TEXT segment word public 'CODE' use16
CFG_LRES_TEXT ends
main_01 group PLAYFLD_TEXT,CFG_LRES_TEXT,HITCIRC_TEXT
extern IRAND:far
HITCIRC_TEXT segment word public 'CODE' use16
assume cs:main_01,ds:DGROUP,es:nothing
include src/main/math/randring_getters.inl
include src/main/math/randring_fill.inl
RANDRING_NEXT_DEF_NOMOD 1, near
include src/main/collision/reset.inl
HITCIRC_TEXT ends
end
