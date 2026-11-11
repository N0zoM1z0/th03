; Clear the sound effect frame and mark the playback slot as empty.
; This is a far no-argument original interface, not a new effect routine.
.8086
SHARED segment word public 'CODE'
assume cs:SHARED, ds:DGROUP
extrn _snd_se_playing:byte, _snd_se_frame:byte
public _snd_se_reset

_snd_se_reset label far
    mov byte ptr DGROUP:_snd_se_frame, 0
    mov byte ptr DGROUP:_snd_se_playing, 0ffh
    retf
    even
SHARED ends

_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
; TASM serializes GROUP members in reverse declaration order.
DGROUP group _BSS, _DATA
end
