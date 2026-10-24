; Zero-byte TLINK segment-order scaffold for the complete Chiyuri producer.
; The prior boss order scaffold stops before PELLET_PUT. Chiyuri's bomb,
; extra attack and selection objects precede the other character producers
; in the literal relocation stream. Declare their real CODE segments here
; so TLINK retains their physical order when those objects link early.
; This module owns no target bytes and contains no game instructions.
.386

PELLET_PUT segment byte public 'CODE' use16
PELLET_PUT ends

BULLET_TEXT segment byte public 'CODE' use16
BULLET_TEXT ends

E_FIREB_TEXT segment byte public 'CODE' use16
E_FIREB_TEXT ends

main_05_TEXT segment byte public 'CODE' use16
main_05_TEXT ends

P_EXATT_TEXT segment byte public 'CODE' use16
P_EXATT_TEXT ends

main_06_TEXT segment byte public 'CODE' use16
main_06_TEXT ends

main_07_TEXT segment byte public 'CODE' use16
main_07_TEXT ends

main_08_TEXT segment byte public 'CODE' use16
main_08_TEXT ends

main_09_TEXT segment byte public 'CODE' use16
main_09_TEXT ends

main_10_TEXT segment byte public 'CODE' use16
main_10_TEXT ends

main_11_TEXT segment byte public 'CODE' use16
main_11_TEXT ends

end
