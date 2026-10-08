; Zero-byte TLINK segment-order scaffold for the complete Chiyuri producer.
; The prior boss order scaffold stops before PELLET_PUT. Since the natural
; Chiyuri compiler object must link before frozen main.obj, these empty
; declarations retain the original first-seen CODE segment ordering.
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

end
