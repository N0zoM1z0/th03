; Complete TH03 MAIN sound owner; symbolic instructions and natural alignment.
.386
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
extrn _snd_se_frame:byte, _snd_se_playing:byte
SE_NONE = 0FFh
SHARED segment word public 'CODE' use16
assume cs:SHARED, ds:DGROUP
public _snd_se_reset
_snd_se_reset proc far
 mov _snd_se_frame, 0
 mov _snd_se_playing, SE_NONE
 retf
_snd_se_reset endp
 even
SHARED ends
end
