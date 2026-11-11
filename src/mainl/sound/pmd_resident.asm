; Inspect the resident PMD interrupt vector and signature at offset 2.
; Reset MIDI/FM capability state before probing. Far returns AX=1/0.
.8086
SHARED segment byte public 'CODE'
assume cs:SHARED, ds:DGROUP
extrn _snd_interrupt_if_midi:byte, _snd_midi_possible:byte
extrn _snd_midi_active:byte, _snd_fm_possible:byte
public _snd_pmd_resident

_snd_pmd_resident label far
    mov byte ptr DGROUP:_snd_interrupt_if_midi, 60h
    mov byte ptr DGROUP:_snd_midi_active, 0
    mov byte ptr DGROUP:_snd_fm_possible, 0
    mov byte ptr DGROUP:_snd_midi_possible, 0
    xor ax, ax
    mov es, ax
    les bx, dword ptr es:[60h * 4]
    cmp byte ptr es:[bx + 2], 'P'
    jne no_pmd
    cmp byte ptr es:[bx + 3], 'M'
    jne no_pmd
    cmp byte ptr es:[bx + 4], 'D'
    jne no_pmd
    mov ax, 1
    retf
no_pmd:
    xor ax, ax
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
