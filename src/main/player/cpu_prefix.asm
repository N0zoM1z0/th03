; Retained reference assembly carrier: C0D8..C370, 664 original bytes.
; This extraction earns no authored-source or exactness credit.
.386
.model use16 large _TEXT
include compat/rec98/ReC98.inc
include compat/rec98/th03/th03.inc
include compat/rec98/th03/main/playfld.inc
include src/main/player/cpu_prefix_types.inc

DF_NONE = 0
DF_EXPLODE = 1
DF_BANNER = 2

_DATA segment word public 'DATA' use16
extrn PaletteTone:word
extrn _CosTable8:word
extrn _SinTable8:word
_DATA ends
_BSS segment word public 'BSS' use16
extrn _damage_all_on:byte
extrn _defeat_flag:byte
extrn _pid_PID_current:byte
extrn _players:player_stuff_t
extrn _playfield_fg_shift_x:word
extrn _resident:dword
extrn _round_or_result_frame:word
extrn _sprite16_clip_left:word
extrn _sprite16_clip_right:word
extrn _sprite16_put_h:word
extrn _sprite16_put_w:byte
extrn byte_20E3D:byte
extrn byte_23AF9:byte
extrn word_20E3E:word
extrn word_20E40:word
extrn word_20E42:word
_BSS ends
DGROUP group _DATA, _BSS

PLAYFLD_TEXT segment word public 'CODE' use16
extern @PLAYFIELD_FG_X_TO_SCREEN$QII:proc
PLAYFLD_TEXT ends
HUD_STAT_TEXT segment byte public 'CODE' use16
@HUD_STATIC_ROUNDS_WON_PUT$QUC procdesc pascal near \
    pid:word
HUD_STAT_TEXT ends
main_01 group PLAYFLD_TEXT, HUD_STAT_TEXT, PLAYER_M_TEXT

extrn @polar$qiii:far
extrn SND_SE_PLAY:far
extrn SPRITE16_PUT:far
extrn SUPER_PUT:far
extrn PALETTE_SHOW:far

PLAYER_M_TEXT segment byte public 'CODE' use16
assume cs:main_01, es:nothing, ss:nothing, ds:_DATA, fs:nothing, gs:nothing
public sub_C0D8, sub_C248, sub_C2F9

sub_C0D8	proc near

arg_0		= word ptr  4

		push	bp
		mov	bp, sp
		push	si
		mov	si, [bp+arg_0]
		cmp	byte ptr [si+1Fh], 30h ; '0'
		jnz	short loc_C127
		push	word ptr [si]	; x
		mov	al, _pid_PID_current
		mov	ah, 0
		push	ax	; pid
		nopcall	@playfield_fg_x_to_screen$qii
		add	ax, -24
		mov	word_20E3E, ax
		mov	ax, [si+2]
		sar	ax, 4
		add	ax, 0FFF8h
		mov	word_20E40, ax
		mov	_defeat_flag, DF_EXPLODE
		call	snd_se_play pascal, 14
		mov	al, _pid_PID_current
		mov	ah, 0
		mov	bx, 1
		sub	bx, ax
		mov	_damage_all_on[bx], 1
		mov	word_20E42, 0
		jmp	short loc_C12C
; ---------------------------------------------------------------------------

loc_C127:
		add	word_20E42, 9

loc_C12C:
		mov	al, [si+1Fh]
		mov	ah, 0
		and	ax, 3
		cmp	ax, 2
		jge	short loc_C14A
		mov	al, _pid_PID_current
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	_playfield_fg_shift_x[bx], 6
		jmp	short loc_C159
; ---------------------------------------------------------------------------

loc_C14A:
		mov	al, _pid_PID_current
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	_playfield_fg_shift_x[bx], -6

loc_C159:
		mov	byte_23AF9, 2
		dec	byte ptr [si+1Fh]
		cmp	byte ptr [si+1Fh], 0
		jnz	short loc_C1CD
		mov	word_20E3E, 0
		mov	word_20E40, 0
		mov	word_20E42, 0
		mov	al, _pid_PID_current
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	_playfield_fg_shift_x[bx], 0
		mov	byte ptr [si+1Fh], -1
		mov	PaletteTone, 100
		call	far ptr	palette_show
		mov	_defeat_flag, DF_BANNER
		mov	al, _pid_PID_current
		mov	ah, 0
		mov	bx, 1
		sub	bx, ax
		shl	bx, 7
		inc	_players[bx].rounds_won
		les	bx, _resident
		assume es:nothing
		mov	al, 1
		sub	al, _pid_PID_current
		mov	es:[bx+resident_t.pid_winner], al
		mov	_round_or_result_frame, 0
		mov	al, 1
		sub	al, _pid_PID_current
		call	@hud_static_rounds_won_put$quc pascal, ax
		jmp	short loc_C1E1
; ---------------------------------------------------------------------------

