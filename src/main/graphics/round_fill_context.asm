; Unowned reference context from the pinned MAIN carrier.
; Source/behavior credit remains open; this TU preserves the current layout.
.386
.model use16 large _TEXT
include compat/rec98/ReC98.inc
include compat/rec98/th02/gaiji/boldfont.inc
include compat/rec98/th03/arg_bx.inc
include compat/rec98/th03/th03.inc
include compat/rec98/th03/main/playfld.inc
include compat/rec98/th03/main/collmap.inc
include compat/rec98/th03/sprites/main_s16.inc
include compat/rec98/th03/sprite16.inc
include compat/rec98/libs/sprite16/sprite16.inc
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
extrn fp_1FBC0:word
extrn byte_1FBC2:byte
extrn byte_1FBC3:byte
extrn word_1FBC4:word
extrn word_1FBC6:word
extrn word_1FBC8:word
extrn word_1FBCA:word
extrn word_1FBCC:word
extrn word_1FBCE:word
extrn word_1FBD0:word
extrn word_1FBD2:word
extrn _pi_headers:PiHeader,_pi_buffers:dword,GRAPH_PI_FREE:far
extrn trapezoid_hmask:word
extrn _execl:far,@MRS_FREE$QI:far,@game_exit$qv:far
extrn SUPER_FREE:far,GRAPH_HIDE:far,TEXT_CLEAR:far,GAIJI_RESTORE:far
extrn GRCG_TRIANGLE:far,GRCG_OFF:far,GRC_SETCLIP:far,GRCG_SETCOLOR:far
HITCIRC_TEXT segment word public 'CODE' use16
assume cs:main_01,ds:_DATA,ss:nothing,es:nothing,fs:nothing,gs:nothing
public sub_B37C,sub_B398,sub_B39E,sub_B3A2,sub_B3F6
public _bomb_bg_fill
_bomb_bg_fill = sub_B39E
public _round_playfield_clear
_round_playfield_clear label near
sub_B37C	proc near
		mov	ax, 0A828h
loc_B37F:
		push	di
		mov	di, bx
		mov	es, ax
		assume es:nothing
		xor	eax, eax
		not	eax
loc_B38A:
		mov	cx, 9
		rep stosd
		sub	di, 74h	; 't'
		jge	short loc_B38A
		pop	di
		retn
sub_B37C	endp
		nop
public _hud_gauge_highlight_fill
_hud_gauge_highlight_fill label near
sub_B398	proc near
		mov	ax, 0ABC0h
		jmp	short loc_B37F
sub_B398	endp
		nop
sub_B39E	proc far
		call	sub_B37C
		retf
sub_B39E	endp
public _hud_gauge_highlights_restore
_hud_gauge_highlights_restore label near
sub_B3A2	proc near
		push	di
		push	si
		EGC_SETUP_COPY
		mov	dx, ds
		mov	di, 232h
		mov	si, 40D8h
		mov	ax, 0ABC0h
		mov	es, ax
		assume es:nothing
		mov	ds, ax
		assume ds:nothing
		nop
loc_B3DE:
		mov	cx, 12h
loc_B3E1:
		movsw
		mov	es:[di+26h], ax
		loop	loc_B3E1
		sub	si, 74h	; 't'
		sub	di, 74h	; 't'
		jge	short loc_B3DE
		mov	ds, dx
		assume ds:_DATA
		pop	si
		pop	di
		retn
sub_B3A2	endp
		nop
public _hud_gauge_bar_fill
_hud_gauge_bar_fill label near
sub_B3F6	proc near
		push	di
		push	si
		mov	di, 0F0h
		mov	ax, 0ABCAh
		mov	es, ax
		assume es:nothing
		mov	si, 50h	; 'P'
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
		jz	short loc_B446
		mov	dx, ax
		shl	ax, 1
		add	si, ax
		xor	ax, ax
		not	ax
		nop
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
		jz	short loc_B450
		add	di, 0F0h
loc_B446:
		mov	ax, [bx+64Ch]
loc_B44A:
		stosw
		sub	di, 52h	; 'R'
		jge	short loc_B44A
loc_B450:
		pop	si
		pop	di
		retn
sub_B3F6	endp
		nop
HITCIRC_TEXT ends
end
