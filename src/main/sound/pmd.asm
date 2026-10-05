; Complete TH03 MAIN sound owner; symbolic instructions and natural alignment.
.386
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
extrn _snd_interrupt_if_midi:byte, _snd_midi_active:byte
extrn _snd_fm_possible:byte, _snd_midi_possible:byte
PMD = 60h
SHARED segment byte public 'CODE' use16
assume cs:SHARED, ds:DGROUP
public _snd_pmd_resident
_snd_pmd_resident proc far
 mov _snd_interrupt_if_midi, PMD
 mov _snd_midi_active, 0
 mov _snd_fm_possible, 0
 mov _snd_midi_possible, 0
 xor ax, ax
 mov es, ax
 les bx, dword ptr es:[PMD*4]
 cmp byte ptr es:[bx+2], 'P'
 jne pmd_absent
 cmp byte ptr es:[bx+3], 'M'
 jne pmd_absent
 cmp byte ptr es:[bx+4], 'D'
 jne pmd_absent
 mov ax, 1
 retf
pmd_absent:
 xor ax, ax
 retf
_snd_pmd_resident endp
 even
SHARED ends
end