loc_C1CD:
		mov	ax, _round_or_result_frame
		and	ax, 1
		imul	ax, 30
		add	ax, 100
		mov	PaletteTone, ax
		call	far ptr	palette_show

loc_C1E1:
		pop	si
		pop	bp
		retn	2
sub_C0D8	endp


; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame

sub_C1E6	proc near

@@top		= word ptr -4
@@left		= word ptr -2
arg_0		= byte ptr  4
arg_2		= byte ptr  6

		enter	4, 0
		mov	al, [bp+arg_2]
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		call	@polar$qiii c, word_20E3E, word_20E42, _CosTable8[bx]
		mov	dl, _pid_PID_current
		mov	dh, 0
		add	dx, dx
		mov	bx, dx
		add	ax, _playfield_fg_shift_x[bx]
		mov	[bp+@@left], ax
		mov	al, [bp+arg_0]
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		call	@polar$qiii c, word_20E40, word_20E42, _SinTable8[bx]
		mov	[bp+@@top], ax
		call	sprite16_put pascal, [bp+@@left], ax, 34B4h
		leave
		retn	4
sub_C1E6	endp


; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame

sub_C248	proc near

var_1		= byte ptr -1

		enter	2, 0
		push	si
		push	di
		cmp	_pid_PID_current, 0
		jnz	short loc_C263
		mov	_sprite16_clip_left, PLAYFIELD1_CLIP_LEFT
		mov	_sprite16_clip_right, PLAYFIELD1_CLIP_RIGHT
		jmp	short loc_C26F
; ---------------------------------------------------------------------------

loc_C263:
		mov	_sprite16_clip_left, PLAYFIELD2_CLIP_LEFT
		mov	_sprite16_clip_right, PLAYFIELD2_CLIP_RIGHT

loc_C26F:
		mov	_sprite16_put_w, (48 / 16)
		mov	_sprite16_put_h, 24
		xor	di, di
		mov	ax, word_20E42
		mov	bx, 4
		cwd
		idiv	bx
		jmp	short loc_C299
; ---------------------------------------------------------------------------

loc_C287:
		push	word ptr [bp-1]
		mov	al, [bp+var_1]
		add	al, 20h	; ' '
		push	ax
		call	sub_C1E6
		inc	di
		mov	al, [bp+var_1]
		add	al, 10h

loc_C299:
		mov	[bp+var_1], al
		cmp	di, 10h
		jl	short loc_C287
		xor	di, di
		mov	ax, word_20E42
		mov	bx, 4
		cwd
		idiv	bx
		mov	dl, 0
		sub	dl, al
		mov	[bp+var_1], dl
		jmp	short loc_C2CA
; ---------------------------------------------------------------------------

loc_C2B5:
		push	word ptr [bp+var_1]
		mov	al, [bp+var_1]
		add	al, 0E0h
		push	ax
		call	sub_C1E6
		inc	di
		mov	al, [bp+var_1]
		add	al, 10h
		mov	[bp+var_1], al

loc_C2CA:
		cmp	di, 10h
		jl	short loc_C2B5
		xor	di, di
		mov	ax, word_20E42
		mov	bx, 4
		cwd
		idiv	bx
		jmp	short loc_C2EB
; ---------------------------------------------------------------------------

loc_C2DC:
		push	word ptr [bp+var_1]
		push	word ptr [bp+var_1]
		call	sub_C1E6
		inc	di
		mov	al, [bp+var_1]
		add	al, 10h

loc_C2EB:
		mov	[bp+var_1], al
		cmp	di, 10h
		jl	short loc_C2DC
		pop	di
		pop	si
		leave
		retn	2
sub_C248	endp


; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame

sub_C2F9	proc near

@@frame_mod_32	= word ptr -2

		enter	2, 0
		push	si
		push	di
		mov	al, byte_20E3D
		mov	ah, 0
		imul	ax, PLAYFIELD_W_BORDERED
		add	ax, 96
		mov	si, ax
		call	super_put pascal, ax, large (40 shl 16) or 18
		lea	ax, [si+64]
		call	super_put pascal, ax, large (40 shl 16) or 19
		mov	al, byte_20E3D
		mov	ah, 0
		mov	dx, 1
		sub	dx, ax
		imul	dx, PLAYFIELD_W_BORDERED
		add	dx, 96
		mov	si, dx
		mov	ax, _round_or_result_frame
		and	ax, 31
		mov	[bp+@@frame_mod_32], ax
		cmp	[bp+@@frame_mod_32], 16
		jge	short loc_C34F
		add	ax, 32
		jmp	short loc_C355
; ---------------------------------------------------------------------------

loc_C34F:
		mov	ax, 64
		sub	ax, [bp+@@frame_mod_32]

loc_C355:
		mov	di, ax
		call	super_put pascal, si, di, 20
		lea	ax, [si+64]
		call	super_put pascal, ax, di, 21
		pop	di
		pop	si
		leave
		retn
sub_C2F9	endp


; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame

PLAYER_M_TEXT ends
end
