; Complete TH03 MAIN sound owner; symbolic instructions and natural alignment.
.386
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
extrn _snd_fm_possible:byte, _snd_midi_active:byte, _snd_active:byte
PMD = 60h
PMD_GET_DRIVER_TYPE_AND_VERSION = 9
SHARED segment word public 'CODE' use16
assume cs:SHARED, ds:DGROUP
public _snd_determine_mode
_snd_determine_mode proc far
 mov ah, PMD_GET_DRIVER_TYPE_AND_VERSION
 int PMD
 xor bx, bx
 cmp al, 0FFh
 je use_midi_mode
 inc bx
 mov _snd_fm_possible, 1
 jmp short store_mode
use_midi_mode:
 mov bl, _snd_midi_active
store_mode:
 mov _snd_active, bl
 mov ax, bx
 retf
_snd_determine_mode endp
 even
SHARED ends
end
