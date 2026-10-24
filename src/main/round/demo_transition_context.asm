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
HITCIRC_TEXT segment byte public 'CODE' use16
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
HITCIRC_TEXT segment byte public 'CODE' use16
assume cs:main_01,ds:_DATA,ss:nothing,es:nothing,fs:nothing,gs:nothing
extrn sub_B39E:far
public sub_B4A3,sub_B4A8,sub_B60A
public _stage_background_update_none
_stage_background_update_none label near
sub_B4A3	proc near
		push	bp
		mov	bp, sp
		pop	bp
		retn
sub_B4A3	endp
public _stage_demo_finish
_stage_demo_finish label near
sub_B4A8	proc near
		push	bp
		mov	bp, sp
		push	si
		cmp	byte_1FBC2, 0
		jnz	short loc_B4E3
		mov	word_1FBC4, 12Fh
		mov	word_1FBC6, 17Eh
		mov	word_1FBC8, 10h
		mov	word_1FBCA, 17Eh
		mov	word_1FBCC, 10h
		mov	word_1FBCE, 10h
		mov	word_1FBD0, 12Fh
		mov	word_1FBD2, 10h
loc_B4E3:
		call	grc_setclip pascal, (8 shl 16) or 0, (623 shl 16) or 191
		sub	word_1FBC4, 12h
		sub	word_1FBCA, 17h
		add	word_1FBCC, 12h
		add	word_1FBD2, 17h
		call	grcg_setcolor pascal, (GC_RMW shl 16) + 2
		mov	trapezoid_hmask, 5555h
		xor	si, si
		jmp	short loc_B565
loc_B51D:
		lea	ax, [si+303]
		push	ax
		push	8
		lea	ax, [si+303]
		push	ax
		push	191
		mov	ax, word_1FBC4
		add	ax, si
		push	ax
		mov	ax, word_1FBC6
		cwd
		sub	ax, dx
		sar	ax, 1
		push	ax
		call	grcg_triangle
		lea	ax, [si+16]
		push	ax
		push	8
		lea	ax, [si+16]
		push	ax
		push	191
		mov	ax, word_1FBCC
		add	ax, si
		push	ax
		mov	ax, word_1FBCE
		cwd
		sub	ax, dx
		sar	ax, 1
		push	ax
		call	grcg_triangle
		add	si, 140h
loc_B565:
		cmp	si, 140h
		jle	short loc_B51D
		mov	trapezoid_hmask, 0AAAAh
		xor	si, si
		jmp	short loc_B5BD
loc_B575:
		lea	ax, [si+16]
		push	ax
		push	191
		lea	ax, [si+303]
		push	ax
		push	191
		mov	ax, word_1FBC8
		add	ax, si
		push	ax
		mov	ax, word_1FBCA
		cwd
		sub	ax, dx
		sar	ax, 1
		push	ax
		call	grcg_triangle
		lea	ax, [si+16]
		push	ax
		push	8
		lea	ax, [si+303]
		push	ax
		push	8
		mov	ax, word_1FBD0
		add	ax, si
		push	ax
		mov	ax, word_1FBD2
		cwd
		sub	ax, dx
		sar	ax, 1
		push	ax
		call	grcg_triangle
		add	si, 140h
loc_B5BD:
		cmp	si, 140h
		jle	short loc_B575
		inc	byte_1FBC2
		cmp	byte_1FBC2, 10h
		jb	short loc_B5EE
		mov	bx, 3932h
		nopcall	sub_B39E
		mov	bx, 395Ah
		nopcall	sub_B39E
		mov	byte_1FBC3, 1
		mov	byte_1FBC2, 0
		mov	fp_1FBC0, offset sub_B60A
loc_B5EE:
		mov	trapezoid_hmask, 0FFFFh
		call	grcg_off
		call	grc_setclip pascal, large 0, ((RES_X - 1) shl 16) or (SPRITE16_RES_Y - 1)
		pop	si
		pop	bp
		retn
sub_B4A8	endp
sub_B60A	proc near
		push	bp
		mov	bp, sp
		push	si
		cmp	byte_1FBC2, 0
		jnz	short loc_B645
		mov	word_1FBC4, 12Fh
		mov	word_1FBC6, 10h
		mov	word_1FBC8, 12Fh
		mov	word_1FBCA, 17Eh
		mov	word_1FBCC, 10h
		mov	word_1FBCE, 17Eh
		mov	word_1FBD0, 10h
		mov	word_1FBD2, 10h
loc_B645:
		call	grc_setclip pascal, (16 shl 16) or 0, (623 shl 16) or 191
		add	word_1FBC6, 17h
		sub	word_1FBC8, 12h
		sub	word_1FBCE, 17h
		add	word_1FBD0, 12h
		call	grcg_setcolor pascal, (GC_RMW shl 16) + 2
		xor	si, si
		jmp	loc_B706
loc_B67A:
		lea	ax, [si+16]
		push	ax
		push	191
		lea	ax, [si+303]
		push	ax
		push	191
		mov	ax, word_1FBC4
		add	ax, si
		push	ax
		mov	ax, word_1FBC6
		cwd
		sub	ax, dx
		sar	ax, 1
		push	ax
		call	grcg_triangle
		lea	ax, [si+16]
		push	ax
		push	8
		lea	ax, [si+16]
		push	ax
		push	191
		mov	ax, word_1FBC8
		add	ax, si
		push	ax
		mov	ax, word_1FBCA
		cwd
		sub	ax, dx
		sar	ax, 1
		push	ax
		call	grcg_triangle
		lea	ax, [si+16]
		push	ax
		push	8
		lea	ax, [si+303]
		push	ax
		push	8
		mov	ax, word_1FBCC
		add	ax, si
		push	ax
		mov	ax, word_1FBCE
		cwd
		sub	ax, dx
		sar	ax, 1
		push	ax
		call	grcg_triangle
		lea	ax, [si+303]
		push	ax
		push	8
		lea	ax, [si+303]
		push	ax
		push	191
		mov	ax, word_1FBD0
		add	ax, si
		push	ax
		mov	ax, word_1FBD2
		cwd
		sub	ax, dx
		sar	ax, 1
		push	ax
		call	grcg_triangle
		add	si, 140h
loc_B706:
		cmp	si, 140h
		jle	loc_B67A
		inc	byte_1FBC2
		cmp	byte_1FBC2, 10h
		jb	short loc_B724
		mov	byte_1FBC2, 0
		mov	fp_1FBC0, offset sub_B4A3
loc_B724:
		call	grcg_off
		call	grc_setclip pascal, large 0, ((RES_X - 1) shl 16) or (SPRITE16_RES_Y - 1)
		pop	si
		pop	bp
		retn
sub_B60A	endp
HITCIRC_TEXT ends
end
