; Original Japanese Borland multibyte character-width conversion.
; Complete two FAR ABI exports with real Shift-JIS mapping tables:
; __mbbtombc maps single/halfwidth bytes to fullwidth Shift-JIS;
; __mbctombb maps fullwidth Shift-JIS to its original single-byte form.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __mbbtombc,__mbctombb

__mbbtombc proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    cmp ax,20h
    jb short maybe_halfwidth
    cmp ax,7eh
    ja short maybe_halfwidth
    mov bx,ax
    sub bx,20h
    add bx,bx
    mov ax,word ptr DGROUP:ascii_fullwidth_sjis[bx]
    jmp short from_single_done
maybe_halfwidth:
    cmp ax,0a1h
    jb short from_single_done
    cmp ax,0dfh
    ja short from_single_done
    mov bx,ax
    sub bx,0a0h
    add bx,bx
    mov ax,word ptr DGROUP:kana_fullwidth_sjis[bx]
    jmp short from_single_done
from_single_done:
    pop di
    pop si
    pop bp
    retf
__mbbtombc endp

__mbctombb proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    mov dx,[bp+6]
    cmp dx,8340h
    jb short maybe_hiragana
    cmp dx,8396h
    ja short maybe_hiragana
    cmp dx,837fh
    jnz short translated_kana
    jmp short unconverted
maybe_hiragana:
    cmp dx,829fh
    jb short search_ascii
    cmp dx,82f1h
    ja short search_ascii
    cmp dx,82ddh
    ja short hiragana_upper_half
    mov ax,0a1h
    jmp short shift_hiragana
hiragana_upper_half:
    mov ax,0a2h
shift_hiragana:
    add dx,ax
translated_kana:
    mov bx,dx
    sub bx,8340h
    mov al,byte ptr DGROUP:kana_halfwidth_reverse[bx]
finish_single_byte:
    mov ah,0
    jmp short finish_single
search_ascii:
    cmp dx,8396h
    ja short unconverted
    mov cx,20h
    mov [bp-2],ds
    mov word ptr [bp-4],offset DGROUP:ascii_fullwidth_sjis
    jmp short compare_ascii_bounds
search_ascii_table:
    les bx,dword ptr [bp-4]
    cmp word ptr es:[bx],dx
    jnz short next_ascii_char
    mov ax,cx
    jmp short finish_single
next_ascii_char:
    inc cx
    add word ptr [bp-4],2
compare_ascii_bounds:
    cmp cx,7eh
    jle short search_ascii_table
    xor cx,cx
search_exceptions:
    mov bx,cx
    add bx,bx
    cmp word ptr DGROUP:sjis_symbol_exceptions[bx],dx
    jnz short next_exception
    mov bx,cx
    mov al,byte ptr DGROUP:single_symbol_exceptions[bx]
    jmp short finish_single_byte
next_exception:
    inc cx
    cmp cx,9
    jl short search_exceptions
unconverted:
    mov ax,dx
finish_single:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
__mbctombb endp
_TEXT ends

_DATA segment word public 'DATA'
; Shift-JIS fullwidth glyphs for ASCII 20h through 7Eh (95 words).
ascii_fullwidth_sjis label word
    dw 08140h,08149h,08168h,08194h,08190h,08193h,08195h,08166h
    dw 08169h,0816Ah,08196h,0817Bh,08143h,0817Ch,08144h,0815Eh
    dw 0824Fh,08250h,08251h,08252h,08253h,08254h,08255h,08256h
    dw 08257h,08258h,08146h,08147h,08183h,08181h,08184h,08148h
    dw 08197h,08260h,08261h,08262h,08263h,08264h,08265h,08266h
    dw 08267h,08268h,08269h,0826Ah,0826Bh,0826Ch,0826Dh,0826Eh
    dw 0826Fh,08270h,08271h,08272h,08273h,08274h,08275h,08276h
    dw 08277h,08278h,08279h,0816Dh,0818Fh,0816Eh,0814Fh,08151h
    dw 08165h,08281h,08282h,08283h,08284h,08285h,08286h,08287h
    dw 08288h,08289h,0828Ah,0828Bh,0828Ch,0828Dh,0828Eh,0828Fh
    dw 08290h,08291h,08292h,08293h,08294h,08295h,08296h,08297h
    dw 08298h,08299h,0829Ah,0816Fh,08162h,08170h,08150h

; Shift-JIS fullwidth glyphs for halfwidth bytes A0h..DFh (64 words).
kana_fullwidth_sjis label word
    dw 08140h,08142h,08175h,08176h,08141h,08145h,08392h,08340h
    dw 08342h,08344h,08346h,08348h,08383h,08385h,08387h,08362h
    dw 0815Bh,08341h,08343h,08345h,08347h,08349h,0834Ah,0834Ch
    dw 0834Eh,08350h,08352h,08354h,08356h,08358h,0835Ah,0835Ch
    dw 0835Eh,08360h,08363h,08365h,08367h,08369h,0836Ah,0836Bh
    dw 0836Ch,0836Dh,0836Eh,08371h,08374h,08377h,0837Ah,0837Dh
    dw 0837Eh,08380h,08381h,08382h,08384h,08386h,08388h,08389h
    dw 0838Ah,0838Bh,0838Ch,0838Dh,0838Fh,08393h,0814Ah,0814Bh

; Fullwidth Katakana 8340h..8396h to halfwidth byte (87 slots).
kana_halfwidth_reverse label byte
    db 0A7h,0B1h,0A8h,0B2h,0A9h,0B3h,0AAh,0B4h,0ABh,0B5h,0B6h,0B6h,0B7h,0B7h,0B8h,0B8h
    db 0B9h,0B9h,0BAh,0BAh,0BBh,0BBh,0BCh,0BCh,0BDh,0BDh,0BEh,0BEh,0BFh,0BFh,0C0h,0C0h
    db 0C1h,0C1h,0AFh,0C2h,0C2h,0C3h,0C3h,0C4h,0C4h,0C5h,0C6h,0C7h,0C8h,0C9h,0CAh,0CAh
    db 0CAh,0CBh,0CBh,0CBh,0CCh,0CCh,0CCh,0CDh,0CDh,0CDh,0CEh,0CEh,0CEh,0CFh,0D0h,000h
    db 0D1h,0D2h,0D3h,0ACh,0D4h,0ADh,0D5h,0AEh,0D6h,0D7h,0D8h,0D9h,0DAh,0DBh,0DCh,0DCh
    db 0B2h,0B4h,0A6h,0DDh,0B3h,0B6h,0B9h

; Original non-alphanumeric Shift-JIS exceptions (nine words).
sjis_symbol_exceptions label word
    dw 08142h,08175h,08176h,08141h,08145h,0815Bh,0814Ah,0814Bh
    dw 00000h

; Matching original single-byte symbols (nine bytes).
single_symbol_exceptions label byte
    db 0A1h,0A2h,0A3h,0A4h,0A5h,0B0h,0DEh,0DFh,000h
_DATA ends
end
