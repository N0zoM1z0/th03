; Detect installed PC-98 PMD driver mode and set shared sound capabilities.
; Original 29-instruction-byte far C interface plus natural CODE alignment.
; The BIOS/PMD status register is preserved; BX returns the active-mode value.
.8086
SHARED segment word public 'CODE'
assume cs:SHARED, ds:DGROUP
extrn _snd_active:byte, _snd_midi_active:byte, _snd_fm_possible:byte
public _snd_determine_mode

_snd_determine_mode label far
    mov ah, 9
    int 60h
    xor bx, bx
    cmp al, 0ffh
    je use_midi
    inc bx
    mov byte ptr DGROUP:_snd_fm_possible, 1
    jmp short store_mode
use_midi:
    mov bl, byte ptr DGROUP:_snd_midi_active
store_mode:
    mov byte ptr DGROUP:_snd_active, bl
    mov ax, bx
    retf
    even
SHARED ends

_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA, _BSS
end
