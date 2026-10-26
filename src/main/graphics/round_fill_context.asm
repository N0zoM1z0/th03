; Register-ABI recovery of MAIN load B37C..B454 (216 bytes).
; Derived from the pinned target and ReC98's initial disassembly, not surviving
; original source. Game-specific geometry is established by callers; unchanged
; master.lib module identity is excluded, but original language/authorship is open.
; No new source-exact/behavior ownership is claimed. See docs/MAIN_GRAPHICS_FILL_REVIEW.md.
;
; All entries require DF=0. GRCG color/mode and EGC enable/disable belong to
; callers. Coordinates below are physical VRAM rows (the game uses 200-line
; graphics), not the doubled display-space Y coordinates. No clipping occurs.
.386
.model use16 large _TEXT
include compat/rec98/ReC98.inc
include compat/rec98/th03/main/playfld.inc
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
PLAYFLD_TEXT segment word public 'CODE' use16
PLAYFLD_TEXT ends
CFG_LRES_TEXT segment byte public 'CODE' use16
CFG_LRES_TEXT ends
HITCIRC_TEXT segment word public 'CODE' use16
HITCIRC_TEXT ends
HUD_STAT_TEXT segment byte public 'CODE' use16
HUD_STAT_TEXT ends
PLAYER_M_TEXT segment byte public 'CODE' use16
PLAYER_M_TEXT ends
main_010_TEXT segment word public 'CODE' use16
main_010_TEXT ends
P_SHOT_TEXT segment byte public 'CODE' use16
P_SHOT_TEXT ends
main_01 group PLAYFLD_TEXT,CFG_LRES_TEXT,HITCIRC_TEXT,HUD_STAT_TEXT,PLAYER_M_TEXT,main_010_TEXT,P_SHOT_TEXT
extrn _hud_gauge_left_masks:word

; Blue-plane segment bases retain the target's physical-row addressing.
PLAYFIELD_FILL_SEG = SEG_PLANE_B + ((PLAYFIELD_TOP / 2) * ROW_SIZE / 16)
GAUGE_HIGHLIGHT_SEG = SEG_PLANE_B + (192 * ROW_SIZE / 16)
GAUGE_BAR_SEG = SEG_PLANE_B + (194 * ROW_SIZE / 16)
FILL_ROW_BYTES = (PLAYFIELD_W / BYTE_DOTS)

HITCIRC_TEXT segment word public 'CODE' use16
assume cs:main_01,ds:_DATA,ss:nothing,es:nothing,fs:nothing,gs:nothing
public sub_B37C,sub_B398,sub_B39E,sub_B3A2,sub_B3F6
public _bomb_bg_fill
_bomb_bg_fill = sub_B39E
public _round_playfield_clear
_round_playfield_clear label near
; BX = last-row byte offset relative to PLAYFIELD_FILL_SEG. Callers use
; 3932h / 395Ah: x=16/336, physical rows8..191, 288 pixels wide.
; Near return; BX/DX/SI/DI/BP/DS preserved, EAX=-1, CX=0, ES replaced.
sub_B37C	proc near
		mov	ax, PLAYFIELD_FILL_SEG
fill_rows_from_bx:
		push	di
		mov	di, bx
		mov	es, ax
		assume es:nothing
		xor	eax, eax
		not	eax
fill_previous_row:
		mov	cx, (FILL_ROW_BYTES / 4)
		rep stosd
		sub	di, (ROW_SIZE + FILL_ROW_BYTES)
		jge	short fill_previous_row
		pop	di
		retn
sub_B37C	endp
		nop ; Unreachable after RET/JMP; even-alignment candidate, not proved.
public _hud_gauge_highlight_fill
_hud_gauge_highlight_fill label near
; Same BX contract and clobbers, tail-sharing the fill loop. BX=232h/25Ah
; selects x=16/336 and physical rows192..199 (8 rows, 288 pixels wide).
sub_B398	proc near
		mov	ax, GAUGE_HIGHLIGHT_SEG
		jmp	short fill_rows_from_bx
sub_B398	endp
		nop ; Unreachable after RET/JMP; even-alignment candidate, not proved.
; Far adapter for bomb/transition callers; exactly the same register contract.
; No stack parameters or callee argument cleanup. The inner call stays near.
sub_B39E	proc far
		call	sub_B37C
		retf
sub_B39E	endp
public _hud_gauge_highlights_restore
_hud_gauge_highlights_restore label near
; No arguments; caller enables EGC before entry and disables it afterward.
; Copy 288x8 from physical (320,392) to (16,192) and (336,192).
; MOVSW loads the EGC latch, not AX; the second write reuses that hardware latch.
; Preserves BX/SI/DI/BP/DS; AX=ABC0h, DX=entering DS, CX=0, ES=ABC0h.
sub_B3A2	proc near
		push	di
		push	si
		EGC_SETUP_COPY
		mov	dx, ds
		mov	di, 232h
		mov	si, 40D8h
		mov	ax, GAUGE_HIGHLIGHT_SEG
		mov	es, ax
		assume es:nothing
		mov	ds, ax
		assume ds:nothing
		nop ; B3DD: executed instruction; original purpose unknown.
restore_previous_row:
		mov	cx, 12h
restore_word_to_both_players:
		movsw
		mov	es:[di+26h], ax
		loop	restore_word_to_both_players
		sub	si, (ROW_SIZE + FILL_ROW_BYTES)
		sub	di, (ROW_SIZE + FILL_ROW_BYTES)
		jge	short restore_previous_row
		mov	ds, dx
		assume ds:_DATA
		pop	si
		pop	di
		retn
sub_B3A2	endp
		nop ; Unreachable after RET/JMP; even-alignment candidate, not proved.
public _hud_gauge_bar_fill
_hud_gauge_bar_fill label near
; DX = pixel X, BX = pixel width; near register-only entry. Writes four
; physical rows194..197. X is rounded down to a WORD boundary and its low four
; bits are added to width: deliberately no left-edge mask and no zero-width
; guard. Table index0 is FFFFh, including the zero-full-word path.
; Preserves SI/DI/BP/DS; clobbers AX/BX/CX/DX/ES. Assumes intended gauge range;
; signed DI termination and 16-bit arithmetic are retained, not sanitized.
sub_B3F6	proc near
		push	di
		push	si
		mov	di, 0F0h
		mov	ax, GAUGE_BAR_SEG
		mov	es, ax
		assume es:nothing
		mov	si, ROW_SIZE
		mov	ax, dx
		and	ax, 0Fh
		add	bx, ax
		shr	dx, 4
		shl	dx, 1
		add	di, dx
		mov	ax, bx
		and	bx, 0Fh
		shl	bx, 1
		shr	ax, 4
		jz	short fill_partial_word
		mov	dx, ax
		shl	ax, 1
		add	si, ax
		xor	ax, ax
		not	ax
		nop ; B427: executed instruction; original purpose unknown.
		mov	cx, dx
		rep stosw
		sub	di, si
		mov	cx, dx
		rep stosw
		sub	di, si
		mov	cx, dx
		rep stosw
		sub	di, si
		mov	cx, dx
		rep stosw
		or	bx, bx
		jz	short bar_fill_return
		add	di, 0F0h
fill_partial_word:
		mov	ax, _hud_gauge_left_masks[bx]
fill_partial_previous_row:
		stosw
		sub	di, (ROW_SIZE + 2)
		jge	short fill_partial_previous_row
bar_fill_return:
		pop	si
		pop	di
		retn
sub_B3F6	endp
		nop ; Unreachable after RET/JMP; even-alignment candidate, not proved.
HITCIRC_TEXT ends
end
