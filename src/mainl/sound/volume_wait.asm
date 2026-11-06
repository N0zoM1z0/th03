; Poll the PMD/MMD volume interrupt until AL matches the caller's volume.
; 27 original instruction bytes, one native assembler CODE alignment byte.
.8086
SHARED segment word public 'CODE'
assume cs:SHARED, ds:DGROUP
extrn _snd_midi_active:byte
public _snd_delay_until_volume

_snd_delay_until_volume label far
    push bp
    mov bp, sp
again:
    mov ah, 8
    cmp byte ptr DGROUP:_snd_midi_active, 1
    je midi
    int 60h
    jmp short compare
midi:
    int 61h
compare:
    cmp al, byte ptr [bp+6]
    je finished
    jmp short again
finished:
    pop bp
    retf
    even
SHARED ends

_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA, _BSS
end
